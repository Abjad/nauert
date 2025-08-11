import abjad

import nauert


def test_QGrid_subdivide_leaf_01():
    q_grid = nauert.QGrid()
    a = nauert.QEventProxy(
        nauert.PitchedQEvent(abjad.Offset(0).value_offset(), [0]),
        abjad.Offset(0).value_offset(),
    )
    b = nauert.QEventProxy(
        nauert.PitchedQEvent(abjad.Offset(9, 20).value_offset(), [1]),
        abjad.Offset(9, 20).value_offset(),
    )
    c = nauert.QEventProxy(
        nauert.PitchedQEvent(abjad.Offset(1, 2).value_offset(), [2]),
        abjad.Offset(1, 2).value_offset(),
    )
    d = nauert.QEventProxy(
        nauert.PitchedQEvent(abjad.Offset(11, 20).value_offset(), [3]),
        abjad.Offset(11, 20).value_offset(),
    )
    e = nauert.QEventProxy(
        nauert.PitchedQEvent(abjad.Offset(1).value_offset(), [4]),
        abjad.Offset(1).value_offset(),
    )
    q_grid.leaves[0].q_event_proxies.extend([a, b, c, d])
    q_grid.leaves[1].q_event_proxies.append(e)
    result = q_grid.subdivide_leaf(q_grid.leaves[0], (2, 3))
    assert result == [a, b, c, d]

    root_node = nauert.QGridContainer(
        (1, 1),
        children=[
            nauert.QGridLeaf(
                preprolated_duration=abjad.Duration(2, 1), q_event_proxies=[]
            ),
            nauert.QGridLeaf(
                preprolated_duration=abjad.Duration(3, 1), q_event_proxies=[]
            ),
        ],
    )
    assert format(q_grid.root_node) == format(root_node)
