import abjad

import nauert


def test_QEventSequence_from_millisecond_pitch_pairs_01():
    durations = [100, 200, 100, 300, 350, 400, 600]
    pitches = [0, None, None, [1, 4], None, 5, 7]
    pairs = tuple(zip(durations, pitches))
    q_events = nauert.QEventSequence.from_millisecond_pitch_pairs(pairs)
    assert q_events == nauert.QEventSequence(
        (
            nauert.PitchedQEvent(abjad.mvo(0), (abjad.NamedPitch("c'"),)),
            nauert.SilentQEvent(abjad.mvo(100, 1)),
            nauert.PitchedQEvent(
                abjad.mvo(400, 1),
                (abjad.NamedPitch("cs'"), abjad.NamedPitch("e'")),
            ),
            nauert.SilentQEvent(abjad.mvo(700, 1)),
            nauert.PitchedQEvent(abjad.mvo(1050, 1), (abjad.NamedPitch("f'"),)),
            nauert.PitchedQEvent(abjad.mvo(1450, 1), (abjad.NamedPitch("g'"),)),
            nauert.TerminalQEvent(abjad.mvo(2050, 1)),
        )
    )
