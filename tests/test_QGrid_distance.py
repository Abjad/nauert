import abjad

import nauert


def test_QGrid_distance_01():
    q_grid = nauert.QGrid()
    assert q_grid.distance is None

    a = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(0).value_offset(), ["A"]),
        abjad.Offset(0).value_offset(),
    )
    q_grid.fit_q_events([a])
    assert q_grid.distance == abjad.Offset(0).value_offset().fraction

    b = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(1, 20).value_offset(), ["B"]),
        abjad.Offset(1, 20).value_offset(),
    )
    q_grid.fit_q_events([b])
    assert q_grid.distance == abjad.Offset(1, 40).value_offset().fraction

    c = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(9, 20).value_offset(), ["C"]),
        abjad.Offset(9, 20).value_offset(),
    )
    q_grid.fit_q_events([c])
    assert q_grid.distance == abjad.Offset(1, 6).value_offset().fraction

    d = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(1, 2).value_offset(), ["D"]),
        abjad.Offset(1, 2).value_offset(),
    )
    q_grid.fit_q_events([d])
    assert q_grid.distance == abjad.Offset(1, 4).value_offset().fraction

    e = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(11, 20).value_offset(), ["E"]),
        abjad.Offset(11, 20).value_offset(),
    )
    q_grid.fit_q_events([e])
    assert q_grid.distance == abjad.Offset(29, 100).value_offset().fraction

    f = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(19, 20).value_offset(), ["F"]),
        abjad.Offset(19, 20).value_offset(),
    )
    q_grid.fit_q_events([f])
    assert q_grid.distance == abjad.Offset(1, 4).value_offset().fraction

    g = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(1).value_offset(), ["G"]),
        abjad.Offset(1).value_offset(),
    )
    q_grid.fit_q_events([g])
    assert q_grid.distance == abjad.Offset(3, 14).value_offset().fraction

    q_events = q_grid.subdivide_leaves([(0, (1, 1))])
    q_grid.fit_q_events(q_events)

    assert q_grid.distance == abjad.Offset(1, 35).value_offset().fraction
