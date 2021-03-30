import pytest
from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.builders import LabelBuilder
from homer.codelets.evaluators import LabelEvaluator
from homer.structure_collection import StructureCollection
from homer.structures.links import Label
from homer.structures.nodes import Concept


@pytest.fixture
def working_space():
    space = Mock()
    space.parent_concept.relevant_value = "value"
    space.contents = StructureCollection()
    return space


@pytest.fixture
def parent_concept(working_space):
    concept = Mock()
    concept.relevant_value = "value"
    concept.parent_space.instance_in_space.return_value = working_space
    concept.classifier.classify.return_value = 1.0
    return concept


@pytest.fixture
def bubble_chamber(parent_concept):
    chamber = Mock()
    chamber.concepts = {"label": Mock(), "build": Mock()}
    label_concept_space = Mock()
    label_concept_space.is_basic_level = True
    label_concept_space.instance_type = str
    label_concept_space.contents.of_type.return_value = StructureCollection(
        {parent_concept}
    )
    space = Mock()
    space.name = "label concepts"
    space.contents.of_type.return_value = StructureCollection({label_concept_space})
    chamber.spaces = StructureCollection({space})
    top_level_working_space = Mock()
    top_level_working_space.name = "top level working"
    chamber.spaces.add(top_level_working_space)
    return chamber


@pytest.fixture
def target_chunk():
    chunk = Mock()
    chunk.has_label.return_value = False
    chunk.nearby.get_unhappy.return_value = Mock()
    chunk.value = ""
    return chunk


def test_bottom_up_codelet_gets_a_concept(bubble_chamber, target_chunk):
    label_builder = LabelBuilder(Mock(), Mock(), bubble_chamber, target_chunk, 1.0)
    assert label_builder.parent_concept is None
    label_builder.run()
    assert label_builder.parent_concept is not None


def test_successful_creates_label_and_spawns_follow_up(bubble_chamber, target_chunk):
    label_builder = LabelBuilder(Mock(), Mock(), bubble_chamber, target_chunk, 1.0)
    result = label_builder.run()
    assert CodeletResult.SUCCESS == result
    assert isinstance(label_builder.child_structure, Label)
    assert len(label_builder.child_codelets) == 1
    assert isinstance(label_builder.child_codelets[0], LabelEvaluator)


def test_fails_when_chunk_is_bad_example(bubble_chamber, target_chunk):
    parent_concept = Mock()
    parent_concept.classifier.classify.return_value = 0.0
    label_builder = LabelBuilder(
        Mock(), Mock(), bubble_chamber, target_chunk, 1.0, parent_concept=parent_concept
    )
    result = label_builder.run()
    assert CodeletResult.FAIL == result
    assert label_builder.child_structure is None
    assert len(label_builder.child_codelets) == 1
    assert isinstance(label_builder.child_codelets[0], LabelBuilder)


def test_fizzles_when_label_exists(bubble_chamber, target_chunk):
    target_chunk.has_label.return_value = True
    label_builder = LabelBuilder(Mock(), Mock(), bubble_chamber, target_chunk, 1.0)
    result = label_builder.run()
    assert CodeletResult.FIZZLE == result
    assert label_builder.child_structure is None
    assert len(label_builder.child_codelets) == 1
    assert isinstance(label_builder.child_codelets[0], LabelBuilder)
