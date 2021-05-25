import pytest
from unittest.mock import Mock, patch

from homer.codelet_result import CodeletResult
from homer.codelets.builders import CorrespondenceBuilder
from homer.codelets.suggesters import CorrespondenceSuggester
from homer.location import Location
from homer.structure import Structure
from homer.structure_collection import StructureCollection
from homer.structures.links import Correspondence
from homer.tools import hasinstance


@pytest.fixture
def same_concept():
    concept = Mock()
    concept.name = "same"
    concept.classifier.classify.return_value = 1.0
    return concept


@pytest.fixture
def same_different_space(same_concept):
    space = Mock()
    space.contents.of_type.return_value = StructureCollection({same_concept})
    return space


@pytest.fixture
def label_concept_space():
    return Mock()


@pytest.fixture
def label_concept_working_space(label_concept_space):
    space = Mock()
    space.conceptual_space = label_concept_space
    return space


@pytest.fixture
def bubble_chamber(same_different_space, label_concept_space):
    chamber = Mock()
    chamber.concepts = {"correspondence": Mock(), "suggest": Mock(), "text": Mock()}
    label_concepts = Mock()
    label_concepts.contents.of_type.return_value = StructureCollection(
        {label_concept_space}
    )
    correspondential_concepts = Mock()
    correspondential_concepts.contents.of_type.return_value = StructureCollection(
        {same_different_space}
    )
    working_spaces = Mock()
    working_space = Mock()
    working_space_contents = Mock()
    working_space_contents.get_exigent.return_value = target_structure_two
    working_space.contents.of_type.return_value = working_space_contents
    working_spaces.get_active.return_value = working_space
    chamber.spaces = {
        "label concepts": label_concepts,
        "correspondential concepts": correspondential_concepts,
        "top level working": Mock(),
        "text": Mock(),
    }
    chamber.working_spaces = working_spaces
    return chamber


@pytest.fixture
def target_space_one(bubble_chamber):
    space = Mock()
    space.name = "target_space_one"
    space.parent_spaces = []
    space.conceptual_space = Mock()
    bubble_chamber.working_spaces.add(target_space_one)
    return space


@pytest.fixture
def target_space_two(bubble_chamber, target_space_one):
    space = Mock()
    space.name = "target_space_two"
    space.conceptual_space = target_space_one.conceptual_space
    space.is_basic_level = True
    return space


@pytest.fixture
def target_structure_one(bubble_chamber, label_concept_working_space):
    structure = Mock()
    structure.is_slot = False
    structure.correspondences = StructureCollection()
    structure.has_correspondence.return_value = False
    structure.parent_spaces = StructureCollection({label_concept_working_space})
    return structure


@pytest.fixture
def target_structure_two(label_concept_working_space, target_space_two):
    structure = Mock()
    structure.is_slot = True
    structure.correspondences = StructureCollection()
    structure.name = "target_structure_two"
    structure.parent_spaces = StructureCollection({label_concept_working_space})
    target_space_two.contents.of_type.return_value = StructureCollection({structure})
    return structure


@pytest.fixture
def existing_correspondence():
    correspondence = Mock()
    correspondence.is_compatible_with.return_value = True
    return correspondence


@pytest.fixture
def target_view(existing_correspondence, target_space_one, target_space_two):
    input_space = Mock()
    input_space.name = "target space 2 container"
    input_space.contents.of_type.return_value = StructureCollection({target_space_two})
    view = Mock()
    view.input_spaces = StructureCollection({input_space})
    view.has_member.return_value = False
    view.members = StructureCollection({existing_correspondence})
    view.slot_values = {}
    return view


