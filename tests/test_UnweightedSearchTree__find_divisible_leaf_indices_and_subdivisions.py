import abjad

import nauert


def test_UnweightedSearchTree__find_divisible_leaf_indices_and_subdivisions_01():
    definition = {2: {2: {2: None}, 3: None}, 5: None}
    search_tree = nauert.UnweightedSearchTree(definition)
    q_grid = nauert.QGrid()
    a = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.mvo(0), ["A"]),
        abjad.mvo(0),
        abjad.mvo(1),
    )
    b = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.mvo(1, 5), ["B"]),
        abjad.mvo(0),
        abjad.mvo(1),
    )
    c = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.mvo(1, 4), ["C"]),
        abjad.mvo(0),
        abjad.mvo(1),
    )
    d = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.mvo(1, 3), ["D"]),
        abjad.mvo(0),
        abjad.mvo(1),
    )
    e = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.mvo(2, 5), ["E"]),
        abjad.mvo(0),
        abjad.mvo(1),
    )
    f = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.mvo(1, 2), ["F"]),
        abjad.mvo(0),
        abjad.mvo(1),
    )
    g = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.mvo(3, 5), ["G"]),
        abjad.mvo(0),
        abjad.mvo(1),
    )
    h = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.mvo(2, 3), ["H"]),
        abjad.mvo(0),
        abjad.mvo(1),
    )
    i = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.mvo(3, 4), ["I"]),
        abjad.mvo(0),
        abjad.mvo(1),
    )
    j = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.mvo(4, 5), ["J"]),
        abjad.mvo(0),
        abjad.mvo(1),
    )
    k = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.mvo(1), ["K"]),
        abjad.mvo(0),
        abjad.mvo(1),
    )
    q_grid.fit_q_events([a, b, c, d, e, f, g, h, i, j, k])
    indices, subdivisions = search_tree._find_divisible_leaf_indices_and_subdivisions(
        q_grid
    )
    assert indices == [0]
    assert subdivisions == [((1, 1), (1, 1, 1, 1, 1))]
