import abjad

from .BeatwiseQSchemaItem import BeatwiseQSchemaItem
from .BeatwiseQTarget import BeatwiseQTarget
from .QSchema import QSchema
from .QTargetBeat import QTargetBeat
from .SearchTree import SearchTree
from .UnweightedSearchTree import UnweightedSearchTree


class BeatwiseQSchema(QSchema):
    r"""
    Beatwise q-schema.

    Treats beats as timestep unit.

        >>> q_schema = abjadext.nauert.BeatwiseQSchema()

    ..  container:: example

        Without arguments, it uses smart defaults:

        >>> abjad.f(q_schema)
        abjadext.nauert.BeatwiseQSchema(
            beatspan=abjad.Duration(1, 4),
            search_tree=abjadext.nauert.UnweightedSearchTree(
                definition={
                    2: {
                        2: {
                            2: {
                                2: None,
                                },
                            3: None,
                            },
                        3: None,
                        5: None,
                        7: None,
                        },
                    3: {
                        2: {
                            2: None,
                            },
                        3: None,
                        5: None,
                        },
                    5: {
                        2: None,
                        3: None,
                        },
                    7: {
                        2: None,
                        },
                    11: None,
                    13: None,
                    },
                ),
            tempo=abjad.MetronomeMark(
                reference_duration=abjad.Duration(1, 4),
                units_per_minute=60,
                ),
            )

    ..  container:: example

        Each time-step in a ``BeatwiseQSchema`` is composed of three settings:

            * ``beatspan``
            * ``search_tree``
            * ``tempo``

        These settings can be applied as global defaults for the schema via keyword
        arguments, which persist until overridden:

        >>> beatspan = abjad.Duration(5, 16)
        >>> search_tree = abjadext.nauert.UnweightedSearchTree({7: None})
        >>> tempo = abjad.MetronomeMark((1, 4), 54)
        >>> q_schema = abjadext.nauert.BeatwiseQSchema(
        ...     beatspan=beatspan,
        ...     search_tree=search_tree,
        ...     tempo=tempo,
        ...     )

    ..  container:: example

        The computed value at any non-negative time-step can be found by
        subscripting:

        >>> index = 0
        >>> for key, value in sorted(q_schema[index].items()):
        ...     print('{}:'.format(key), value)
        ...
        beatspan: 5/16
        search_tree: UnweightedSearchTree(definition={7: None})
        tempo: 4=54

        >>> index = 1000
        >>> for key, value in sorted(q_schema[index].items()):
        ...     print('{}:'.format(key), value)
        ...
        beatspan: 5/16
        search_tree: UnweightedSearchTree(definition={7: None})
        tempo: 4=54

    ..  container:: example

        Per-time-step settings can be applied in a variety of ways.

        Instantiating the schema via ``*arguments`` with a series of either
        ``BeatwiseQSchemaItem`` instances, or dictionaries which could be used to
        instantiate ``BeatwiseQSchemaItem`` instances, will apply those settings
        sequentially, starting from time-step ``0``:

        >>> a = {'beatspan': abjad.Duration(5, 32)}
        >>> b = {'beatspan': abjad.Duration(3, 16)}
        >>> c = {'beatspan': abjad.Duration(1, 8)}

        >>> q_schema = abjadext.nauert.BeatwiseQSchema(a, b, c)

        >>> q_schema[0]['beatspan']
        Duration(5, 32)

        >>> q_schema[1]['beatspan']
        Duration(3, 16)

        >>> q_schema[2]['beatspan']
        Duration(1, 8)

        >>> q_schema[3]['beatspan']
        Duration(1, 8)

    ..  container:: example

        Similarly, instantiating the schema from a single dictionary, consisting
        of integer:specification pairs, or a sequence via ``*arguments`` of (integer,
        specification) pairs, allows for applying settings to  non-sequential
        time-steps:

        >>> a = {'search_tree': abjadext.nauert.UnweightedSearchTree({2: None})}
        >>> b = {'search_tree': abjadext.nauert.UnweightedSearchTree({3: None})}

        >>> settings = {
        ...     2: a,
        ...     4: b,
        ... }

        >>> q_schema = abjadext.nauert.MeasurewiseQSchema(settings)

        >>> abjad.f(q_schema[0]['search_tree'])
        abjadext.nauert.UnweightedSearchTree(
            definition={
                2: {
                    2: {
                        2: {
                            2: None,
                            },
                        3: None,
                        },
                    3: None,
                    5: None,
                    7: None,
                    },
                3: {
                    2: {
                        2: None,
                        },
                    3: None,
                    5: None,
                    },
                5: {
                    2: None,
                    3: None,
                    },
                7: {
                    2: None,
                    },
                11: None,
                13: None,
                },
            )

        >>> print(format(q_schema[1]['search_tree']))
        abjadext.nauert.UnweightedSearchTree(
            definition={
                2: {
                    2: {
                        2: {
                            2: None,
                            },
                        3: None,
                        },
                    3: None,
                    5: None,
                    7: None,
                    },
                3: {
                    2: {
                        2: None,
                        },
                    3: None,
                    5: None,
                    },
                5: {
                    2: None,
                    3: None,
                    },
                7: {
                    2: None,
                    },
                11: None,
                13: None,
                },
            )

        >>> q_schema[2]['search_tree']
        UnweightedSearchTree(definition={2: None})

        >>> q_schema[3]['search_tree']
        UnweightedSearchTree(definition={2: None})

        >>> q_schema[4]['search_tree']
        UnweightedSearchTree(definition={3: None})

        >>> q_schema[1000]['search_tree']
        UnweightedSearchTree(definition={3: None})

    ..  container:: example

        The following is equivalent to the above schema definition:

        >>> q_schema = abjadext.nauert.MeasurewiseQSchema(
        ...     (2, {'search_tree': abjadext.nauert.UnweightedSearchTree({2: None})}),
        ...     (4, {'search_tree': abjadext.nauert.UnweightedSearchTree({3: None})}),
        ...     )

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_beatspan", "_items", "_lookups", "_search_tree", "_tempo")

    _keyword_argument_names = ("beatspan", "search_tree", "tempo")

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, *arguments, **keywords):
        self._beatspan = abjad.Duration(keywords.get("beatspan", (1, 4)))
        search_tree = keywords.get("search_tree", UnweightedSearchTree())
        assert isinstance(search_tree, SearchTree)
        self._search_tree = search_tree
        tempo = keywords.get("tempo", ((1, 4), 60))
        if isinstance(tempo, tuple):
            tempo = abjad.MetronomeMark(*tempo)
        self._tempo = tempo
        QSchema.__init__(self, *arguments, **keywords)

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return abjad.FormatSpecification(
            client=self,
            storage_format_args_values=self.items or (),
            storage_format_keyword_names=["beatspan", "search_tree", "tempo"],
        )

    ### PUBLIC PROPERTIES ###

    @property
    def beatspan(self):
        """
        Default beatspan of beatwise q-schema.
        """
        return self._beatspan

    @property
    def item_class(self):
        """
        The schema's item class.

        Returns beatwise q-schema item.
        """
        return BeatwiseQSchemaItem

    @property
    def target_class(self):
        """
        Target class of beatwise q-schema.

        Returns beatwise q-target.
        """
        return BeatwiseQTarget

    @property
    def target_item_class(self):
        """
        Target item class of beatwise q-schema.

        Returns q-target beat.
        """
        return QTargetBeat
