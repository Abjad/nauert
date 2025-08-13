import abjad

import nauert

test_time_segments = [
    (116, 255),
    (279, 580),
    (627, 720),
    (743, 1300),
    (1324, 1509),
    (1533, 2090),
    (2113, 2833),
    (3320, 3390),
    (3413, 4087),
    (4203, 4389),
    (4412, 4807),
    (4946, 5898),
    (6478, 6687),
    (6711, 6780),
    (6803, 7082),
    (7129, 7314),
    (7361, 7918),
    (7988, 8290),
    (8313, 8452),
    (8475, 8731),
    (8754, 8824),
    (8847, 9009),
    (9033, 9172),
    (9404, 9474),
    (9520, 9961),
    (10356, 10449),
    (10472, 10588),
    (10612, 10960),
    (11006, 11262),
    (11285, 11378),
    (11401, 11517),
    (11540, 12237),
    (12423, 12957),
    (13073, 13166),
    (13189, 13700),
    (13769, 13862),
    (14095, 14234),
    (14350, 15279),
    (15372, 15952),
    (15999, 16091),
    (16138, 16324),
    (16765, 16997),
    (17043, 17136),
    (17160, 17345),
    (17392, 17578),
    (18599, 19342),
]


def test_QEventSequence_from_millisecond_durations_01():
    """
    Test basic functionality.
    """

    durations = abjad.math.difference_series([x[0] for x in test_time_segments])
    q_events = nauert.QEventSequence.from_millisecond_durations(durations)
    assert q_events == nauert.QEventSequence(
        (
            nauert.PitchedQEvent(abjad.mvo(0, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(163, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(511, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(627, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(1208, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(1417, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(1997, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(3204, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(3297, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(4087, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(4296, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(4830, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(6362, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(6595, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(6687, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(7013, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(7245, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(7872, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(8197, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(8359, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(8638, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(8731, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(8917, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(9288, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(9404, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(10240, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(10356, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(10496, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(10890, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(11169, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(11285, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(11424, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(12307, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(12957, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(13073, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(13653, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(13979, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(14234, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(15256, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(15883, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(16022, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(16649, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(16927, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(17044, 1), (abjad.NamedPitch("c'"),)),
            nauert.PitchedQEvent(abjad.mvo(17276, 1), (abjad.NamedPitch("c'"),)),
            nauert.TerminalQEvent(abjad.mvo(18483, 1)),
        )
    )


def test_QEventSequence_from_millisecond_durations_02():
    """
    Silences are not fused.
    """

    durations = [100, -100, 100, -100, -100, 100]
    q_events = nauert.QEventSequence.from_millisecond_durations(
        durations, fuse_silences=False
    )
    assert q_events == nauert.QEventSequence(
        (
            nauert.PitchedQEvent(abjad.mvo(0), (abjad.NamedPitch("c'"),)),
            nauert.SilentQEvent(abjad.mvo(100)),
            nauert.PitchedQEvent(abjad.mvo(200), (abjad.NamedPitch("c'"),)),
            nauert.SilentQEvent(abjad.mvo(300)),
            nauert.SilentQEvent(abjad.mvo(400)),
            nauert.PitchedQEvent(abjad.mvo(500), (abjad.NamedPitch("c'"),)),
            nauert.TerminalQEvent(abjad.mvo(600)),
        )
    )


def test_QEventSequence_from_millisecond_durations_03():
    """
    Silences are fused.
    """

    durations = [100, -100, 100, -100, -100, 100]
    q_events = nauert.QEventSequence.from_millisecond_durations(
        durations, fuse_silences=True
    )
    assert q_events == nauert.QEventSequence(
        (
            nauert.PitchedQEvent(abjad.mvo(0), (abjad.NamedPitch("c'"),)),
            nauert.SilentQEvent(abjad.mvo(100)),
            nauert.PitchedQEvent(abjad.mvo(200), (abjad.NamedPitch("c'"),)),
            nauert.SilentQEvent(abjad.mvo(300)),
            nauert.PitchedQEvent(abjad.mvo(500), (abjad.NamedPitch("c'"),)),
            nauert.TerminalQEvent(abjad.mvo(600)),
        )
    )
