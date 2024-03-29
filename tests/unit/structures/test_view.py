import pytest
from unittest.mock import Mock

from linguoplotter.structures import View


def test_add(bubble_chamber):
    view = View(
        "",
        "",
        Mock(),
        [],
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(Mock(), Mock()),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    node_1 = Mock()
    node_2 = Mock()
    correspondence = Mock()
    correspondence.node_pairs = [(node_1, node_2)]

    assert view.members.is_empty()
    assert [] == view.node_groups

    view.add(correspondence)
    assert correspondence in view.members
    assert [
        {node_1.parent_space: node_1, node_2.parent_space: node_2}
    ] == view.node_groups


def test_can_accept_member(bubble_chamber):
    parent_frame = Mock()
    parent_frame.concepts = bubble_chamber.new_structure_collection()
    view = View(
        "",
        "",
        parent_frame,
        [],
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(Mock(), Mock()),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )

    space_1 = Mock()
    space_2 = Mock()

    node_1 = Mock()
    node_1.is_link = False
    node_1.parent_space = space_1
    node_2 = Mock()
    node_2.is_link = False
    node_2.parent_space = space_2
    node_3 = Mock()
    node_3.is_link = False
    node_3.parent_space = space_1
    node_4 = Mock()
    node_4.is_link = False
    node_4.parent_space = space_2

    correspondence_1 = Mock()
    correspondence_1.parent_concept = Mock()
    correspondence_1.conceptual_space = Mock()
    correspondence_1.start = node_1
    correspondence_1.end = node_2
    correspondence_1.node_pairs = [(node_1, node_2)]
    node_2.correspondences = bubble_chamber.new_structure_collection()

    assert view.can_accept_member(
        correspondence_1.parent_concept,
        correspondence_1.conceptual_space,
        correspondence_1.start,
        correspondence_1.end,
    )
    node_2.correspondences.add(correspondence_1)
    view.add(correspondence_1)

    correspondence_2 = Mock()
    correspondence_2.parent_concept = correspondence_1.parent_concept
    correspondence_2.conceptual_space = correspondence_1.conceptual_space
    correspondence_2.start = node_1
    correspondence_2.end = node_2
    correspondence_2.node_pairs = [(node_1, node_2)]

    assert not view.can_accept_member(
        correspondence_2.parent_concept,
        correspondence_2.conceptual_space,
        correspondence_2.start,
        correspondence_2.end,
    )

    correspondence_3 = Mock()
    correspondence_3.parent_concept = correspondence_1.parent_concept
    correspondence_3.conceptual_space = Mock()
    correspondence_3.start = node_1
    correspondence_3.end = node_4
    correspondence_3.node_pairs = [(node_1, node_4)]
    node_4.correspondences = bubble_chamber.new_structure_collection()

    assert not view.can_accept_member(
        correspondence_3.parent_concept,
        correspondence_3.conceptual_space,
        correspondence_3.start,
        correspondence_3.end,
    )

    start_relation = Mock()
    start_relation.is_link = True
    end_relation = Mock()
    end_relation.is_link = True
    end_relation.parent_concept.is_slot = False
    end_relation.correspondences = bubble_chamber.new_structure_collection()
    assert end_relation.correspondences.is_empty()
    correspondence_4 = Mock()
    correspondence_4.parent_concept = correspondence_1.parent_concept
    correspondence_4.conceptual_space = correspondence_1.conceptual_space
    correspondence_4.start = start_relation
    correspondence_4.end = end_relation
    correspondence_4.node_pairs = [(node_1, node_2), (node_3, node_4)]

    assert view.can_accept_member(
        correspondence_4.parent_concept,
        correspondence_4.conceptual_space,
        correspondence_4.start,
        correspondence_4.end,
    )
