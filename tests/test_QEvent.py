import decimal

import abjad
import pytest

import nauert


def test_PitchedQEvent___init___01():
    q_event = nauert.PitchedQEvent(abjad.mvo(130), [0, 1, 4])
    assert q_event.value_offset() == abjad.mvo(130)
    assert q_event.pitches == (
        abjad.NamedPitch(0),
        abjad.NamedPitch(1),
        abjad.NamedPitch(4),
    )
    assert q_event.attachments == ()


def test_PitchedQEvent___init___02():
    q_event = nauert.PitchedQEvent(
        abjad.mvo(133, 5),
        [abjad.NamedPitch("fss")],
        attachments=["foo", "bar", "baz"],
    )
    assert q_event.value_offset() == abjad.mvo(133, 5)
    assert q_event.pitches == (abjad.NamedPitch("fss"),)
    assert q_event.attachments == ("foo", "bar", "baz")


def test_PitchedQEvent___eq___01():
    a = nauert.PitchedQEvent(abjad.mvo(1000), [0])
    b = nauert.PitchedQEvent(abjad.mvo(1000), [0])
    assert a == b


def test_PitchedQEvent___eq___02():
    a = nauert.PitchedQEvent(abjad.mvo(1000), [0])
    b = nauert.PitchedQEvent(abjad.mvo(1000), [0], ["foo", "bar", "baz"])
    c = nauert.PitchedQEvent(abjad.mvo(9999), [0])
    d = nauert.PitchedQEvent(abjad.mvo(1000), [0, 1, 4])
    assert a != b
    assert a != c
    assert a != d


def test_PitchedQEvent___eq___03():
    a = nauert.TerminalQEvent(abjad.mvo(100))
    b = nauert.PitchedQEvent(abjad.mvo(100), [0])
    c = nauert.SilentQEvent(abjad.mvo(100))
    assert a != b
    assert a != c


def test_SilentQEvent___init___01():
    q_event = nauert.SilentQEvent(abjad.mvo(130))
    assert q_event.value_offset() == abjad.mvo(130)
    assert q_event.attachments == ()


def test_SilentQEvent___init___02():
    attachments = ["foo", "bar", "baz"]
    q_event = nauert.SilentQEvent(abjad.mvo(155, 7), attachments=attachments)
    assert q_event.value_offset() == abjad.mvo(155, 7)
    assert q_event.attachments == ("foo", "bar", "baz")


def test_SilentQEvent___eq___01():
    a = nauert.SilentQEvent(abjad.mvo(1000))
    b = nauert.SilentQEvent(abjad.mvo(1000))
    assert a == b


def test_SilentQEvent___eq___02():
    a = nauert.SilentQEvent(abjad.mvo(1000))
    b = nauert.SilentQEvent(abjad.mvo(1000), ["foo", "bar", "baz"])
    c = nauert.SilentQEvent(abjad.mvo(9999))
    assert a != b
    assert a != c


def test_TerminalQEvent___init___01():
    q_event = nauert.TerminalQEvent(abjad.mvo(154))
    assert q_event.value_offset() == abjad.mvo(154)


def test_TerminalQEvent___eq___01():
    a = nauert.TerminalQEvent(abjad.mvo(1000))
    b = nauert.TerminalQEvent(abjad.mvo(1000))
    assert a == b


def test_TerminalQEvent___eq___02():
    a = nauert.TerminalQEvent(abjad.mvo(1000))
    b = nauert.TerminalQEvent(abjad.mvo(9000))
    assert a != b


def test_TerminalQEvent___eq___03():
    a = nauert.TerminalQEvent(abjad.mvo(100))
    b = nauert.PitchedQEvent(abjad.mvo(100), [0])
    c = nauert.SilentQEvent(abjad.mvo(100))
    assert a != b
    assert a != c


def test_QEvent_from_offset_pitches_attachments():
    q_event = nauert.QEvent.from_offset_pitches_attachments(abjad.mvo(100), 1, ("foo",))
    assert isinstance(q_event, nauert.PitchedQEvent)
    assert q_event.value_offset().fraction == 100
    assert q_event.pitches == (abjad.NamedPitch(1),)
    assert q_event.attachments == ("foo",)


def test_QEvent_from_offset_pitches_attachments_with_incorrectly_typed_pitches():
    with pytest.raises(TypeError):
        nauert.QEvent.from_offset_pitches_attachments(
            abjad.ValueOffset(abjad.Fraction(100)), decimal.Decimal(0), ("foo",)
        )
