import abjad

import nauert


def test_QGrid_subdivide_leaf_01():
    q_grid = nauert.QGrid()
    a = nauert.QEventProxy(
        nauert.PitchedQEvent(abjad.duration.offset(0), [0]),
        abjad.duration.offset(0),
    )
    b = nauert.QEventProxy(
        nauert.PitchedQEvent(abjad.duration.offset(9, 20), [1]),
        abjad.duration.offset(9, 20),
    )
    c = nauert.QEventProxy(
        nauert.PitchedQEvent(abjad.duration.offset(1, 2), [2]),
        abjad.duration.offset(1, 2),
    )
    d = nauert.QEventProxy(
        nauert.PitchedQEvent(abjad.duration.offset(11, 20), [3]),
        abjad.duration.offset(11, 20),
    )
    e = nauert.QEventProxy(
        nauert.PitchedQEvent(abjad.duration.offset(1), [4]),
        abjad.duration.offset(1),
    )
    q_grid.leaves[0].q_event_proxies.extend([a, b, c, d])
    q_grid.leaves[1].q_event_proxies.append(e)
    result = q_grid.subdivide_leaf(q_grid.leaves[0], (2, 3))
    assert result == [a, b, c, d]

    root_node = nauert.QGridContainer(
        (1, 1),
        children=[
            nauert.QGridLeaf(
                preprolated_duration=abjad.ValueDuration(2, 1), q_event_proxies=[]
            ),
            nauert.QGridLeaf(
                preprolated_duration=abjad.ValueDuration(3, 1), q_event_proxies=[]
            ),
        ],
    )
    assert format(q_grid.root_node) == format(root_node)