def test_gets_second_target_space_and_structure_if_needed(
    bubble_chamber,
    target_view,
    target_space_one,
    target_structure_one,
    same_concept,
    target_space_two,
    target_structure_two,
):
    target_structures = {
        "target_view": target_view,
        "target_space_one": target_space_one,
        "target_space_two": target_space_two,
        "target_structure_one": target_structure_one,
        "target_structure_two": target_structure_two,
        "target_conceptual_space": None,
        "parent_concept": same_concept,
    }
    correspondence_suggester = CorrespondenceSuggester(
        Mock(),
        Mock(),
        bubble_chamber,
        target_structures,
        Mock(),
    )
    assert correspondence_suggester.target_space_two is None
    assert correspondence_suggester.target_structure_two is None
    correspondence_suggester.run()
    assert correspondence_suggester.target_space_two == target_space_two
    assert correspondence_suggester.target_structure_two == target_structure_two


def test_gets_parent_concept_if_needed(
    bubble_chamber,
    target_view,
    target_space_one,
    target_structure_one,
    target_space_two,
    target_structure_two,
):
    target_structures = {
        "target_view": target_view,
        "target_space_one": target_space_one,
        "target_space_two": target_space_two,
        "target_structure_one": target_structure_one,
        "target_structure_two": target_structure_two,
        "target_conceptual_space": None,
        "parent_concept": None,
    }
    correspondence_suggester = CorrespondenceSuggester(
        Mock(),
        Mock(),
        bubble_chamber,
        target_structures,
        Mock(),
    )
    assert correspondence_suggester.parent_concept is None
    correspondence_suggester.run()
    assert correspondence_suggester.parent_concept is not None


def test_gives_high_confidence_for_good_example(
    bubble_chamber,
    target_view,
    target_space_one,
    target_structure_one,
    same_concept,
    target_space_two,
    target_structure_two,
):
    target_structures = {
        "target_view": target_view,
        "target_space_one": target_space_one,
        "target_space_two": target_space_two,
        "target_structure_one": target_structure_one,
        "target_structure_two": target_structure_two,
        "target_conceptual_space": None,
        "parent_concept": same_concept,
    }
    correspondence_suggester = CorrespondenceSuggester(
        Mock(),
        Mock(),
        bubble_chamber,
        target_structures,
        Mock(),
    )
    result = correspondence_suggester.run()
    assert CodeletResult.SUCCESS == result
    assert correspondence_suggester.confidence == 1
    assert len(correspondence_suggester.child_codelets) == 1
    assert isinstance(correspondence_suggester.child_codelets[0], CorrespondenceBuilder)


def test_gives_low_confidence_for_bad_example(
    bubble_chamber,
    target_view,
    target_space_one,
    target_structure_one,
    target_space_two,
    target_structure_two,
):
    concept = Mock()
    concept.classifier.classify.return_value = 0.0
    target_structures = {
        "target_view": target_view,
        "target_space_one": target_space_one,
        "target_space_two": target_space_two,
        "target_structure_one": target_structure_one,
        "target_structure_two": target_structure_two,
        "target_conceptual_space": None,
        "parent_concept": concept,
    }

    correspondence_suggester = CorrespondenceSuggester(
        Mock(),
        Mock(),
        bubble_chamber,
        target_structures,
        Mock(),
    )
    result = correspondence_suggester.run()
    assert CodeletResult.SUCCESS == result
    assert correspondence_suggester.confidence == 0
    assert len(correspondence_suggester.child_codelets) == 1
    assert isinstance(correspondence_suggester.child_codelets[0], CorrespondenceBuilder)


def test_fizzles_when_correspondence_already_exists(
    bubble_chamber,
    target_view,
    target_space_one,
    target_structure_one,
    target_space_two,
    target_structure_two,
    same_concept,
):
    target_view.has_member.return_value = True
    target_structures = {
        "target_view": target_view,
        "target_space_one": target_space_one,
        "target_space_two": target_space_two,
        "target_structure_one": target_structure_one,
        "target_structure_two": target_structure_two,
        "target_conceptual_space": None,
        "parent_concept": same_concept,
    }

    correspondence_suggester = CorrespondenceSuggester(
        Mock(),
        Mock(),
        bubble_chamber,
        target_structures,
        Mock(),
    )
    result = correspondence_suggester.run()
    assert CodeletResult.FIZZLE == result