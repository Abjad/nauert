import abjad

import nauert


def test_UnweightedSearchTree__find_divisible_leaf_indices_and_subdivisions_01():
    definition = {2: {2: {2: None}, 3: None}, 5: None}
    search_tree = nauert.UnweightedSearchTree(definition)
    q_grid = nauert.QGrid()
    a = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(0).value_offset(), ["A"]),
        abjad.Offset(0).value_offset(),
        abjad.Offset(1).value_offset(),
    )
    b = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(1, 5).value_offset(), ["B"]),
        abjad.Offset(0).value_offset(),
        abjad.Offset(1).value_offset(),
    )
    c = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(1, 4).value_offset(), ["C"]),
        abjad.Offset(0).value_offset(),
        abjad.Offset(1).value_offset(),
    )
    d = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(1, 3).value_offset(), ["D"]),
        abjad.Offset(0).value_offset(),
        abjad.Offset(1).value_offset(),
    )
    e = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(2, 5).value_offset(), ["E"]),
        abjad.Offset(0).value_offset(),
        abjad.Offset(1).value_offset(),
    )
    f = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(1, 2).value_offset(), ["F"]),
        abjad.Offset(0).value_offset(),
        abjad.Offset(1).value_offset(),
    )
    g = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(3, 5).value_offset(), ["G"]),
        abjad.Offset(0).value_offset(),
        abjad.Offset(1).value_offset(),
    )
    h = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(2, 3).value_offset(), ["H"]),
        abjad.Offset(0).value_offset(),
        abjad.Offset(1).value_offset(),
    )
    i = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(3, 4).value_offset(), ["I"]),
        abjad.Offset(0).value_offset(),
        abjad.Offset(1).value_offset(),
    )
    j = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(4, 5).value_offset(), ["J"]),
        abjad.Offset(0).value_offset(),
        abjad.Offset(1).value_offset(),
    )
    k = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(1).value_offset(), ["K"]),
        abjad.Offset(0).value_offset(),
        abjad.Offset(1).value_offset(),
    )
    q_grid.fit_q_events([a, b, c, d, e, f, g, h, i, j, k])
    indices, subdivisions = search_tree._find_divisible_leaf_indices_and_subdivisions(
        q_grid
    )
    assert indices == [0]
    assert subdivisions == [((1, 1), (1, 1, 1, 1, 1))]
