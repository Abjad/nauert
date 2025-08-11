import abjad

import nauert


def test_WeightedSearchTree___call___01():
    definition = {"divisors": (2, 3, 5, 7), "max_depth": 3, "max_divisions": 2}
    search_tree = nauert.WeightedSearchTree(definition)
    q_grid = nauert.QGrid()
    a = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(0).value_offset(), ["A"], index=1),
        abjad.Offset(0).value_offset(),
        abjad.Offset(1).value_offset(),
    )
    b = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(1, 5).value_offset(), ["B"], index=2),
        abjad.Offset(0).value_offset(),
        abjad.Offset(1).value_offset(),
    )
    c = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(1, 4).value_offset(), ["C"], index=3),
        abjad.Offset(0).value_offset(),
        abjad.Offset(1).value_offset(),
    )
    d = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(1, 3).value_offset(), ["D"], index=4),
        abjad.Offset(0).value_offset(),
        abjad.Offset(1).value_offset(),
    )
    e = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(2, 5).value_offset(), ["E"], index=5),
        abjad.Offset(0).value_offset(),
        abjad.Offset(1).value_offset(),
    )
    f = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(1, 2).value_offset(), ["F"], index=6),
        abjad.Offset(0).value_offset(),
        abjad.Offset(1).value_offset(),
    )
    g = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(3, 5).value_offset(), ["G"], index=7),
        abjad.Offset(0).value_offset(),
        abjad.Offset(1).value_offset(),
    )
    h = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(2, 3).value_offset(), ["H"], index=8),
        abjad.Offset(0).value_offset(),
        abjad.Offset(1).value_offset(),
    )
    i = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(3, 4).value_offset(), ["I"], index=9),
        abjad.Offset(0).value_offset(),
        abjad.Offset(1).value_offset(),
    )
    j = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(4, 5).value_offset(), ["J"], index=10),
        abjad.Offset(0).value_offset(),
        abjad.Offset(1).value_offset(),
    )
    k = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(1).value_offset(), ["K"], index=11),
        abjad.Offset(0).value_offset(),
        abjad.Offset(1).value_offset(),
    )
    q_grid.fit_q_events([a, b, c, d, e, f, g, h, i, j, k])
    q_grids = search_tree(q_grid)
    assert [q_grid.root_node.rtm_format() for q_grid in q_grids] == [
        "(1 (1 1))",
        "(1 (2 1))",
        "(1 (1 2))",
        "(1 (4 1))",
        "(1 (3 2))",
        "(1 (2 3))",
        "(1 (1 4))",
        "(1 (6 1))",
        "(1 (5 2))",
        "(1 (4 3))",
        "(1 (3 4))",
        "(1 (2 5))",
        "(1 (1 6))",
    ]
