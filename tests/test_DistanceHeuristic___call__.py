import abjad

import nauert


def test_DistanceHeuristic___call___01():
    heuristic = nauert.DistanceHeuristic()
    q_event_a = nauert.PitchedQEvent(abjad.duration.offset(250), [0, 1])
    q_event_b = nauert.SilentQEvent(abjad.duration.offset(500))
    q_event_c = nauert.PitchedQEvent(abjad.duration.offset(750), [3, 7])
    proxy_a = nauert.QEventProxy(q_event_a, abjad.duration.offset(1, 4))
    proxy_b = nauert.QEventProxy(q_event_b, abjad.duration.offset(1, 2))
    proxy_c = nauert.QEventProxy(q_event_c, abjad.duration.offset(3, 4))
    definition = {2: {2: None}, 3: None, 5: None}
    search_tree = nauert.UnweightedSearchTree(definition)
    job = nauert.QuantizationJob(1, search_tree, [proxy_a, proxy_b, proxy_c])
    job()
    q_target_beat = nauert.QTargetBeat()
    q_target_beat._q_grids = job.q_grids
    q_target_beats = heuristic((q_target_beat,))
    q_target_beat = q_target_beats[0]
    q_grid = q_target_beat.q_grid
    assert q_grid.distance == abjad.ValueDuration(0)
    rtm = q_grid.rtm_format()
    assert rtm == "(1 ((1 (1 1)) (1 (1 1))))"


def test_DistanceHeuristic___call___02():
    heuristic = nauert.DistanceHeuristic()
    q_event_a = nauert.PitchedQEvent(abjad.duration.offset(250), [0, 1])
    q_event_b = nauert.SilentQEvent(abjad.duration.offset(500))
    q_event_c = nauert.PitchedQEvent(abjad.duration.offset(750), [3, 7])
    proxy_a = nauert.QEventProxy(q_event_a, abjad.duration.offset(1, 4))
    proxy_b = nauert.QEventProxy(q_event_b, abjad.duration.offset(1, 2))
    proxy_c = nauert.QEventProxy(q_event_c, abjad.duration.offset(3, 4))
    definition = {2: None, 3: None, 5: None}
    search_tree = nauert.UnweightedSearchTree(definition)
    job = nauert.QuantizationJob(1, search_tree, [proxy_a, proxy_b, proxy_c])
    job()
    q_target_beat = nauert.QTargetBeat()
    q_target_beat._q_grids = job.q_grids
    q_target_beats = heuristic((q_target_beat,))
    q_target_beat = q_target_beats[0]
    q_grid = q_target_beat.q_grid
    assert q_grid.distance == abjad.ValueDuration(1, 15)
    rtm = q_grid.rtm_format()
    assert rtm == "(1 (1 1 1 1 1))"
