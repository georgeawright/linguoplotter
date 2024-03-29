import pytest
from unittest.mock import Mock

from linguoplotter.codelet_result import CodeletResult
from linguoplotter.codelets.builders.projection_builders import LabelProjectionBuilder
from linguoplotter.structure_collection import StructureCollection
from linguoplotter.structures.links import Correspondence
from linguoplotter.tools import hasinstance


@pytest.fixture
def grammar_space(bubble_chamber):
    space = Mock()
    space.name = "grammar"
    bubble_chamber.conceptual_spaces = bubble_chamber.new_structure_collection(space)
    return space


@pytest.fixture
def target_view():
    view = Mock()
    view.slot_values = {}
    return view


@pytest.fixture
def target_projectee(target_view):
    label = Mock()
    label.start = Mock()
    label.start.correspondences_to_space.return_value = Mock()
    return label


@pytest.fixture
def label_concept():
    concept = Mock()
    return concept


@pytest.fixture
def frame_correspondee(bubble_chamber, target_view, label_concept, target_projectee):
    correspondee = Mock()
    correspondee.structure_id = "frame_correspondee"
    frame_correspondence = Mock()
    frame_correspondence.start = frame_correspondee
    frame_correspondence.end = target_projectee
    target_projectee.correspondences = bubble_chamber.new_structure_collection(
        frame_correspondence
    )
    non_frame_correspondee = Mock()
    non_frame_correspondence = Mock()
    non_frame_correspondence.start = non_frame_correspondee
    non_frame_correspondence.end = correspondee
    correspondee.correspondences = bubble_chamber.new_structure_collection(
        frame_correspondence, non_frame_correspondence
    )
    target_view.members = bubble_chamber.new_structure_collection(
        frame_correspondence, non_frame_correspondence
    )
    target_view.slot_values[correspondee.structure_id] = label_concept
    return correspondee


def test_projects_slot_into_output_space(
    bubble_chamber, target_view, target_projectee, frame_correspondee, grammar_space
):
    target_projectee.is_slot = True
    target_projectee.has_correspondence_to_space.return_value = False
    target_structures = {
        "target_view": target_view,
        "target_projectee": target_projectee,
        "target_correspondence": Mock(),
        "frame_correspondee": frame_correspondee,
        "non_frame": Mock(),
        "non_frame_correspondee": Mock(),
    }
    builder = LabelProjectionBuilder("", "", bubble_chamber, target_structures, 1.0)
    builder.run()
    assert CodeletResult.FINISH == builder.result


def test_fizzles_if_word_projection_exists(
    bubble_chamber, target_view, target_projectee, frame_correspondee
):
    target_projectee.is_slot = True
    target_projectee.has_correspondence_to_space.return_value = True
    target_structures = {
        "target_view": target_view,
        "target_projectee": target_projectee,
        "target_correspondence": Mock(),
        "frame_correspondee": frame_correspondee,
        "non_frame": Mock(),
        "non_frame_correspondee": Mock(),
    }
    builder = LabelProjectionBuilder("", "", bubble_chamber, target_structures, 1.0)
    builder.run()
    assert CodeletResult.FIZZLE == builder.result
