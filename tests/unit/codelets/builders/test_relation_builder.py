import pytest
from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.builders import ChunkBuilder, RelationBuilder
from homer.codelets.evaluators import RelationEvaluator
from homer.structure_collection import StructureCollection
from homer.structures.links import Relation
from homer.tools import hasinstance


@pytest.fixture
def parent_concept():
    concept = Mock()
    concept.classifier.classify.return_value = 1.0
    return concept


@pytest.fixture
def bubble_chamber(parent_concept):
    chamber = Mock()
    chamber.concepts = {"relation": Mock(), "build": Mock()}
    relational_concept_space = Mock()
    relational_concept_space.contents.of_type.return_value = StructureCollection(
        {parent_concept}
    )
    relational_concept = Mock()
    relational_concept.child_spaces = StructureCollection({relational_concept_space})
    space = Mock()
    space.name = "relational concepts"
    space.contents.of_type.return_value = StructureCollection(
        {relational_concept_space}
    )
    chamber.spaces = StructureCollection({space})
    return chamber


@pytest.fixture
def target_structure_two():
    structure = Mock()
    return structure


@pytest.fixture
def target_structure_one(target_structure_two):
    structure = Mock()
    parent_space_contents = Mock()
    parent_space_contents.get_exigent.return_value = target_structure_two
    structure.parent_spaces.get_random.return_value = parent_space_contents
    structure.has_relation.return_value = False
    structure.nearby.get_unhappy.return_value = Mock()
    return structure


def test_bottom_up_codelet_gets_a_concept(bubble_chamber):
    target_structure_one = Mock()
    relation_builder = RelationBuilder(
        Mock(), Mock(), bubble_chamber, Mock(), target_structure_one, 1.0
    )
    assert relation_builder.parent_concept is None
    relation_builder.run()
    assert relation_builder.parent_concept is not None


def test_codelet_gets_a_second_target_structure(bubble_chamber, target_structure_one):
    relation_builder = RelationBuilder(
        Mock(), Mock(), bubble_chamber, Mock(), target_structure_one, Mock()
    )
    assert relation_builder.target_structure_two is None
    relation_builder.run()
    assert relation_builder.target_structure_two is not None


def test_successful_creates_chunk_and_spawns_follow_up(
    bubble_chamber, target_structure_one
):
    relation_builder = RelationBuilder(
        Mock(), Mock(), bubble_chamber, Mock(), target_structure_one, Mock()
    )
    result = relation_builder.run()
    assert CodeletResult.SUCCESS == result
    assert hasinstance(relation_builder.child_structures, Relation)
    assert len(relation_builder.child_codelets) == 1
    assert isinstance(relation_builder.child_codelets[0], RelationEvaluator)


def test_fails_when_structures_cannot_be_related(
    parent_concept, bubble_chamber, target_structure_one
):
    parent_concept.classifier.classify.return_value = 0.0
    relation_builder = RelationBuilder(
        Mock(), Mock(), bubble_chamber, Mock(), target_structure_one, 1.0
    )
    result = relation_builder.run()
    assert CodeletResult.FAIL == result
    assert relation_builder.child_structures is None


def test_fizzles_when_relation_already_exists(bubble_chamber, target_structure_one):
    target_structure_one.has_relation.return_value = True
    relation_builder = RelationBuilder(
        Mock(), Mock(), bubble_chamber, Mock(), target_structure_one, 1.0
    )
    result = relation_builder.run()
    assert CodeletResult.FIZZLE == result
    assert relation_builder.child_structures is None
    assert len(relation_builder.child_codelets) == 1
    assert isinstance(relation_builder.child_codelets[0], RelationBuilder)
