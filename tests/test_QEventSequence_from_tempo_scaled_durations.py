import abjad

import nauert


def test_QEventSequence_from_tempo_scaled_durations_01():
    """
    Test basic functionality.
    """
    pairs = [(1, 4), (1, 3), (1, 7), (2, 5), (3, 4)]
    durations = abjad.duration.durations(pairs)
    tempo = abjad.MetronomeMark(abjad.Duration(1, 4), 55)
    q_events = nauert.QEventSequence.from_tempo_scaled_durations(durations, tempo)
    assert q_events == nauert.QEventSequence(
        (
            nauert.PitchedQEvent(abjad.mvo(0, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(12000, 11), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(28000, 11), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(244000, 77), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(34400, 7), (abjad.NamedPitch("c'"),)),
            nauert.TerminalQEvent(abjad.mvo(630400, 77)),
        )
    )


def test_QEventSequence_from_tempo_scaled_durations_02():
    """
    Silences are fused.
    """
    pairs = [(1, 4), (-1, 4), (1, 4), (1, 4), (-1, 4), (-1, 4), (1, 4)]
    durations = abjad.duration.durations(pairs)
    tempo = abjad.MetronomeMark(abjad.Duration(1, 4), 77)
    q_events = nauert.QEventSequence.from_tempo_scaled_durations(durations, tempo)
    assert q_events == nauert.QEventSequence(
        (
            nauert.PitchedQEvent(abjad.mvo(0, 1), (abjad.NamedPitch("c'"),)),
            nauert.SilentQEvent(abjad.mvo(60000, 77)),
            nauert.PitchedQEvent(abjad.mvo(120000, 77), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(180000, 77), (abjad.NamedPitch("c'"),)),
            nauert.SilentQEvent(abjad.mvo(240000, 77)),
            nauert.PitchedQEvent(abjad.mvo(360000, 77), (abjad.NamedPitch("c'"),)),
            nauert.TerminalQEvent(abjad.mvo(60000, 11)),
        )
    )
