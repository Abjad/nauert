import bisect
import copy

import abjad

from .QEventProxy import QEventProxy
from .QGridContainer import QGridContainer
from .QGridLeaf import QGridLeaf


class QGrid:
    """
    Q-grid.

    Rhythm-tree-based model for how millisecond attack points collapse onto the
    offsets generated by a nested rhythmic structure.

    >>> q_grid = abjadext.nauert.QGrid()

    ..  container:: example

        >>> abjad.f(q_grid)
        abjadext.nauert.QGrid(
            root_node=abjadext.nauert.QGridLeaf(
                preprolated_duration=abjad.Duration(1, 1),
                is_divisible=True,
                ),
            next_downbeat=abjadext.nauert.QGridLeaf(
                preprolated_duration=abjad.Duration(1, 1),
                is_divisible=True,
                ),
            )

    ..  container:: example

        ``QGrids`` model not only the internal nodes of the nesting structure,
        but also the downbeat to the "next" ``QGrid``, allowing events which
        occur very late within one structure to collapse virtually onto the
        beginning of the next structure.

        ``QEventProxies`` can be "loaded in" to the node contained by the
        ``QGrid`` closest to their virtual offset:

        >>> q_event_a = abjadext.nauert.PitchedQEvent(250, [0])
        >>> q_event_b = abjadext.nauert.PitchedQEvent(750, [1])
        >>> proxy_a = abjadext.nauert.QEventProxy(q_event_a, 0.25)
        >>> proxy_b = abjadext.nauert.QEventProxy(q_event_b, 0.75)

        >>> q_grid.fit_q_events([proxy_a, proxy_b])

        >>> for q_event_proxy in q_grid.root_node.q_event_proxies:
        ...     abjad.f(q_event_proxy)
        ...
        abjadext.nauert.QEventProxy(
            abjadext.nauert.PitchedQEvent(
                offset=abjad.Offset((250, 1)),
                pitches=(
                    abjad.NamedPitch("c'"),
                    ),
                ),
            abjad.Offset((1, 4))
            )

        >>> for q_event_proxy in q_grid.next_downbeat.q_event_proxies:
        ...     abjad.f(q_event_proxy)
        ...
        abjadext.nauert.QEventProxy(
            abjadext.nauert.PitchedQEvent(
                offset=abjad.Offset((750, 1)),
                pitches=(
                    abjad.NamedPitch("cs'"),
                    ),
                ),
            abjad.Offset((3, 4))
            )

    Used internally by the ``Quantizer``.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_next_downbeat", "_root_node")

    _publish_storage_format = True

    ### INITIALIZATION ###

    def __init__(self, root_node=None, next_downbeat=None):
        if root_node is None:
            root_node = QGridLeaf(preprolated_duration=1)
        assert isinstance(
            root_node,
            (QGridLeaf, QGridContainer),
        )
        if next_downbeat is None:
            next_downbeat = QGridLeaf(preprolated_duration=1)
        assert isinstance(next_downbeat, QGridLeaf)
        self._root_node = root_node
        self._next_downbeat = next_downbeat
        self._next_downbeat._offset = abjad.Offset(1)
        self._next_downbeat._offsets_are_current = True

    ### SPECIAL METHODS ###

    def __call__(self, beatspan):
        """
        Calls q-grid.
        """
        result = self.root_node(beatspan)
        result_leaves = []
        for x in result:
            if isinstance(x, abjad.Container):
                leaves = abjad.select(x).leaves()
                result_leaves.extend(leaves)
            else:
                result_leaves.append(x)
        for result_leaf, q_grid_leaf in zip(result_leaves, self.leaves[:-1]):
            if q_grid_leaf.q_event_proxies:
                q_events = [
                    q_event_proxy.q_event
                    for q_event_proxy in q_grid_leaf.q_event_proxies
                ]
                q_events.sort(key=lambda x: 0 if x.index is None else x.index)
                annotation = {"q_events": tuple(q_events)}
                abjad.attach(annotation, result_leaf)
        return result

    def __copy__(self, *arguments):
        """
        Copies q-grid.

        Returns new q-grid.
        """
        root_node, next_downbeat = self._root_node, self._next_downbeat
        return type(self)(copy.deepcopy(root_node), copy.deepcopy(next_downbeat))

    def __eq__(self, argument):
        """
        True if `argument` is a q-grid with root node and next downbeat
        equal to those of this q-grid. Otherwise false.

        Returns true or false.
        """
        if type(self) == type(argument):
            if self.root_node == argument.root_node:
                if self.next_downbeat == argument.next_downbeat:
                    return True
        return False

    def __format__(self, format_specification=""):
        """
        Formats q-event.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        """
        return abjad.StorageFormatManager(self).get_storage_format()

    def __hash__(self):
        """
        Hashes q-grid.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        """
        return super(QGrid, self).__hash__()

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return abjad.FormatSpecification(client=self)

    ### PUBLIC METHODS ###

    def fit_q_events(self, q_event_proxies):
        r"""Fit each ``QEventProxy`` in ``q_event_proxies`` onto
        the contained ``QGridLeaf`` whose offset is nearest.

        Returns None
        """
        assert all(isinstance(x, QEventProxy) for x in q_event_proxies)
        leaves, offsets = self.leaves, self.offsets
        for q_event_proxy in q_event_proxies:
            idx = bisect.bisect_left(offsets, q_event_proxy.offset)
            if q_event_proxy.offset == offsets[idx]:
                leaves[idx].q_event_proxies.append(q_event_proxy)
            else:
                left, right = offsets[idx - 1], offsets[idx]
                left_diff = abs(left - q_event_proxy.offset)
                right_diff = abs(right - q_event_proxy.offset)
                if right_diff < left_diff:
                    leaves[idx].q_event_proxies.append(q_event_proxy)
                else:
                    leaves[idx - 1].q_event_proxies.append(q_event_proxy)

    def sort_q_events_by_index(self):
        r"""Sort ``QEventProxies`` attached to each ``QGridLeaf`` in a
        ``QGrid`` by their index.

        Returns None.
        """
        for leaf in self.leaves:
            leaf.q_event_proxies.sort(key=lambda x: x.index)

    def subdivide_leaf(self, leaf, subdivisions):
        r"""Replace the ``QGridLeaf`` ``leaf`` contained in a ``QGrid``
        by a ``QGridContainer`` containing ``QGridLeaves`` with durations
        equal to the ratio described in ``subdivisions``

        Returns the ``QEventProxies`` attached to ``leaf``.
        """
        container = QGridContainer(
            preprolated_duration=leaf.preprolated_duration,
            children=[
                QGridLeaf(preprolated_duration=subdivision)
                for subdivision in subdivisions
            ],
        )
        if leaf.parent is not None:
            index = leaf.parent.index(leaf)
            leaf.parent[index] = [container]
        # otherwise, our root node if just a QGridLeaf
        else:
            self._root_node = container
        return leaf.q_event_proxies

    def subdivide_leaves(self, pairs):
        r"""Given a sequence of leaf-index:subdivision-ratio pairs ``pairs``,
        subdivide the ``QGridLeaves`` described by the indices into
        ``QGridContainers`` containing ``QGridLeaves`` with durations
        equal to their respective subdivision-ratios.

        Returns the ``QEventProxies`` attached to thus subdivided
        ``QGridLeaf``.
        """
        import abjad

        pairs = sorted(dict(pairs).items())
        leaf_indices = [pair[0] for pair in pairs]
        subdivisions = [pair[1] for pair in pairs]

        all_leaves = self.leaves
        leaves_to_subdivide = [all_leaves[idx] for idx in leaf_indices]

        q_event_proxies = []
        for i, leaf in enumerate(leaves_to_subdivide):

            next_leaf = all_leaves[all_leaves.index(leaf) + 1]
            if next_leaf is self.next_downbeat:
                next_leaf_offset = abjad.Offset(1)
            else:
                next_leaf_offset = next_leaf.start_offset

            q_event_proxies.extend(self.subdivide_leaf(leaf, subdivisions[i]))
            for q_event_proxy in tuple(next_leaf.q_event_proxies):
                if q_event_proxy.offset < next_leaf_offset:
                    idx = next_leaf.q_event_proxies.index(q_event_proxy)
                    q_event_proxies.append(next_leaf.q_event_proxies.pop(idx))

        return q_event_proxies

    ### PUBLIC PROPERTIES ###

    @property
    def distance(self):
        r"""The computed total distance of the offset of each ``QEventProxy``
        contained by the ``QGrid`` to the offset of the ``QGridLeaf`` to
        which the ``QEventProxy`` is attached.

        Return ``Duration`` instance.
        """
        count = 0
        absolute_distance = 0
        for leaf, offset in zip(self.leaves, self.offsets):
            for q_event_proxy in leaf.q_event_proxies:
                absolute_distance += abs(q_event_proxy.offset - offset)
                count += 1
        if count:
            return absolute_distance / count
        return None

    @property
    def leaves(self):
        r"""All of the leaf nodes in the QGrid, including the next
        downbeat's node.

        Returns tuple of ``QGridLeaf`` instances.
        """
        if isinstance(self._root_node, QGridLeaf):
            return (self._root_node, self._next_downbeat)
        return self._root_node.leaves + (self._next_downbeat,)

    @property
    def next_downbeat(self):
        r"""The node representing the "next" downbeat after the contents
        of the QGrid's tree.

        Return ``QGridLeaf`` instance.
        """
        return self._next_downbeat

    @property
    def offsets(self):
        r"""The offsets between 0 and 1 of all of the leaf nodes in the QGrid.

        Returns tuple of ``Offset`` instances.
        """
        import abjad

        return tuple([x.start_offset for x in self.leaves[:-1]] + [abjad.Offset(1)])

    @property
    def pretty_rtm_format(self):
        r"""The pretty RTM-format of the root node of the ``QGrid``.

        Returns string.
        """
        return self._root_node.pretty_rtm_format

    @property
    def root_node(self):
        r"""The root node of the ``QGrid``.

        Return ``QGridLeaf`` or ``QGridContainer``.
        """
        return self._root_node

    @property
    def rtm_format(self):
        r"""The RTM format of the root node of the ``QGrid``.

        Returns string.
        """
        return self._root_node.rtm_format
