import pytest
from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.builders.projection_builders import ChunkProjectionBuilder
from homer.structure_collection import StructureCollection
from homer.structures.links import Correspondence
from homer.structures.nodes import Word
from homer.tools import hasinstance


@pytest.fixture
def bubble_chamber():
    chamber = Mock()
    chamber.concepts = {"build": Mock(), "same": Mock(), "chunk": Mock()}
    chamber.conceptual_spaces = {"grammar": Mock()}
    chamber.chunks = StructureCollection()
    return chamber


@pytest.fixture
def target_view():
    view = Mock()
    view.slot_values = {}
    return view


@pytest.fixture
def target_projectee(target_view):
    chunk = Mock()
    chunk_copy = Mock()
    chunk_copy.locations = []
    chunk.copy_to_location.return_value = chunk_copy
    return chunk


def test_projects_chunk_into_output_space(
    bubble_chamber, target_view, target_projectee
):
    target_projectee.has_correspondence_to_space.return_value = False
    target_structures = {
        "target_view": target_view,
        "target_projectee": target_projectee,
        "target_correspondence": None,
        "frame_correspondee": None,
        "non_frame": None,
        "non_frame_correspondee": None,
    }
    builder = ChunkProjectionBuilder("", "", bubble_chamber, target_structures, 1.0)
    builder.run()
    assert CodeletResult.SUCCESS == builder.result


def test_fizzles_if_chunk_projection_exists(
    bubble_chamber, target_view, target_projectee
):
    target_projectee.has_correspondence_to_space.return_value = True
    target_structures = {
        "target_view": target_view,
        "target_projectee": target_projectee,
        "target_correspondence": None,
        "frame_correspondee": None,
        "non_frame": None,
        "non_frame_correspondee": None,
    }
    builder = ChunkProjectionBuilder("", "", bubble_chamber, target_structures, 1.0)
    builder.run()
    assert CodeletResult.FIZZLE == builder.result