import abjad

import nauert


def test_QGrid___eq___01():
    a = nauert.QGrid()
    b = nauert.QGrid()
    assert format(a) == format(b)
    assert a != b


def test_QGrid___eq___02():
    a = nauert.QGrid(
        root_node=nauert.QGridContainer(
            (1, 1),
            children=[
                nauert.QGridLeaf(
                    preprolated_duration=abjad.Duration(1, 1),
                    q_event_proxies=[
                        nauert.QEventProxy(
                            nauert.SilentQEvent(abjad.Offset(100).value_offset()),
                            abjad.Offset(0.5).value_offset(),
                        )
                    ],
                )
            ],
        ),
        next_downbeat=nauert.QGridLeaf(
            preprolated_duration=abjad.Duration(1, 1),
            q_event_proxies=[
                nauert.QEventProxy(
                    nauert.TerminalQEvent(abjad.Offset(200).value_offset()),
                    abjad.Offset(0.9).value_offset(),
                )
            ],
        ),
    )
    b = nauert.QGrid(
        root_node=nauert.QGridContainer(
            (1, 1),
            children=[
                nauert.QGridLeaf(
                    preprolated_duration=abjad.Duration(1, 1),
                    q_event_proxies=[
                        nauert.QEventProxy(
                            nauert.SilentQEvent(abjad.Offset(100).value_offset()),
                            abjad.Offset(0.5).value_offset(),
                        )
                    ],
                )
            ],
        ),
        next_downbeat=nauert.QGridLeaf(
            preprolated_duration=abjad.Duration(1, 1),
            q_event_proxies=[
                nauert.QEventProxy(
                    nauert.TerminalQEvent(abjad.Offset(200).value_offset()),
                    abjad.Offset(0.9).value_offset(),
                )
            ],
        ),
    )
    assert format(a) == format(b)
    assert a != b


def test_QGrid___eq___03():
    a = nauert.QGrid()
    b = nauert.QGrid(
        root_node=nauert.QGridContainer(
            (1, 1),
            children=[
                nauert.QGridLeaf(
                    preprolated_duration=abjad.Duration(1, 1),
                    q_event_proxies=[
                        nauert.QEventProxy(
                            nauert.SilentQEvent(abjad.Offset(100).value_offset()),
                            abjad.Offset(0.5).value_offset(),
                        )
                    ],
                )
            ],
        )
    )
    c = nauert.QGrid(
        next_downbeat=nauert.QGridLeaf(
            preprolated_duration=abjad.Duration(1, 1),
            q_event_proxies=[
                nauert.QEventProxy(
                    nauert.TerminalQEvent(abjad.Offset(200).value_offset()),
                    abjad.Offset(0.9).value_offset(),
                )
            ],
        )
    )
    d = (
        nauert.QGrid(
            root_node=nauert.QGridContainer(
                (1, 1),
                children=[
                    nauert.QGridLeaf(
                        preprolated_duration=abjad.Duration(1, 1),
                        q_event_proxies=[
                            nauert.QEventProxy(
                                nauert.SilentQEvent(abjad.Offset(100).value_offset()),
                                abjad.Offset(0.5).value_offset(),
                            )
                        ],
                    )
                ],
            ),
            next_downbeat=nauert.QGridLeaf(
                preprolated_duration=abjad.Duration(1, 1),
                q_event_proxies=[
                    nauert.QEventProxy(
                        nauert.TerminalQEvent(abjad.Offset(200).value_offset()),
                        abjad.Offset(0.9).value_offset(),
                    )
                ],
            ),
        ),
    )
    assert a != b
    assert a != c
    assert a != d
    assert b != c
    assert b != d
    assert c != d
