import abc
import typing

import abjad

from .qevents import PitchedQEvent, QEvent, SilentQEvent


class GraceHandler(abc.ABC):
    """
    Abstract grace-handler.

    Determines what pitch, if any, will be selected from a list of
    ``QEvents`` to be applied to an attack-point generated by a ``QGrid``,
    and whether there should be a ``BeforeGraceContainer`` attached to that
    attack-point.

    When called on a sequence of ``QEvents``, ``GraceHandler``
    subclasses should return a pair, where the first item of the pair
    is a sequence of pitch tokens or ``None``, and where the
    second item of the pair is a ``BeforeGraceContainer`` instance or None.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __call__(
        self, q_events
    ) -> tuple[
        tuple[abjad.NamedPitch, ...],
        typing.Optional[tuple],
        typing.Optional[abjad.BeforeGraceContainer],
    ]:
        """
        Calls grace handler.
        """
        raise NotImplementedError


class CollapsingGraceHandler(GraceHandler):
    r"""
    Collapsing grace-handler.

    Collapses pitch information into a single chord rather than creating a
    grace container.

    ..  container:: example

        >>> durations = [1000, 1, 1, 997]
        >>> pitches = [0, 7, 4, 0]
        >>> q_event_sequence = nauert.QEventSequence.from_millisecond_pitch_pairs(
        ...     tuple(zip(durations, pitches))
        ... )
        >>> grace_handler = nauert.CollapsingGraceHandler()
        >>> result = nauert.quantize(
        ...     q_event_sequence, grace_handler=grace_handler
        ... )
        >>> abjad.show(result) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(result)
            >>> print(string)
            \new Voice
            {
                {
                    \tempo 4=60
                    %%% \time 4/4 %%%
                    c'4
                    <c' e' g'>4
                    r4
                    r4
                }
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __call__(
        self, q_events: typing.Sequence[QEvent]
    ) -> tuple[tuple[abjad.NamedPitch, ...], tuple, None]:
        """
        Calls collapsing grace handler.
        """
        pitches: list[abjad.NamedPitch] = []
        attachments: list[typing.Any] = []
        for q_event in q_events:
            if isinstance(q_event, PitchedQEvent):
                pitches.extend(q_event.pitches)
                attachments.extend(q_event.attachments)
        return tuple(pitches), tuple(attachments), None


class ConcatenatingGraceHandler(GraceHandler):
    r"""
    Concatenating grace-handler.

    Concatenates all but the final ``QEvent`` attached to a ``QGrid`` offset
    into a ``BeforeGraceContainer``, using a fixed leaf duration ``duration``.

    When called, it returns pitch information of final ``QEvent``, and the
    generated ``BeforeGraceContainer``, if any.

    ..  container:: example

        >>> durations = [1000, 1, 999]
        >>> pitches = [0, 2, 0]
        >>> q_event_sequence = nauert.QEventSequence.from_millisecond_pitch_pairs(
        ...     tuple(zip(durations, pitches))
        ... )
        >>> grace_handler = nauert.ConcatenatingGraceHandler()
        >>> result = nauert.quantize(
        ...     q_event_sequence, grace_handler=grace_handler
        ... )
        >>> abjad.show(result) # doctest: +SKIP

        ..  docs::

            >>> print(abjad.lilypond(result))
            \new Voice
            {
                {
                    \tempo 4=60
                    %%% \time 4/4 %%%
                    c'4
                    \grace {
                        d'16
                    }
                    c'4
                    r4
                    r4
                }
            }

    ..  container:: example

        When ``discard_grace_rest`` is set to ``True`` (the default), all the
        grace rests are discarded.

        >>> durations = [1000, 1, 999]
        >>> pitches = [0, None, 0]
        >>> q_event_sequence = nauert.QEventSequence.from_millisecond_pitch_pairs(
        ...     tuple(zip(durations, pitches))
        ... )
        >>> grace_handler = nauert.ConcatenatingGraceHandler()
        >>> result = nauert.quantize(q_event_sequence, grace_handler=grace_handler)
        >>> abjad.show(result) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(result)
            >>> print(string)
            \new Voice
            {
                {
                    \tempo 4=60
                    %%% \time 4/4 %%%
                    c'4
                    c'4
                    r4
                    r4
                }
            }

    ..  container:: example

        When ``discard_grace_rest`` is set to ``False``, grace rests are not
        discarded.

        >>> grace_handler = nauert.ConcatenatingGraceHandler(discard_grace_rest=False)
        >>> result = nauert.quantize(q_event_sequence, grace_handler=grace_handler)
        >>> abjad.show(result) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(result)
            >>> print(string)
            \new Voice
            {
                {
                    \tempo 4=60
                    %%% \time 4/4 %%%
                    c'4
                    \grace {
                        r16
                    }
                    c'4
                    r4
                    r4
                }
            }

    ..  container:: example

        When ``replace_rest_with_final_grace_note`` is set to ``False``, grace
        notes are allowed to be attached to a rest.

        >>> durations = [1000, 1, 999, 1000]
        >>> pitches = [0, 0, None, 0]
        >>> q_event_sequence = nauert.QEventSequence.from_millisecond_pitch_pairs(
        ...     tuple(zip(durations, pitches))
        ... )
        >>> grace_handler = nauert.ConcatenatingGraceHandler(
        ...     replace_rest_with_final_grace_note=False
        ... )
        >>> result = nauert.quantize(
        ...     q_event_sequence, grace_handler=grace_handler
        ... )
        >>> abjad.show(result) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(result)
            >>> print(string)
            \new Voice
            {
                {
                    \tempo 4=60
                    %%% \time 4/4 %%%
                    c'4
                    \grace {
                        c'16
                    }
                    r4
                    c'4
                    r4
                }
            }

    ..  container:: example

        When ``replace_rest_with_final_grace_note`` is set to ``True`` (the
        default behavior), any rest with grace notes attached to it is replaced
        by the last pitched grace note in the grace container.

        >>> grace_handler = nauert.ConcatenatingGraceHandler()
        >>> result = nauert.quantize(q_event_sequence, grace_handler=grace_handler)
        >>> abjad.show(result) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(result)
            >>> print(string)
            \new Voice
            {
                {
                    \tempo 4=60
                    %%% \time 4/4 %%%
                    c'4
                    c'4
                    c'4
                    r4
                }
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_discard_grace_rest",
        "_grace_duration",
        "_replace_rest_with_final_grace_note",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        discard_grace_rest: bool = True,
        grace_duration: abjad.typings.Duration | None = None,
        replace_rest_with_final_grace_note: bool = True,
    ):
        self._discard_grace_rest = discard_grace_rest
        if grace_duration is None:
            grace_duration = (1, 16)
        grace_duration = abjad.Duration(grace_duration)
        assert grace_duration.is_dyadic_rational
        self._grace_duration = grace_duration
        self._replace_rest_with_final_grace_note = replace_rest_with_final_grace_note

    ### SPECIAL METHODS ###

    def __call__(
        self, q_events: typing.Sequence[QEvent]
    ) -> tuple[
        tuple[abjad.NamedPitch, ...],
        typing.Optional[tuple],
        typing.Optional[abjad.BeforeGraceContainer],
    ]:
        """
        Calls concatenating grace handler.
        """
        grace_events, final_event = q_events[:-1], q_events[-1]
        attachments: tuple | None
        if grace_events and self._replace_rest_with_final_grace_note:
            index = self._find_last_pitched_q_event(q_events)
            grace_events, final_event = q_events[:index], q_events[index]

        if isinstance(final_event, PitchedQEvent):
            # TODO: we are only supporting preserving attachments for PitchedQEvent
            pitches = final_event.pitches
            attachments = final_event.attachments
        else:
            pitches = ()
            attachments = None

        grace_events_list = list(grace_events)
        if self._discard_grace_rest:
            for q_event in grace_events_list:
                if isinstance(q_event, SilentQEvent):
                    grace_events_list.remove(q_event)
        grace_events = tuple(grace_events_list)

        grace_container: abjad.BeforeGraceContainer | None
        if grace_events:
            grace_container = abjad.BeforeGraceContainer()
            for q_event in grace_events:
                leaf: abjad.Leaf
                if isinstance(q_event, PitchedQEvent):
                    if len(q_event.pitches) == 1:
                        leaf = abjad.Note(q_event.pitches[0], self.grace_duration)
                    else:
                        leaf = abjad.Chord(q_event.pitches, self.grace_duration)
                else:
                    leaf = abjad.Rest(self.grace_duration)
                q_event_attachments = (
                    None if not hasattr(q_event, "attachments") else q_event.attachments
                )
                # assert hasattr(q_event, "attachments")
                # q_event_attachments = q_event.attachments
                if q_event_attachments is not None:
                    abjad.annotate(leaf, "q_event_attachments", q_event_attachments)
                grace_container.append(leaf)
        else:
            grace_container = None

        return tuple(pitches), attachments, grace_container

    ### PRIVATE METHODS ###

    @staticmethod
    def _find_last_pitched_q_event(q_events: typing.Sequence[QEvent]) -> int:
        for index, q_event in enumerate(reversed(q_events)):
            if isinstance(q_event, PitchedQEvent):
                return len(q_events) - index - 1
        message = "There should be at least one PitchedQEvent in q_events"
        raise ValueError(message)

    ### PUBLIC METHODS ###

    def handle_orphaned_q_event_proxies(self, last_leaf, q_event_proxies):
        r"""
        Embeds orphaned ``QEvents`` into an ``AfterGraceContainer`` and
        attaches it to the last leaf.

        ..  container:: example

            >>> durations = [1000, 1000, 1000, 400, 50, 50]
            >>> pitches = range(len(durations))
            >>> q_event_sequence = nauert.QEventSequence.from_millisecond_pitch_pairs(
            ...     tuple(zip(durations, pitches))
            ... )
            >>> search_tree = nauert.UnweightedSearchTree()
            >>> attack_point_optimizer = nauert.MeasurewiseAttackPointOptimizer()
            >>> q_schema = nauert.MeasurewiseQSchema(
            ...     search_tree=search_tree, time_signature=(7, 8), use_full_measure=True
            ... )
            >>> result = nauert.quantize(
            ...     q_event_sequence,
            ...     q_schema=q_schema,
            ...     attach_tempos=True,
            ...     attack_point_optimizer=attack_point_optimizer,
            ... )
            >>> staff = abjad.Staff([result])
            >>> score = abjad.Score([staff], name="Score")
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \new Voice
                    {
                        {
                            \tempo 4=60
                            \time 7/8
                            c'4
                            cs'8
                            ~
                            cs'8
                            d'8
                            ~
                            d'8
                            \afterGrace
                            ef'8
                            {
                                e'16
                                f'16
                            }
                        }
                    }
                }

        """
        grace_container = abjad.AfterGraceContainer() if q_event_proxies else None
        for proxy in q_event_proxies:
            q_event = proxy.q_event
            if isinstance(q_event, PitchedQEvent):
                if len(q_event.pitches) == 1:
                    leaf = abjad.Note(q_event.pitches[0], self.grace_duration)
                else:
                    leaf = abjad.Chord(q_event.pitches, self.grace_duration)
                abjad.annotate(leaf, "q_event_attachments", q_event.attachments)
                assert grace_container is not None
                grace_container.append(leaf)
        if grace_container:  # TODO: check if the grace_container is empty?
            abjad.attach(grace_container, last_leaf)

    ### PUBLIC PROPERTIES ###

    @property
    def discard_grace_rest(self) -> bool:
        """
        Boolean of whether to discard grace rests or not.
        """
        return self._discard_grace_rest

    @property
    def grace_duration(self) -> abjad.Duration:
        """
        Grace duration of concantenating grace handler.
        """
        return self._grace_duration

    @property
    def replace_rest_with_final_grace_note(self) -> bool:
        """
        Boolean of whether to replace the rest with the final (pitched) grace
        note.
        """
        return self._replace_rest_with_final_grace_note


class DiscardingGraceHandler(GraceHandler):
    r"""
    Discarding grace-handler.

    Discards all but final q-event attached to an offset.

    Does not create grace containers.

    ..  container:: example

        >>> durations = [1000, 1, 999]
        >>> pitches = [0, 0, 1]
        >>> q_event_sequence = nauert.QEventSequence.from_millisecond_pitch_pairs(
        ...     tuple(zip(durations, pitches))
        ... )
        >>> grace_handler = nauert.DiscardingGraceHandler()
        >>> result = nauert.quantize(
        ...     q_event_sequence, grace_handler=grace_handler
        ... )
        >>> abjad.show(result) # doctest: +SKIP

        ..  docs::

            >>> print(abjad.lilypond(result))
            \new Voice
            {
                {
                    \tempo 4=60
                    %%% \time 4/4 %%%
                    c'4
                    cs'4
                    r4
                    r4
                }
            }

        >>> grace_handler.discarded_q_events
        [[(PitchedQEvent(offset=Offset((1000, 1)), pitches=(NamedPitch("c'"),), index=None, attachments=()),)]]

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_discarded_q_events",)

    ### INITIALIZER ###

    def __init__(self):
        self._discarded_q_events: [QEvent] = []

    ### SPECIAL METHODS ###

    def __call__(
        self, q_events: typing.Sequence[QEvent]
    ) -> tuple[tuple[abjad.NamedPitch, ...], tuple, None]:
        """
        Calls discarding grace handler.
        """
        if q_events[:-1]:
            self._discarded_q_events.append([q_events[:-1]])
        q_event = q_events[-1]
        if isinstance(q_event, PitchedQEvent):
            return tuple(q_event.pitches), tuple(q_event.attachments), None
        return (), (), None

    @property
    def discarded_q_events(self):
        """
        Returns the discarded QEvents.
        """
        return self._discarded_q_events
