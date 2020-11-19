from unittest.mock import Mock

from homer.structure import Structure
from homer.structure_collection import StructureCollection
from homer.structures import Lexeme
from homer.structures.links import Correspondence, Label, Relation


def test_correspondences_returns_correspondences():
    number_of_correspondences = 10
    links_in = StructureCollection()
    links_out = StructureCollection()
    for _ in range(number_of_correspondences // 2):
        correspondence = Correspondence(
            Mock(), Mock(), Mock(), Mock(), Mock(), Mock, Mock(), Mock()
        )
        links_out.add(correspondence)
        correspondence = Correspondence(
            Mock(), Mock(), Mock(), Mock(), Mock(), Mock, Mock(), Mock()
        )
        links_in.add(correspondence)
    for _ in range(number_of_correspondences // 2):
        links_out.add(Mock())
        links_in.add(Mock())
    structure = Structure(Mock(), Mock(), links_in=links_in, links_out=links_out)
    assert number_of_correspondences == len(structure.correspondences)
    for correspondence in structure.correspondences:
        assert isinstance(correspondence, Correspondence)


def test_labels_returns_labels():
    number_of_labels = 10
    links_out = StructureCollection()
    for _ in range(number_of_labels):
        label = Label(Mock(), Mock(), Mock(), Mock())
        links_out.add(label)
    for _ in range(number_of_labels):
        links_out.add(Mock())
    structure = Structure(Mock(), Mock(), links_out=links_out)
    assert number_of_labels == len(structure.labels)
    for label in structure.labels:
        assert isinstance(label, Label)


def test_lexemes_returns_lexemes():
    structure = Structure(Mock(), Mock())
    number_of_lexemes = 10
    for _ in range(number_of_lexemes):
        lexeme = Lexeme(Mock(), Mock())
        relation = Relation(structure, lexeme, Mock(), Mock(), Mock())
        structure.links_out.add(relation)
    for _ in range(number_of_lexemes):
        structure.links_out.add(Mock())
    assert number_of_lexemes == len(structure.lexemes)
    for lexeme in structure.lexemes:
        assert isinstance(lexeme, Lexeme)


def test_labels_in_space():
    structure = Structure(Mock(), Mock(), links_out=StructureCollection())
    space = Mock()
    space.contents = StructureCollection()
    label_in_space = Label(Mock(), Mock(), Mock(), Mock())
    space.contents.add(label_in_space)
    label_not_in_space = Label(Mock(), Mock(), Mock(), Mock())
    structure.links_out.add(label_in_space)
    structure.links_out.add(label_not_in_space)
    assert label_in_space in structure.labels_in_space(space)
    assert label_not_in_space not in structure.labels_in_space(space)


def test_relations_in_space_with():
    structure = Structure(Mock(), Mock(), links_out=StructureCollection())
    end = Mock()
    space = Mock()
    space.contents = StructureCollection()
    relation_in_space_with_end = Relation(structure, end, Mock(), Mock(), Mock())
    relation_in_space_not_with_end = Relation(structure, Mock(), Mock(), Mock(), Mock())
    relation_not_in_space_with_end = Relation(structure, end, Mock(), Mock(), Mock())
    space.contents.add(relation_in_space_with_end)
    space.contents.add(relation_in_space_not_with_end)
    structure.links_out.add(relation_in_space_with_end)
    structure.links_out.add(relation_in_space_not_with_end)
    structure.links_out.add(relation_not_in_space_with_end)
    assert relation_in_space_with_end in structure.relations_in_space_with(space, end)
    assert relation_in_space_not_with_end not in structure.relations_in_space_with(
        space, end
    )
    assert relation_not_in_space_with_end not in structure.relations_in_space_with(
        space, end
    )


def test_boost_and_update_activation():
    structure = Structure(Mock(), Mock())
    assert 0.0 == structure.activation
    structure.boost_activation(0.5)
    assert 0.0 == structure.activation
    structure.update_activation()
    assert 0.5 == structure.activation
    structure.boost_activation(0.5)
    structure.update_activation()
    assert 1.0 == structure.activation
    structure.boost_activation(0.1)
    structure.update_activation()
    assert 1.0 == structure.activation


def test_decay_and_update_activation():
    structure = Structure(Mock(), Mock())
    assert 0.0 == structure.activation
    structure.boost_activation(1.0)
    structure.update_activation()
    assert 1.0 == structure.activation
    structure.decay_activation(0.5)
    assert 1.0 == structure.activation
    structure.update_activation()
    assert 0.5 == structure.activation
    structure.decay_activation(1.0)
    structure.update_activation()
    assert 0.0 == structure.activation
