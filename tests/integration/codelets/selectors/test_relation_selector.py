import pytest
import random
from unittest.mock import Mock, patch

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.selectors import RelationSelector
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Chunk, Concept
from homer.structures.links import Relation
from homer.structures.spaces import ConceptualSpace, WorkingSpace


@pytest.fixture
def bubble_chamber():
    chamber = BubbleChamber(
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
        Mock(),
    )
    relation_concept = Concept(
        Mock(),
        Mock(),
        "relation",
        None,
        None,
        None,
        None,
        "value",
        StructureCollection(),
        None,
    )
    chamber.concepts.add(relation_concept)
    select_concept = Concept(
        Mock(),
        Mock(),
        "select",
        None,
        None,
        None,
        None,
        "value",
        StructureCollection(),
        None,
    )
    chamber.concepts.add(select_concept)
    relation = Relation(Mock(), Mock(), relation_concept, select_concept, None, None, 1)
    relation_concept.links_out.add(relation)
    select_concept.links_in.add(relation)
    return chamber


@pytest.fixture
def conceptual_space():
    space = ConceptualSpace(Mock(), Mock(), Mock(), Mock(), Mock())
    return space


@pytest.fixture
def working_space():
    space = WorkingSpace(Mock(), Mock(), Mock(), StructureCollection(), Mock(), Mock())
    return space


@pytest.fixture
def start(working_space):
    chunk = Chunk(Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock())
    chunk.locations.append(Location([1, 1], working_space))
    return chunk


@pytest.fixture
def end():
    chunk = Chunk(Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock())
    return chunk


@pytest.fixture
def good_relation(start, end, conceptual_space, working_space):
    concept = Concept(
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        conceptual_space,
        Mock(),
        Mock(),
        Mock(),
    )
    relation = Relation(
        Mock(),
        Mock(),
        start,
        end,
        concept,
        working_space,
        1.0,
    )
    start.links_out.add(relation)
    end.links_in.add(relation)
    working_space.contents.add(relation)
    return relation


@pytest.fixture
def bad_relation(start, end, conceptual_space, working_space):
    concept = Concept(
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        conceptual_space,
        Mock(),
        Mock(),
        Mock(),
    )
    relation = Relation(
        Mock(),
        Mock(),
        start,
        end,
        concept,
        working_space,
        0.0,
    )
    start.links_out.add(relation)
    end.links_in.add(relation)
    working_space.contents.add(relation)
    return relation


def test_good_relation_is_boosted_bad_relation_is_decayed(
    bubble_chamber, good_relation, bad_relation
):
    parent_id = ""
    champion = bad_relation
    urgency = 1.0
    selector = RelationSelector.spawn(parent_id, bubble_chamber, champion, urgency)
    for _ in range(20):
        selector.run()
        selector = selector.child_codelets[0]
        good_relation.update_activation()
        bad_relation.update_activation()
    assert 1 == good_relation.activation
    assert 0 == bad_relation.activation
