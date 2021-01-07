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
from homer.structures.links import Correspondence, Relation
from homer.structures.spaces import WorkingSpace
from homer.structures.spaces.frames import Template


@pytest.fixture
def bubble_chamber():
    chamber = BubbleChamber(
        StructureCollection(),
        StructureCollection(),
        StructureCollection(),
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
    word_concept = Concept(
        Mock(), Mock(), "word", None, None, None, "value", StructureCollection(), None
    )
    chamber.concepts.add(word_concept)
    build_concept = Concept(
        Mock(), Mock(), "build", None, None, None, "value", StructureCollection(), None
    )
    chamber.concepts.add(build_concept)
    relation = Relation(Mock(), Mock(), word_concept, build_concept, None, None, 1)
    word_concept.links_out.add(relation)
    build_concept.links_in.add(relation)
    text_concept = Concept(
        Mock(), Mock(), "text", None, None, None, "value", StructureCollection(), None
    )
    chamber.concepts.add(text_concept)
    same_concept = Concept(
        Mock(), Mock(), "same", None, None, None, "value", StructureCollection(), None
    )
    chamber.concepts.add(same_concept)
    input_concept = Concept(
        Mock(), Mock(), "input", None, None, None, "value", StructureCollection(), None
    )
    chamber.concepts.add(input_concept)
    return chamber


@pytest.fixture
def target_view(bubble_chamber):
    members = Mock()
    parent_space = Mock()
    output_space = WorkingSpace(
        Mock(),
        Mock(),
        "output_space_name",
        StructureCollection(),
        0.0,
        bubble_chamber.concepts["text"],
    )
    quality = Mock()
    view = View(Mock(), Mock(), members, parent_space, output_space, quality)
    bubble_chamber.spaces.add(output_space)
    return view


@pytest.fixture
def template(bubble_chamber):
    name = "mock template"
    members = StructureCollection()
    parent_concept = bubble_chamber.concepts["text"]
    template = Template(Mock(), Mock(), name, members, parent_concept)
    bubble_chamber.spaces.add(template)
    return template


@pytest.fixture
def input_space(bubble_chamber):
    name = "input space"
    contents = StructureCollection()
    quality = 0.0
    parent_concept = bubble_chamber.concepts["input"]
    space = WorkingSpace(Mock(), Mock(), name, contents, quality, parent_concept)
    return space


@pytest.fixture
def target_correspondence(template, input_space):
    start = TemplateSlot(Mock(), Mock(), Mock(), Mock(), Mock(), Mock())
    end = Mock()
    start_space = template
    end_space = input_space
    parent_concept = Mock()
    parent_space = Mock()
    conceptual_space = Mock()
    quality = Mock()
    correspondence = Correspondence(
        Mock(),
        Mock(),
        start,
        end,
        start_space,
        end_space,
        parent_concept,
        parent_space,
        conceptual_space,
        quality,
    )
    correspondence._activation = 1.0
    return correspondence


@pytest.mark.skip
def test_successful_adds_member_to_chunk_and_spawns_follow_up_and_same_chunk_cannot_be_recreated(
    bubble_chamber, target_view, target_correspondence
):
    parent_id = ""
    urgency = 1.0

    builder = WordBuilder.spawn(
        parent_id, bubble_chamber, target_view, target_correspondence, urgency
    )
    builder.run()
    assert CodeletResult.SUCCESS == builder.result
    assert isinstance(builder.child_structure, Word)
    assert isinstance(builder.child_codelets[0], FunctionWordBuilder)
    builder = WordBuilder.spawn(
        parent_id, bubble_chamber, target_view, target_correspondence, urgency
    )
    builder.run()
    assert CodeletResult.FIZZLE == builder.result
