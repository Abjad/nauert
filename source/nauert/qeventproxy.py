import typing

import abjad

from . import qevents as _qevents


class QEventProxy:
    """
    Q-event proxy.

    Maps Q-event offset with the range of its beatspan to the range 0-1.

    ..  container:: example

        >>> q_event = nauert.PitchedQEvent(abjad.Offset(130).value_offset(), [0, 1, 4])
        >>> nauert.QEventProxy(q_event, abjad.Offset(0.5).value_offset())
        QEventProxy(q_event=PitchedQEvent(offset=ValueOffset(Fraction(130, 1)), pitches=(NamedPitch("c'"), NamedPitch("cs'"), NamedPitch("e'")), index=None, attachments=()), offset=ValueOffset(Fraction(1, 2)))

    Not composer-safe.

    Used internally by the ``quantize`` function.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_offset", "_q_event")

    ### INITIALIZER ###

    def __init__(
        self,
        q_event: _qevents.QEvent | None = None,
        *offsets: abjad.ValueOffset,
    ) -> None:
        assert all(isinstance(_, abjad.ValueOffset) for _ in offsets), repr(offsets)
        if len(offsets) == 1:
            offset = abjad.ValueOffset(offsets[0].fraction)
            assert isinstance(q_event, _qevents.QEvent)
            assert 0 <= offset.fraction <= 1
        elif len(offsets) == 2:
            minimum, maximum = (
                abjad.ValueOffset(offsets[0].fraction),
                abjad.ValueOffset(offsets[1].fraction),
            )
            assert isinstance(q_event, _qevents.QEvent)
            assert minimum <= q_event.value_offset() <= maximum
            fraction = (q_event.value_offset() - minimum) / (maximum - minimum)
            offset = abjad.ValueOffset(fraction)
        elif len(offsets) == 0:
            assert q_event is None
            offset = abjad.ValueOffset(abjad.Fraction(0))
        else:
            message = f"can not initialize {type(self).__name__}: {offsets!r}."
            raise ValueError(message)
        self._q_event = q_event
        self._offset = abjad.ValueOffset(offset.fraction)

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when `argument` is a q-event proxy with offset and q-event
        equal to those of this q-event proxy. Otherwise false.
        """
        if type(self) is type(argument):
            if self.value_offset() == argument.value_offset():
                if self.q_event == argument.q_event:
                    return True
        return False

    def __hash__(self) -> int:
        """
        Hashes q-event proxy.

        Required to be explicitly redefined on Python 3 if __eq__ changes.
        """
        return super(QEventProxy, self).__hash__()

    def __repr__(self) -> str:
        """
        Gets repr.
        """
        class_name = type(self).__name__
        string = (
            f"{class_name}(q_event={self.q_event!r}, offset={self.value_offset()!r})"
        )
        return string

    ### PUBLIC PROPERTIES ###

    @property
    def index(self) -> typing.Optional[int]:
        """
        Gets index of q-event proxy.
        """
        assert self._q_event is not None, "There is no QEvent is this proxy."
        return self._q_event.index

    def value_offset(self) -> abjad.ValueOffset:
        """
        Gets offset of q-event proxy.
        """
        return self._offset

    @property
    def q_event(self) -> typing.Optional[_qevents.QEvent]:
        """
        Gets q-event of q-event proxy.
        """
        return self._q_event
