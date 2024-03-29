import pytest
from unittest.mock import Mock

from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.location import Location
from linguoplotter.structure import Structure
from linguoplotter.structures.links import Correspondence, Label, Relation
from linguoplotter.structures.nodes import Chunk, Concept, Rule


@pytest.mark.skip
def test_spreading_activation():
    bubble_chamber = BubbleChamber.setup(Mock())

    contextual_space = Mock()
    contextual_space.quality = 0.5
    bubble_chamber.contextual_spaces.add(contextual_space)

    conceptual_space = Mock()
    concept_a = Concept(
        "",
        "",
        "a",
        [Location([], conceptual_space)],
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
    )
    concept_b = Concept(
        "",
        "",
        "b",
        [Location([], conceptual_space)],
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
    )
    concept_c = Concept(
        "",
        "",
        "c",
        [Location([], conceptual_space)],
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
    )
    concept_d = Concept(
        "",
        "",
        "d",
        [Location([], conceptual_space)],
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
    )
    c_to_d = Relation(
        "",
        "",
        concept_c,
        bubble_chamber.new_structure_collection(concept_c, concept_d),
        Mock(),
        conceptual_space,
        Mock(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
    )
    c_to_d._activation = 1.0
    concept_c.links_out.add(c_to_d)
    concept_d.links_in.add(c_to_d)
    rule_a_b_c = Rule(
        "",
        "",
        "a-->b,c",
        Location([], conceptual_space),
        concept_a,
        concept_b,
        concept_c,
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
    )
    a_to_rule = Relation(
        "",
        "",
        concept_a,
        bubble_chamber.new_structure_collection(concept_a, rule_a_b_c),
        Mock(),
        conceptual_space,
        Mock(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
    )
    a_to_rule._activation = 1.0
    concept_a.links_out.add(a_to_rule)
    rule_a_b_c.links_in.add(a_to_rule)
    rule_to_b = Relation(
        "",
        "",
        rule_a_b_c,
        bubble_chamber.new_structure_collection(rule_a_b_c, concept_b),
        Mock(),
        conceptual_space,
        Mock(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
    )
    rule_to_b._activation = 1.0
    rule_a_b_c.links_out.add(rule_to_b)
    concept_b.links_in.add(rule_to_b)
    rule_to_c = Relation(
        "",
        "",
        rule_a_b_c,
        bubble_chamber.new_structure_collection(rule_a_b_c, concept_c),
        Mock(),
        conceptual_space,
        Mock(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
    )
    rule_to_c._activation = 1.0
    rule_a_b_c.links_out.add(rule_to_c)
    concept_c.links_in.add(rule_to_c)
    chunk = Chunk(
        "",
        "",
        [Location([], conceptual_space)],
        Mock(),
        Mock(),
        Mock(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        Mock(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
    )
    label_a = Label(
        "",
        "",
        chunk,
        bubble_chamber.new_structure_collection(chunk),
        concept_b,
        conceptual_space,
        Mock(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
        bubble_chamber.new_structure_collection(),
    )
    chunk.links_out.add(label_a)

    bubble_chamber.concepts.add(concept_a)
    bubble_chamber.concepts.add(concept_b)
    bubble_chamber.concepts.add(concept_c)
    bubble_chamber.concepts.add(concept_d)
    bubble_chamber.rules.add(rule_a_b_c)
    bubble_chamber.chunks.add(chunk)
    bubble_chamber.labels.add(label_a)

    concept_a_last_activation = concept_a.activation
    concept_b_last_activation = concept_b.activation
    concept_c_last_activation = concept_c.activation
    concept_d_last_activation = concept_d.activation
    rule_a_b_c_last_activation = rule_a_b_c.activation
    chunk_last_activation = chunk.activation
    label_a_last_activation = label_a.activation

    bubble_chamber.spread_activations()
    bubble_chamber.update_activations()

    assert concept_b.activation > concept_b_last_activation

    assert concept_a.activation == concept_a_last_activation
    assert concept_c.activation == concept_c_last_activation
    assert concept_d.activation == concept_d_last_activation
    assert rule_a_b_c.activation == rule_a_b_c_last_activation
    assert chunk.activation == chunk_last_activation
    assert label_a.activation == label_a_last_activation

    concept_b._activation = 1.0
    concept_b_last_activation = concept_b.activation

    bubble_chamber.spread_activations()
    bubble_chamber.update_activations()

    assert rule_a_b_c.activation > rule_a_b_c_last_activation

    assert concept_a.activation == concept_a_last_activation
    assert concept_b.activation == concept_b_last_activation
    assert concept_c.activation == concept_c_last_activation
    assert concept_d.activation == concept_d_last_activation
    assert chunk.activation == chunk_last_activation
    assert label_a.activation == label_a_last_activation

    rule_a_b_c._activation = 1.0
    rule_a_b_c_last_activation = rule_a_b_c.activation

    bubble_chamber.spread_activations()
    bubble_chamber.update_activations()

    assert concept_a.activation > concept_a_last_activation
    assert concept_c.activation > concept_c_last_activation

    assert concept_b.activation == concept_b_last_activation
    assert concept_d.activation == concept_d_last_activation
    assert rule_a_b_c.activation == rule_a_b_c_last_activation
    assert chunk.activation == chunk_last_activation
    assert label_a.activation == label_a_last_activation

    concept_c._activation = 1.0
    concept_c_last_activation = concept_c.activation
    concept_a._activation = 1.0
    concept_a_last_activation = concept_a.activation

    bubble_chamber.spread_activations()
    bubble_chamber.update_activations()

    assert concept_d.activation > concept_d_last_activation

    assert concept_a.activation == concept_a_last_activation
    assert concept_b.activation == concept_b_last_activation
    assert concept_c.activation == concept_c_last_activation
    assert rule_a_b_c.activation == rule_a_b_c_last_activation
    assert chunk.activation == chunk_last_activation
    assert label_a.activation == label_a_last_activation
