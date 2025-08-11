import abjad

import nauert


def test_QGrid_fit_q_events_01():
    q_grid = nauert.QGrid()
    a = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(0).value_offset(), ["A"]),
        abjad.Offset(0).value_offset(),
    )
    b = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(1, 20).value_offset(), ["B"]),
        abjad.Offset(1, 20).value_offset(),
    )
    c = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(9, 20).value_offset(), ["C"]),
        abjad.Offset(9, 20).value_offset(),
    )
    d = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(1, 2).value_offset(), ["D"]),
        abjad.Offset(1, 2).value_offset(),
    )
    e = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(11, 20).value_offset(), ["E"]),
        abjad.Offset(11, 20).value_offset(),
    )
    f = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(19, 20).value_offset(), ["F"]),
        abjad.Offset(19, 20).value_offset(),
    )
    g = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(1).value_offset(), ["G"]),
        abjad.Offset(1).value_offset(),
    )
    q_grid.fit_q_events([a, b, c, d, e, f, g])
    assert q_grid.leaves[0].q_event_proxies == [a, b, c, d]
    assert q_grid.leaves[1].q_event_proxies == [e, f, g]

    q_events = q_grid.subdivide_leaves([(0, (1, 1))])
    q_grid.fit_q_events(q_events)
    assert q_grid.leaves[0].q_event_proxies == [a, b]
    assert q_grid.leaves[1].q_event_proxies == [c, d, e]
    assert q_grid.leaves[2].q_event_proxies == [g, f]
