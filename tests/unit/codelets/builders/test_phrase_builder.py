import pytest
from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.builders import PhraseBuilder
from homer.codelets.evaluators import PhraseEvaluator
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.nodes import Phrase


@pytest.fixture
def s_concept():
    return Mock()


@pytest.fixture
def np_concept():
    return Mock()


@pytest.fixture
def vp_concept():
    return Mock()


@pytest.fixture
def s_np_vp(s_concept, np_concept, vp_concept):
    rule = Mock()
    rule.activation = 1.0
    rule.root = s_concept
    rule.left_branch = np_concept
    rule.right_branch = vp_concept
    return rule


@pytest.fixture
def prep():
    word = Mock()
    word.name = "prep"
    word.unhappiness = 1
    word.members = StructureCollection()
    return word


@pytest.fixture
def noun():
    word = Mock()
    word.name = "noun"
    word.unhappiness = 1
    word.members = StructureCollection()
    return word


@pytest.fixture
def pp_slot(prep, noun):
    phrase = Mock()
    phrase.name = "pp_slot"
    phrase.unhappiness = 1
    phrase.members = StructureCollection({prep, noun})
    return phrase


@pytest.fixture
def bubble_chamber(s_np_vp, pp_slot, prep, noun):
    chamber = Mock()
    chamber.concepts = {"build": Mock(), "phrase": Mock()}
    chamber.rules = StructureCollection({s_np_vp})
    chamber.text_fragments = StructureCollection({pp_slot, prep, noun})
    chamber.phrases = StructureCollection()
    pp_slot.potential_rule_mates = StructureCollection({prep, noun})
    prep.potential_rule_mates = StructureCollection({pp_slot, noun})
    noun.potential_rule_mates = StructureCollection({pp_slot, prep})
    return chamber


@pytest.fixture
def s(s_concept):
    phrase = Mock()
    phrase.name = "s"
    phrase.is_slot = False
    phrase.quality = 1
    phrase.parent_concept = s_concept
    return phrase


@pytest.fixture
def s_slot(s_concept):
    phrase = Mock()
    phrase.name = "s_slot"
    phrase.is_slot = True
    phrase.quality = 1
    phrase.parent_concept = s_concept
    return phrase


@pytest.fixture
def np(np_concept):
    phrase = Mock()
    phrase.name = "np"
    phrase.is_slot = False
    phrase.quality = 1
    phrase.location = Location([[0], [1]], Mock())
    phrase.parent_concept = np_concept
    return phrase


@pytest.fixture
def vp(vp_concept):
    phrase = Mock()
    phrase.name = "vp"
    phrase.is_slot = False
    phrase.quality = 1
    phrase.location = Location([[2], [3]], Mock())
    phrase.parent_concept = vp_concept
    return phrase


def test_gets_a_rule_if_necessary(bubble_chamber, s_slot, np, vp):
    target_root = s_slot
    target_left_branch = np
    target_right_branch = vp
    target_rule = None
    phrase_builder = PhraseBuilder(
        "",
        "",
        bubble_chamber,
        target_root,
        target_left_branch,
        target_right_branch,
        1.0,
        target_rule=target_rule,
    )
    phrase_builder.run()
    assert phrase_builder.target_rule is not None


def test_successfully_creates_a_branch_slot(bubble_chamber, s, np, s_np_vp):
    target_root = s
    target_left_branch = np
    target_right_branch = None
    target_rule = s_np_vp
    phrase_builder = PhraseBuilder(
        "",
        "",
        bubble_chamber,
        target_root,
        target_left_branch,
        target_right_branch,
        1.0,
        target_rule=target_rule,
    )
    phrase_builder.run()
    assert CodeletResult.SUCCESS == phrase_builder.result
    assert isinstance(phrase_builder.child_structure, Phrase)
    assert len(phrase_builder.child_codelets) == 1
    assert isinstance(phrase_builder.child_codelets[0], PhraseEvaluator)


def test_fails_to_create_a_branch_slot_if_incompatible_with_rule(
    bubble_chamber, s, np, s_np_vp
):
    target_root = s
    target_left_branch = None
    target_right_branch = np
    target_rule = s_np_vp
    phrase_builder = PhraseBuilder(
        "",
        "",
        bubble_chamber,
        target_root,
        target_left_branch,
        target_right_branch,
        1.0,
        target_rule=target_rule,
    )
    phrase_builder.run()
    assert CodeletResult.FIZZLE == phrase_builder.result
    assert phrase_builder.child_structure is None
    assert len(phrase_builder.child_codelets) == 1
    assert isinstance(phrase_builder.child_codelets[0], PhraseBuilder)


def test_successfully_fills_in_a_root_slot(bubble_chamber, s_slot, np, vp, s_np_vp):
    target_root = s_slot
    target_left_branch = np
    target_right_branch = vp
    target_rule = s_np_vp
    phrase_builder = PhraseBuilder(
        "",
        "",
        bubble_chamber,
        target_root,
        target_left_branch,
        target_right_branch,
        1.0,
        target_rule=target_rule,
    )
    phrase_builder.run()
    assert CodeletResult.SUCCESS == phrase_builder.result
    assert phrase_builder.child_structure == s_slot
    assert len(phrase_builder.child_codelets) == 1
    assert isinstance(phrase_builder.child_codelets[0], PhraseEvaluator)


def test_fails_to_fill_root_slot_if_incompatible_with_rule(
    bubble_chamber, s_slot, vp, np, s_np_vp
):
    target_root = s_slot
    target_left_branch = vp
    target_right_branch = np
    target_rule = s_np_vp
    phrase_builder = PhraseBuilder(
        "",
        "",
        bubble_chamber,
        target_root,
        target_left_branch,
        target_right_branch,
        1.0,
        target_rule=target_rule,
    )
    phrase_builder.run()
    assert CodeletResult.FIZZLE == phrase_builder.result
    assert phrase_builder.child_structure is None
    assert len(phrase_builder.child_codelets) == 1
    assert isinstance(phrase_builder.child_codelets[0], PhraseBuilder)


def test_successfully_creates_and_fills_a_root_slot(
    bubble_chamber, np, vp, s_np_vp, s_concept
):
    target_root = None
    target_left_branch = np
    target_right_branch = vp
    target_rule = s_np_vp
    phrase_builder = PhraseBuilder(
        "",
        "",
        bubble_chamber,
        target_root,
        target_left_branch,
        target_right_branch,
        1.0,
        target_rule=target_rule,
    )
    phrase_builder.run()
    assert CodeletResult.SUCCESS == phrase_builder.result
    assert isinstance(phrase_builder.child_structure, Phrase)
    assert phrase_builder.child_structure.parent_concept == s_concept
    assert len(phrase_builder.child_codelets) == 1
    assert isinstance(phrase_builder.child_codelets[0], PhraseEvaluator)


def test_fails_to_create_and_fill_a_root_slot_if_incompatible_with_rule(
    bubble_chamber, vp, np, s_np_vp
):
    target_root = None
    target_left_branch = vp
    target_right_branch = np
    target_rule = s_np_vp
    phrase_builder = PhraseBuilder(
        "",
        "",
        bubble_chamber,
        target_root,
        target_left_branch,
        target_right_branch,
        1.0,
        target_rule=target_rule,
    )
    phrase_builder.run()
    assert CodeletResult.FIZZLE == phrase_builder.result
    assert phrase_builder.child_structure is None
    assert len(phrase_builder.child_codelets) == 1
    assert isinstance(phrase_builder.child_codelets[0], PhraseBuilder)
