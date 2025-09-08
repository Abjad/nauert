import abjad

import nauert


def test_QGrid_distance_01():
    q_grid = nauert.QGrid()
    assert q_grid.distance is None

    a = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.duration.offset(0), ["A"]),
        abjad.duration.offset(0),
    )
    q_grid.fit_q_events([a])
    assert q_grid.distance == abjad.duration.offset(0).duration()

    b = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.duration.offset(1, 20), ["B"]),
        abjad.duration.offset(1, 20),
    )
    q_grid.fit_q_events([b])
    assert q_grid.distance == abjad.duration.offset(1, 40).duration()

    c = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.duration.offset(9, 20), ["C"]),
        abjad.duration.offset(9, 20),
    )
    q_grid.fit_q_events([c])
    assert q_grid.distance == abjad.duration.offset(1, 6).duration()

    d = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.duration.offset(1, 2), ["D"]),
        abjad.duration.offset(1, 2),
    )
    q_grid.fit_q_events([d])
    assert q_grid.distance == abjad.duration.offset(1, 4).duration()

    e = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.duration.offset(11, 20), ["E"]),
        abjad.duration.offset(11, 20),
    )
    q_grid.fit_q_events([e])
    assert q_grid.distance == abjad.duration.offset(29, 100).duration()

    f = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.duration.offset(19, 20), ["F"]),
        abjad.duration.offset(19, 20),
    )
    q_grid.fit_q_events([f])
    assert q_grid.distance == abjad.duration.offset(1, 4).duration()

    g = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.duration.offset(1), ["G"]),
        abjad.duration.offset(1),
    )
    q_grid.fit_q_events([g])
    assert q_grid.distance == abjad.duration.offset(3, 14).duration()

    q_events = q_grid.subdivide_leaves([(0, (1, 1))])
    q_grid.fit_q_events(q_events)

    assert q_grid.distance == abjad.duration.offset(1, 35).duration()
