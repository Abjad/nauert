import abjad

import nauert


def test_QEventProxy___init___01():
    q_event = nauert.PitchedQEvent(abjad.Offset(130).value_offset(), [0])
    proxy = nauert.QEventProxy(q_event, abjad.Offset(0.5).value_offset())
    assert proxy.q_event == q_event
    assert proxy.value_offset() == abjad.Offset(1, 2).value_offset()


def test_QEventProxy___init___02():
    q_event = nauert.PitchedQEvent(abjad.Offset(130).value_offset(), [0, 1, 4])
    proxy = nauert.QEventProxy(
        q_event, abjad.Offset(100).value_offset(), abjad.Offset(1000).value_offset()
    )
    assert proxy.q_event == q_event
    assert proxy.value_offset() == abjad.Offset(1, 30).value_offset()
