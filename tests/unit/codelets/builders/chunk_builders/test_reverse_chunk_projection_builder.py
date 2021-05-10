import pytest
from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.builders.chunk_builders import ReverseChunkProjectionBuilder
from homer.codelets.evaluators.chunk_evaluators import ReverseChunkProjectionEvaluator
from homer.structure_collection import StructureCollection
from homer.structures.nodes import Chunk
from homer.tools import hasinstance


@pytest.fixture
def bubble_chamber():
    chamber = Mock()
    chamber.concepts = {"build": Mock(), "chunk": Mock(), "same": Mock()}
    return chamber


@pytest.fixture
def target_view(bubble_chamber):
    view = Mock()
    existing_chunk = Mock()
    existing_chunk.members = StructureCollection()
    view.interpretation_space.contents.of_type.return_value = StructureCollection(
        {existing_chunk}
    )
    bubble_chamber.monitoring_views.get_active.return_value = view
    return view


@pytest.fixture
def temperature_interpretation_space():
    space = Mock()
    space.parent_concept.relevant_value = "value"
    return space


@pytest.fixture
def target_interpretation_chunk(temperature_interpretation_space):
    chunk = Mock()
    chunk.members = StructureCollection()
    chunk.parent_spaces = StructureCollection({temperature_interpretation_space})
    link = Mock()
    link.parent_concept.classifier.classify.return_value = 1
    chunk.links = StructureCollection({link})
    chunk.correspondences = StructureCollection()
    chunk.labels = StructureCollection({link})
    chunk.links_out = StructureCollection()
    chunk.links_in = StructureCollection()
    return chunk


@pytest.fixture
def target_raw_chunk():
    chunk = Mock()
    chunk.has_correspondence_to_space.return_value = False
    chunk.value = [[10]]
    location = Mock()
    location.coordinates = [[0, 0]]
    chunk.location_in_space.return_value = location
    return chunk


def test_successful_projects_chunk_creates_larger_chunk_and_spawns_follow_up(
    bubble_chamber, target_view, target_interpretation_chunk, target_raw_chunk
):
    chunk_builder = ReverseChunkProjectionBuilder(
        Mock(),
        Mock(),
        bubble_chamber,
        target_view,
        target_interpretation_chunk,
        target_raw_chunk,
        1,
    )
    result = chunk_builder.run()
    assert CodeletResult.SUCCESS == result
    assert hasinstance(chunk_builder.child_structures, Chunk)
    child_chunks = chunk_builder.child_structures.of_type(Chunk)
    child_chunk_1 = child_chunks.pop()
    child_chunk_2 = child_chunks.pop()
    assert (
        child_chunk_1 in child_chunk_2.members
        and child_chunk_2.size > len(target_interpretation_chunk.members)
    ) or (
        child_chunk_2 in child_chunk_1.members
        and child_chunk_1.size > len(target_interpretation_chunk.members)
    )
    assert len(chunk_builder.child_codelets) == 1
    assert isinstance(chunk_builder.child_codelets[0], ReverseChunkProjectionEvaluator)


def test_fails_when_raw_chunk_is_incompatible_with_links(
    bubble_chamber, target_view, target_interpretation_chunk, target_raw_chunk
):
    link_1 = Mock()
    link_1.parent_concept.classifier.classify.return_value = 0
    target_interpretation_chunk.links.add(link_1)
    link_2 = Mock()
    link_2.parent_concept.classifier.classify.return_value = 0
    target_interpretation_chunk.links.add(link_2)
    chunk_builder = ReverseChunkProjectionBuilder(
        Mock(),
        Mock(),
        bubble_chamber,
        target_view,
        target_interpretation_chunk,
        target_raw_chunk,
        1.0,
    )
    result = chunk_builder.run()
    assert CodeletResult.FAIL == result
    assert chunk_builder.child_structures is None
    assert len(chunk_builder.child_codelets) == 1
    assert isinstance(chunk_builder.child_codelets[0], ReverseChunkProjectionBuilder)


def test_fizzles_when_raw_chunk_has_correspondence_to_interpretation_space(
    bubble_chamber, target_view, target_interpretation_chunk, target_raw_chunk
):
    target_raw_chunk.has_correspondence_to_space.return_value = True
    urgency = 1.0
    chunk_builder = ReverseChunkProjectionBuilder(
        Mock(),
        Mock(),
        bubble_chamber,
        target_view,
        target_interpretation_chunk,
        target_raw_chunk,
        urgency,
    )
    result = chunk_builder.run()
    assert CodeletResult.FIZZLE == result
    assert chunk_builder.child_structures is None
    assert len(chunk_builder.child_codelets) == 1
    assert isinstance(chunk_builder.child_codelets[0], ReverseChunkProjectionBuilder)