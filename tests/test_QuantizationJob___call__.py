import abjad

import nauert


def test_QuantizationJob___call___01():
    job_id = 1
    definition = {2: {2: {2: None}, 3: None}, 5: None}
    search_tree = nauert.UnweightedSearchTree(definition)
    q_event_proxies = [
        nauert.QEventProxy(
            nauert.SilentQEvent(abjad.Offset(0).value_offset(), ["A"], index=1),
            abjad.Offset(0).value_offset(),
            abjad.Offset(1).value_offset(),
        ),
        nauert.QEventProxy(
            nauert.SilentQEvent(abjad.Offset(1, 5).value_offset(), ["B"], index=2),
            abjad.Offset(0).value_offset(),
            abjad.Offset(1).value_offset(),
        ),
        nauert.QEventProxy(
            nauert.SilentQEvent(abjad.Offset(1, 4).value_offset(), ["C"], index=3),
            abjad.Offset(0).value_offset(),
            abjad.Offset(1).value_offset(),
        ),
        nauert.QEventProxy(
            nauert.SilentQEvent(abjad.Offset(1, 3).value_offset(), ["D"], index=4),
            abjad.Offset(0).value_offset(),
            abjad.Offset(1).value_offset(),
        ),
        nauert.QEventProxy(
            nauert.SilentQEvent(abjad.Offset(2, 5).value_offset(), ["E"], index=5),
            abjad.Offset(0).value_offset(),
            abjad.Offset(1).value_offset(),
        ),
        nauert.QEventProxy(
            nauert.SilentQEvent(abjad.Offset(1, 2).value_offset(), ["F"], index=6),
            abjad.Offset(0).value_offset(),
            abjad.Offset(1).value_offset(),
        ),
        nauert.QEventProxy(
            nauert.SilentQEvent(abjad.Offset(3, 5).value_offset(), ["G"], index=7),
            abjad.Offset(0).value_offset(),
            abjad.Offset(1).value_offset(),
        ),
        nauert.QEventProxy(
            nauert.SilentQEvent(abjad.Offset(2, 3).value_offset(), ["H"], index=8),
            abjad.Offset(0).value_offset(),
            abjad.Offset(1).value_offset(),
        ),
        nauert.QEventProxy(
            nauert.SilentQEvent(abjad.Offset(3, 4).value_offset(), ["I"], index=9),
            abjad.Offset(0).value_offset(),
            abjad.Offset(1).value_offset(),
        ),
        nauert.QEventProxy(
            nauert.SilentQEvent(abjad.Offset(4, 5).value_offset(), ["J"], index=10),
            abjad.Offset(0).value_offset(),
            abjad.Offset(1).value_offset(),
        ),
        nauert.QEventProxy(
            nauert.SilentQEvent(abjad.Offset(1).value_offset(), ["K"], index=11),
            abjad.Offset(0).value_offset(),
            abjad.Offset(1).value_offset(),
        ),
    ]
    job = nauert.QuantizationJob(job_id, search_tree, q_event_proxies)
    job()
    assert len(job.q_grids) == 10

    rtm_formats = [q_grid.root_node.rtm_format() for q_grid in job.q_grids]
    rtm_formats.sort(reverse=True)
    assert rtm_formats == [
        "1",
        "(1 (1 1))",
        "(1 (1 1 1 1 1))",
        "(1 ((1 (1 1)) (1 (1 1))))",
        "(1 ((1 (1 1)) (1 (1 1 1))))",
        "(1 ((1 (1 1 1)) (1 (1 1))))",
        "(1 ((1 (1 1 1)) (1 (1 1 1))))",
        "(1 ((1 (1 1 1)) (1 ((1 (1 1)) (1 (1 1))))))",
        "(1 ((1 ((1 (1 1)) (1 (1 1)))) (1 (1 1 1))))",
        "(1 ((1 ((1 (1 1)) (1 (1 1)))) (1 ((1 (1 1)) (1 (1 1))))))",
    ], rtm_formats
