import decimal

import abjad
import pytest

import nauert


def test_PitchedQEvent___init___01():
    q_event = nauert.PitchedQEvent(abjad.Offset(130).value_offset(), [0, 1, 4])
    assert q_event.value_offset() == abjad.Offset(130).value_offset()
    assert q_event.pitches == (
        abjad.NamedPitch(0),
        abjad.NamedPitch(1),
        abjad.NamedPitch(4),
    )
    assert q_event.attachments == ()


def test_PitchedQEvent___init___02():
    q_event = nauert.PitchedQEvent(
        abjad.Offset(133, 5).value_offset(),
        [abjad.NamedPitch("fss")],
        attachments=["foo", "bar", "baz"],
    )
    assert q_event.value_offset() == abjad.Offset(133, 5).value_offset()
    assert q_event.pitches == (abjad.NamedPitch("fss"),)
    assert q_event.attachments == ("foo", "bar", "baz")


def test_PitchedQEvent___eq___01():
    a = nauert.PitchedQEvent(abjad.Offset(1000).value_offset(), [0])
    b = nauert.PitchedQEvent(abjad.Offset(1000).value_offset(), [0])
    assert a == b


def test_PitchedQEvent___eq___02():
    a = nauert.PitchedQEvent(abjad.Offset(1000).value_offset(), [0])
    b = nauert.PitchedQEvent(
        abjad.Offset(1000).value_offset(), [0], ["foo", "bar", "baz"]
    )
    c = nauert.PitchedQEvent(abjad.Offset(9999).value_offset(), [0])
    d = nauert.PitchedQEvent(abjad.Offset(1000).value_offset(), [0, 1, 4])
    assert a != b
    assert a != c
    assert a != d


def test_PitchedQEvent___eq___03():
    a = nauert.TerminalQEvent(abjad.Offset(100).value_offset())
    b = nauert.PitchedQEvent(abjad.Offset(100).value_offset(), [0])
    c = nauert.SilentQEvent(abjad.Offset(100).value_offset())
    assert a != b
    assert a != c


def test_SilentQEvent___init___01():
    q_event = nauert.SilentQEvent(abjad.Offset(130).value_offset())
    assert q_event.value_offset() == abjad.Offset(130).value_offset()
    assert q_event.attachments == ()


def test_SilentQEvent___init___02():
    attachments = ["foo", "bar", "baz"]
    q_event = nauert.SilentQEvent(
        abjad.Offset(155, 7).value_offset(), attachments=attachments
    )
    assert q_event.value_offset() == abjad.Offset(155, 7).value_offset()
    assert q_event.attachments == ("foo", "bar", "baz")


def test_SilentQEvent___eq___01():
    a = nauert.SilentQEvent(abjad.Offset(1000).value_offset())
    b = nauert.SilentQEvent(abjad.Offset(1000).value_offset())
    assert a == b


def test_SilentQEvent___eq___02():
    a = nauert.SilentQEvent(abjad.Offset(1000).value_offset())
    b = nauert.SilentQEvent(abjad.Offset(1000).value_offset(), ["foo", "bar", "baz"])
    c = nauert.SilentQEvent(abjad.Offset(9999).value_offset())
    assert a != b
    assert a != c


def test_TerminalQEvent___init___01():
    q_event = nauert.TerminalQEvent(abjad.Offset(154).value_offset())
    assert q_event.value_offset() == abjad.Offset(154).value_offset()


def test_TerminalQEvent___eq___01():
    a = nauert.TerminalQEvent(abjad.Offset(1000).value_offset())
    b = nauert.TerminalQEvent(abjad.Offset(1000).value_offset())
    assert a == b


def test_TerminalQEvent___eq___02():
    a = nauert.TerminalQEvent(abjad.Offset(1000).value_offset())
    b = nauert.TerminalQEvent(abjad.Offset(9000).value_offset())
    assert a != b


def test_TerminalQEvent___eq___03():
    a = nauert.TerminalQEvent(abjad.Offset(100).value_offset())
    b = nauert.PitchedQEvent(abjad.Offset(100).value_offset(), [0])
    c = nauert.SilentQEvent(abjad.Offset(100).value_offset())
    assert a != b
    assert a != c


def test_QEvent_from_offset_pitches_attachments():
    q_event = nauert.QEvent.from_offset_pitches_attachments(
        abjad.Offset(100).value_offset(), 1, ("foo",)
    )
    assert isinstance(q_event, nauert.PitchedQEvent)
    assert q_event.value_offset().fraction == 100
    assert q_event.pitches == (abjad.NamedPitch(1),)
    assert q_event.attachments == ("foo",)


def test_QEvent_from_offset_pitches_attachments_with_incorrectly_typed_pitches():
    with pytest.raises(TypeError):
        nauert.QEvent.from_offset_pitches_attachments(
            abjad.ValueOffset(abjad.Fraction(100)), decimal.Decimal(0), ("foo",)
        )
