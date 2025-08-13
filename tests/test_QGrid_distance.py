import abjad

import nauert


def test_QGrid_distance_01():
    q_grid = nauert.QGrid()
    assert q_grid.distance is None

    a = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.mvo(0), ["A"]),
        abjad.mvo(0),
    )
    q_grid.fit_q_events([a])
    assert q_grid.distance == abjad.mvo(0).fraction

    b = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.mvo(1, 20), ["B"]),
        abjad.mvo(1, 20),
    )
    q_grid.fit_q_events([b])
    assert q_grid.distance == abjad.mvo(1, 40).fraction

    c = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.mvo(9, 20), ["C"]),
        abjad.mvo(9, 20),
    )
    q_grid.fit_q_events([c])
    assert q_grid.distance == abjad.mvo(1, 6).fraction

    d = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.mvo(1, 2), ["D"]),
        abjad.mvo(1, 2),
    )
    q_grid.fit_q_events([d])
    assert q_grid.distance == abjad.mvo(1, 4).fraction

    e = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.mvo(11, 20), ["E"]),
        abjad.mvo(11, 20),
    )
    q_grid.fit_q_events([e])
    assert q_grid.distance == abjad.mvo(29, 100).fraction

    f = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.mvo(19, 20), ["F"]),
        abjad.mvo(19, 20),
    )
    q_grid.fit_q_events([f])
    assert q_grid.distance == abjad.mvo(1, 4).fraction

    g = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.mvo(1), ["G"]),
        abjad.mvo(1),
    )
    q_grid.fit_q_events([g])
    assert q_grid.distance == abjad.mvo(3, 14).fraction

    q_events = q_grid.subdivide_leaves([(0, (1, 1))])
    q_grid.fit_q_events(q_events)

    assert q_grid.distance == abjad.mvo(1, 35).fraction
