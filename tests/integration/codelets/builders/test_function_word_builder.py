import math
import pytest
from unittest.mock import Mock

from homer.bubble_chamber import BubbleChamber
from homer.codelet_result import CodeletResult
from homer.codelets.builders import WordBuilder, FunctionWordBuilder
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Concept
from homer.structures.chunks import View, Word
from homer.structures.chunks.slots import TemplateSlot
from homer.structures.links import Correspondence
from homer.structures.spaces import ConceptualSpace, WorkingSpace
from homer.structures.spaces.frames import Template


@pytest.fixture
def bubble_chamber():
    chamber = BubbleChamber(
        Mock(),
        Mock(),
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
    text_concept = Concept(
        "text", None, None, None, "value", StructureCollection(), None
    )
    chamber.concepts.add(text_concept)
    same_concept = Concept(
        "same", None, None, None, "value", StructureCollection(), None
    )
    chamber.concepts.add(same_concept)
    input_concept = Concept(
        "input", None, None, None, "value", StructureCollection(), None
    )
    chamber.concepts.add(input_concept)
    text_space = ConceptualSpace("text", StructureCollection(), text_concept)
    chamber.spaces.add(text_space)
    return chamber


@pytest.fixture
def output_space(bubble_chamber):
    name = "output space name"
    members = StructureCollection()
    quality = 0.0
    parent_concept = bubble_chamber.concepts["text"]
    space = WorkingSpace(name, members, quality, parent_concept)
    return space


@pytest.fixture
def template_word():
    word = Word(Mock(), Mock(), Mock(), Mock())
    return word


@pytest.fixture
def template(bubble_chamber, template_word):
    name = "mock template"
    members = StructureCollection({template_word})
    parent_concept = bubble_chamber.concepts["text"]
    template = Template(name, members, parent_concept)
    bubble_chamber.spaces.add(template)
    return template


def test_successful_adds_member_to_chunk_and_spawns_follow_up_and_same_chunk_cannot_be_recreated(
    bubble_chamber,
    template,
    output_space,
):
    parent_id = ""
    urgency = 1.0

    builder = FunctionWordBuilder.spawn(
        parent_id, bubble_chamber, template, output_space, urgency
    )
    builder.run()
    assert CodeletResult.SUCCESS == builder.result
    assert isinstance(builder.child_structure, Word)
    assert isinstance(builder.child_codelets[0], FunctionWordBuilder)
    builder = FunctionWordBuilder.spawn(
        parent_id, bubble_chamber, template, output_space, urgency
    )
    builder.run()
    assert CodeletResult.FIZZLE == builder.result