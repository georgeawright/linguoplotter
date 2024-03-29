import pytest
from unittest.mock import Mock

from linguoplotter.codelet_result import CodeletResult
from linguoplotter.codelets.builders import ChunkBuilder
from linguoplotter.codelets.evaluators import ChunkEvaluator
from linguoplotter.structure_collection import StructureCollection
from linguoplotter.structures.links import Label
from linguoplotter.structures.nodes import Chunk
from linguoplotter.tools import hasinstance


@pytest.fixture
def bubble_chamber():
    chamber = Mock()
    chamber.satisfaction = 0.0
    chamber.concepts = {"build": Mock(), "chunk": Mock()}
    chamber.chunks = StructureCollection()
    return chamber


@pytest.fixture
def target_space():
    space = Mock()
    space.conceptual_spaces = [Mock()]
    return space


@pytest.fixture
def target_slot():
    chunk = Mock()
    chunk.is_slot = True
    return chunk


@pytest.fixture
def target_rule():
    rule = Mock()
    root_concept = Mock()
    rule.root_concept = root_concept
    rule.left_concept = root_concept
    rule.right_concept = None
    rule.compatibility_with.return_value = 1.0
    return rule


@pytest.fixture
def target_root(target_slot, target_rule):
    chunk = Mock()
    chunk.members = StructureCollection({target_slot})
    chunk.rule = target_rule
    chunk.locations = [Mock()]
    return chunk


@pytest.fixture
def target_node(target_root):
    chunk = Mock()
    chunk.is_slot = False
    chunk.super_chunks = StructureCollection({target_root})
    target_root.members.add(chunk)
    return chunk


@pytest.fixture
def target_slot_filler():
    chunk = Mock()
    chunk.is_slot = False
    return chunk


@pytest.fixture
def test_fizzles_if_chunk_exists(bubble_chamber, target_node):
    target_rule = Mock()
    existing_chunk = Mock()
    existing_chunk.rule = target_rule
    target_slot_filler = Mock()
    existing_chunk.members = StructureCollection({target_node, target_slot_filler})
    bubble_chamber.chunks.add(existing_chunk)
    target_space = Mock()
    contents_where = Mock()
    contents_where.at = StructureCollection({target_slot_filler})
    target_space.contents.where.return_value = contents_where
    target_structures = {
        "target_space": Mock(),
        "target_rule": target_rule,
        "target_root": None,
        "target_node": target_node,
        "target_slot": None,
        "target_slot_filler": None,
        "target_branch": "left",
    }
    urgency = 1
    builder = ChunkBuilder("", "", bubble_chamber, target_structures, urgency)
    builder.run()
    assert CodeletResult.FIZZLE == builder.result


@pytest.fixture
def test_creates_new_chunk_if_necessary(
    bubble_chamber, target_space, target_rule, target_node
):
    target_structures = {
        "target_space": target_space,
        "target_rule": target_rule,
        "target_root": None,
        "target_node": target_node,
        "target_slot": None,
        "target_slot_filler": None,
        "target_branch": "left",
    }
    urgency = 1
    builder = ChunkBuilder("", "", bubble_chamber, target_structures, urgency)
    builder.run()
    assert CodeletResult.FINISH == builder.result
    assert 2 == len(builder.child_structures)
    assert hasinstance(builder.child_structures, Chunk)


@pytest.fixture
def test_fills_slot_if_necessary(
    bubble_chamber,
    target_rule,
    target_root,
    target_node,
    target_slot,
    target_slot_filler,
):
    target_rule.right_concept = None
    target_structures = {
        "target_space": Mock(),
        "target_rule": target_rule,
        "target_root": target_root,
        "target_node": target_node,
        "target_slot": target_slot,
        "target_slot_filler": target_slot_filler,
        "target_branch": "left",
    }
    urgency = 1
    target_root.has_free_branch = False
    assert target_slot_filler not in target_root.members
    builder = ChunkBuilder("", "", bubble_chamber, target_structures, urgency)
    builder.run()
    assert CodeletResult.FINISH == builder.result
    assert target_slot_filler in target_root.members
    assert target_slot not in target_root.members


@pytest.fixture
def test_leaves_slot_if_appropriate(
    bubble_chamber,
    target_rule,
    target_root,
    target_node,
    target_slot,
    target_slot_filler,
):
    target_structures = {
        "target_space": Mock(),
        "target_rule": target_rule,
        "target_root": target_root,
        "target_node": target_node,
        "target_slot": target_slot,
        "target_slot_filler": target_slot_filler,
        "target_branch": "left",
    }
    urgency = 1
    assert target_slot_filler not in target_root.members
    builder = ChunkBuilder("", "", bubble_chamber, target_structures, urgency)
    builder.run()
    assert CodeletResult.FINISH == builder.result
    assert target_slot_filler in target_root.members
    assert target_slot in target_root.members
