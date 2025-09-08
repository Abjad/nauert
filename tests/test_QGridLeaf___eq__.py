import abjad

import nauert


def test_QGridLeaf___eq___01():
    a = nauert.QGridLeaf(abjad.ValueDuration(1), [])
    b = nauert.QGridLeaf(abjad.ValueDuration(1), [])
    assert format(a) == format(b)
    assert a != b


def test_QGridLeaf___eq___02():
    a = nauert.QGridLeaf(abjad.ValueDuration(1), [])
    sqe = nauert.SilentQEvent(abjad.duration.offset(1000))
    b = nauert.QGridLeaf(
        abjad.ValueDuration(1),
        [nauert.QEventProxy(sqe, abjad.duration.offset(1, 2))],
    )
    c = nauert.QGridLeaf(abjad.ValueDuration(2), [])
    d = nauert.QGridLeaf(
        abjad.ValueDuration(2),
        [nauert.QEventProxy(sqe, abjad.duration.offset(1, 2))],
    )
    assert a != b
    assert a != c
    assert a != d
    assert b != c
    assert b != d
    assert c != d
