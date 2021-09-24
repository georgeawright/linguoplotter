import pytest
from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.suggesters.projection_suggesters import LabelProjectionSuggester
from homer.structure_collection import StructureCollection


@pytest.fixture
def bubble_chamber():
    chamber = Mock()
    chamber.concepts = {"suggest": Mock(), "same": Mock(), "label": Mock()}
    return chamber


@pytest.fixture
def target_view():
    view = Mock()
    view.slot_values = {}
    return view


@pytest.fixture
def target_projectee(target_view):
    label = Mock()
    label.start.has_correspondence_to_space.return_value = True
    frame_correspondee = Mock()
    frame_correspondee.structure_id = "frame_correspondee"
    frame_correspondence = Mock()
    frame_correspondence.start = frame_correspondee
    frame_correspondence.end = label
    label.correspondences = StructureCollection({frame_correspondence})
    non_frame_correspondee = Mock()
    non_frame_correspondence = Mock()
    non_frame_correspondence.start = non_frame_correspondee
    non_frame_correspondence.end = frame_correspondee
    frame_correspondee.correspondences = StructureCollection({non_frame_correspondence})
    target_view.members = StructureCollection(
        {frame_correspondence, non_frame_correspondence}
    )
    target_view.slot_values[frame_correspondee.structure_id] = Mock()
    return label


def test_gives_suggests_projection_from_slot(
    bubble_chamber, target_view, target_projectee
):
    target_structures = {
        "target_view": target_view,
        "target_projectee": target_projectee,
    }
    suggester = LabelProjectionSuggester("", "", bubble_chamber, target_structures, 1.0)
    suggester.run()
    assert CodeletResult.SUCCESS == suggester.result


def test_gives_full_confidence_to_project_non_slot(
    bubble_chamber, target_view, target_projectee
):
    target_projectee.correspondences = StructureCollection()
    target_projectee.is_slot = False
    target_projectee.has_correspondence_to_space.return_value = False
    target_structures = {
        "target_view": target_view,
        "target_projectee": target_projectee,
    }
    suggester = LabelProjectionSuggester("", "", bubble_chamber, target_structures, 1.0)
    suggester.run()
    assert CodeletResult.SUCCESS == suggester.result
    assert 1.0 == suggester.confidence


def test_fizzles_if_label_projection_exists(
    bubble_chamber, target_view, target_projectee
):
    target_view.slot_values[target_projectee.structure_id] = Mock()
    target_structures = {
        "target_view": target_view,
        "target_projectee": target_projectee,
    }
    suggester = LabelProjectionSuggester("", "", bubble_chamber, target_structures, 1.0)
    suggester.run()
    assert CodeletResult.FIZZLE == suggester.result


def test_fizzles_if_label_start_has_no_correspondence_to_output(
    bubble_chamber, target_view, target_projectee
):
    target_projectee.start.has_correspondence_to_space.return_value = False
    target_structures = {
        "target_view": target_view,
        "target_projectee": target_projectee,
    }
    suggester = LabelProjectionSuggester("", "", bubble_chamber, target_structures, 1.0)
    suggester.run()
    assert CodeletResult.FIZZLE == suggester.result
