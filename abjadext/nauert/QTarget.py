import abc
import bisect

import abjad

from .AttackPointOptimizer import AttackPointOptimizer
from .ConcatenatingGraceHandler import ConcatenatingGraceHandler
from .DistanceHeuristic import DistanceHeuristic
from .GraceHandler import GraceHandler
from .Heuristic import Heuristic
from .JobHandler import JobHandler
from .NaiveAttackPointOptimizer import NaiveAttackPointOptimizer
from .QEventSequence import QEventSequence
from .SerialJobHandler import SerialJobHandler
from .SilentQEvent import SilentQEvent


class QTarget:
    """
    Abstract q-target.

    ``QTarget`` is created by a concrete ``QSchema`` instance, and represents
    the mold into which the timepoints contained by a ``QSequence`` instance
    will be poured, as structured by that ``QSchema`` instance.

    Not composer-safe.

    Used internally by the ``Quantizer``.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_items",)

    ### INITIALIZATION ###

    def __init__(self, items=None):
        items = items or []
        # assert len(items)
        assert all(isinstance(x, self.item_class) for x in items)
        self._items = tuple(sorted(items, key=lambda x: x.offset_in_ms))

    ### SPECIAL METHODS ###

    def __call__(
        self,
        q_event_sequence,
        grace_handler=None,
        heuristic=None,
        job_handler=None,
        attack_point_optimizer=None,
        attach_tempos=True,
    ):
        """
        Calls q-target.
        """
        assert isinstance(q_event_sequence, QEventSequence)

        if grace_handler is None:
            grace_handler = ConcatenatingGraceHandler()
        assert isinstance(grace_handler, GraceHandler)

        if heuristic is None:
            heuristic = DistanceHeuristic()
        assert isinstance(heuristic, Heuristic)

        if job_handler is None:
            job_handler = SerialJobHandler()
        assert isinstance(job_handler, JobHandler)

        if attack_point_optimizer is None:
            attack_point_optimizer = NaiveAttackPointOptimizer()
        assert isinstance(attack_point_optimizer, AttackPointOptimizer)

        # if next-to-last QEvent is silent, pop the TerminalQEvent,
        # in order to prevent rest-tuplets
        q_events = q_event_sequence
        if isinstance(q_event_sequence[-2], SilentQEvent):
            q_events = q_event_sequence[:-1]

        # parcel QEvents out to each beat
        beats = self.beats
        offsets = sorted([beat.offset_in_ms for beat in beats])
        for q_event in q_events:
            index = bisect.bisect(offsets, q_event.offset) - 1
            beat = beats[index]
            beat.q_events.append(q_event)

        # generate QuantizationJobs and process with the JobHandler
        jobs = [beat(i) for i, beat in enumerate(beats)]
        jobs = [job for job in jobs if job]
        jobs = job_handler(jobs)
        for job in jobs:
            beats[job.job_id]._q_grids = job.q_grids

        # for i, beat in enumerate(beats):
        #    print i, len(beat.q_grids)
        #    for q_event in beat.q_events:
        #        print '\t{}'.format(q_event.offset)

        # select the best QGrid for each beat, according to the Heuristic
        beats = heuristic(beats)

        # shift QEvents attached to each QGrid's "next downbeat"
        # over to the next QGrid's first leaf - the real downbeat
        self._shift_downbeat_q_events_to_next_q_grid()

        #  TODO: handle a final QGrid with QEvents attached to its
        #        next_downbeat.
        #  TODO: remove a final QGrid with no QEvents

        # convert the QGrid representation into notation,
        # handling grace-note behavior with the GraceHandler
        return self._notate(
            attach_tempos=attach_tempos,
            attack_point_optimizer=attack_point_optimizer,
            grace_handler=grace_handler,
        )

    ### PRIVATE METHODS ###

    @abc.abstractmethod
    def _notate(
        self,
        grace_handler=None,
        attack_point_optimizer=None,
        attach_tempos=True,
    ):
        pass

    def _notate_leaves(self, grace_handler=None, voice=None):
        for leaf in abjad.iterate(voice).leaves():
            if leaf._has_indicator(dict):
                annotation = leaf._get_indicator(dict)
                q_events = annotation["q_events"]
                pitches, grace_container = grace_handler(q_events)
                if not pitches:
                    new_leaf = abjad.Rest(leaf)
                elif 1 < len(pitches):
                    new_leaf = abjad.Chord(leaf)
                    new_leaf.written_pitches = pitches
                else:
                    new_leaf = abjad.Note(leaf)
                    new_leaf.written_pitch = pitches[0]
                if grace_container:
                    abjad.attach(grace_container, new_leaf)
                abjad.mutate.replace(leaf, new_leaf)
                if not isinstance(new_leaf, abjad.Rest):
                    abjad.annotate(new_leaf, "tie_to_next", True)
            else:
                previous_leaf = abjad._iterate._get_leaf(leaf, -1)
                if isinstance(previous_leaf, abjad.Rest):
                    new_leaf = type(previous_leaf)(leaf.written_duration)
                elif isinstance(previous_leaf, abjad.Note):
                    new_leaf = type(previous_leaf)(
                        previous_leaf.written_pitch, leaf.written_duration
                    )
                else:
                    new_leaf = type(previous_leaf)(
                        previous_leaf.written_pitch, leaf.written_duration
                    )
                abjad.mutate.replace(leaf, new_leaf)
                if abjad.get.annotation(previous_leaf, "tie_to_next") is True:
                    leaves = abjad.select([previous_leaf, new_leaf])
                    abjad.tie(leaves)
                    abjad.annotate(new_leaf, "tie_to_next", True)
            if leaf._has_indicator(abjad.MetronomeMark):
                tempo = leaf._get_indicator(abjad.MetronomeMark)
                abjad.detach(abjad.MetronomeMark, leaf)
                abjad.detach(abjad.MetronomeMark, new_leaf)
                abjad.attach(tempo, new_leaf)
            if leaf._has_indicator(abjad.TimeSignature):
                time_signature = leaf._get_indicator(abjad.TimeSignature)
                abjad.detach(abjad.TimeSignature, leaf)
                abjad.detach(abjad.TimeSignature, new_leaf)
                abjad.attach(time_signature, new_leaf)

    def _shift_downbeat_q_events_to_next_q_grid(self):
        beats = self.beats
        for one, two in abjad.sequence(beats).nwise():
            one_q_events = one.q_grid.next_downbeat.q_event_proxies
            two_q_events = two.q_grid.leaves[0].q_event_proxies
            while one_q_events:
                two_q_events.append(one_q_events.pop())

    ### PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def beats(self):
        r"""Beats of q-target."""
        raise NotImplementedError

    @property
    def duration_in_ms(self):
        r"""Duration of q-target in milliseconds.

        Returns duration.
        """
        last_item = self._items[-1]
        return last_item.offset_in_ms + last_item.duration_in_ms

    @abc.abstractproperty
    def item_class(self):
        r"""Item class of q-target."""
        raise NotImplementedError

    @property
    def items(self):
        r"""Items of q-target."""
        return self._items
