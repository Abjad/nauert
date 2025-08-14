import abjad

import nauert


def test_UnweightedSearchTree__find_divisible_leaf_indices_and_subdivisions_01():
    definition = {2: {2: {2: None}, 3: None}, 5: None}
    search_tree = nauert.UnweightedSearchTree(definition)
    q_grid = nauert.QGrid()
    a = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.duration.offset(0), ["A"]),
        abjad.duration.offset(0),
        abjad.duration.offset(1),
    )
    b = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.duration.offset(1, 5), ["B"]),
        abjad.duration.offset(0),
        abjad.duration.offset(1),
    )
    c = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.duration.offset(1, 4), ["C"]),
        abjad.duration.offset(0),
        abjad.duration.offset(1),
    )
    d = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.duration.offset(1, 3), ["D"]),
        abjad.duration.offset(0),
        abjad.duration.offset(1),
    )
    e = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.duration.offset(2, 5), ["E"]),
        abjad.duration.offset(0),
        abjad.duration.offset(1),
    )
    f = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.duration.offset(1, 2), ["F"]),
        abjad.duration.offset(0),
        abjad.duration.offset(1),
    )
    g = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.duration.offset(3, 5), ["G"]),
        abjad.duration.offset(0),
        abjad.duration.offset(1),
    )
    h = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.duration.offset(2, 3), ["H"]),
        abjad.duration.offset(0),
        abjad.duration.offset(1),
    )
    i = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.duration.offset(3, 4), ["I"]),
        abjad.duration.offset(0),
        abjad.duration.offset(1),
    )
    j = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.duration.offset(4, 5), ["J"]),
        abjad.duration.offset(0),
        abjad.duration.offset(1),
    )
    k = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.duration.offset(1), ["K"]),
        abjad.duration.offset(0),
        abjad.duration.offset(1),
    )
    q_grid.fit_q_events([a, b, c, d, e, f, g, h, i, j, k])
    indices, subdivisions = search_tree._find_divisible_leaf_indices_and_subdivisions(
        q_grid
    )
    assert indices == [0]
    assert subdivisions == [((1, 1), (1, 1, 1, 1, 1))]
