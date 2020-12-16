import pytest
import random
from unittest.mock import Mock, patch

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.selectors import CorrespondenceSelector
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Chunk, Concept
from homer.structures.links import Correspondence, Relation
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
    correspondence_concept = Concept(
        Mock(),
        Mock(),
        "correspondence",
        None,
        None,
        None,
        None,
        "value",
        StructureCollection(),
        None,
    )
    chamber.concepts.add(correspondence_concept)
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
    relation = Relation(
        Mock(), Mock(), correspondence_concept, select_concept, None, None, 1
    )
    correspondence_concept.links_out.add(relation)
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
def start_space():
    space = WorkingSpace(Mock(), Mock(), Mock(), StructureCollection(), Mock(), Mock())
    return space


@pytest.fixture
def end_space():
    space = WorkingSpace(Mock(), Mock(), Mock(), StructureCollection(), Mock(), Mock())
    return space


@pytest.fixture
def start(start_space):
    chunk = Chunk(Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock())
    chunk.locations.append(Location([1, 1], start_space))
    return chunk


@pytest.fixture
def end():
    chunk = Chunk(Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock())
    return chunk


@pytest.fixture
def good_correspondence(
    start, end, start_space, end_space, conceptual_space, working_space
):
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
    correspondence = Correspondence(
        Mock(),
        Mock(),
        start,
        end,
        start_space,
        end_space,
        concept,
        working_space,
        conceptual_space,
        1.0,
    )
    start.links_out.add(correspondence)
    end.links_in.add(correspondence)
    working_space.contents.add(correspondence)
    return correspondence


@pytest.fixture
def bad_correspondence(
    start,
    end,
    start_space,
    end_space,
    conceptual_space,
    working_space,
):
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
    correspondence = Correspondence(
        Mock(),
        Mock(),
        start,
        end,
        start_space,
        end_space,
        concept,
        working_space,
        conceptual_space,
        0.0,
    )
    start.links_out.add(correspondence)
    end.links_in.add(correspondence)
    working_space.contents.add(correspondence)
    return correspondence


def test_good_correspondence_is_boosted_bad_correspondence_is_decayed(
    bubble_chamber, good_correspondence, bad_correspondence
):
    parent_id = ""
    champion = bad_correspondence
    urgency = 1.0
    selector = CorrespondenceSelector.spawn(
        parent_id, bubble_chamber, champion, urgency
    )
    for _ in range(20):
        selector.run()
        selector = selector.child_codelets[0]
        good_correspondence.update_activation()
        bad_correspondence.update_activation()
    assert 1 == good_correspondence.activation
    assert 0 == bad_correspondence.activation
