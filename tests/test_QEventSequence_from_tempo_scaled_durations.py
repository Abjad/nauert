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
            nauert.PitchedQEvent(
                abjad.Offset(0, 1).value_offset(), (abjad.NamedPitch("c'"),)
            ),
            nauert.PitchedQEvent(
                abjad.Offset(12000, 11).value_offset(), (abjad.NamedPitch("c'"),)
            ),
            nauert.PitchedQEvent(
                abjad.Offset(28000, 11).value_offset(), (abjad.NamedPitch("c'"),)
            ),
            nauert.PitchedQEvent(
                abjad.Offset(244000, 77).value_offset(), (abjad.NamedPitch("c'"),)
            ),
            nauert.PitchedQEvent(
                abjad.Offset(34400, 7).value_offset(), (abjad.NamedPitch("c'"),)
            ),
            nauert.TerminalQEvent(abjad.Offset(630400, 77).value_offset()),
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
            nauert.PitchedQEvent(
                abjad.Offset(0, 1).value_offset(), (abjad.NamedPitch("c'"),)
            ),
            nauert.SilentQEvent(abjad.Offset(60000, 77).value_offset()),
            nauert.PitchedQEvent(
                abjad.Offset(120000, 77).value_offset(), (abjad.NamedPitch("c'"),)
            ),
            nauert.PitchedQEvent(
                abjad.Offset(180000, 77).value_offset(), (abjad.NamedPitch("c'"),)
            ),
            nauert.SilentQEvent(abjad.Offset(240000, 77).value_offset()),
            nauert.PitchedQEvent(
                abjad.Offset(360000, 77).value_offset(), (abjad.NamedPitch("c'"),)
            ),
            nauert.TerminalQEvent(abjad.Offset(60000, 11).value_offset()),
        )
    )
