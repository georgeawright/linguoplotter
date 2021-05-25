import pytest
from unittest.mock import Mock, patch

from homer.codelet_result import CodeletResult
from homer.codelets.builders.phrase_builders import PhraseProjectionBuilder
from homer.codelets.suggesters.phrase_suggesters import PhraseProjectionSuggester
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.links import Correspondence
from homer.structures.nodes import Phrase
from homer.tools import hasinstance


@pytest.fixture
def bubble_chamber():
    chamber = Mock()
    chamber.concepts = {"suggest": Mock(), "same": Mock(), "phrase": Mock()}
    chamber.discourse_views = StructureCollection()
    return chamber


@pytest.fixture
def frame():
    frame = Mock()
    return frame


@pytest.fixture
def input_space():
    space = Mock()
    return space


@pytest.fixture
def output_space():
    space = Mock()
    return space


@pytest.fixture
def target_view(bubble_chamber, frame):
    correspondence = Mock()
    correspondence.start.has_correspondence_to_space.return_value = False
    view = Mock()
    view.activation = 1.0
    view.members = StructureCollection({correspondence})
    view.input_frames = StructureCollection({frame})
    bubble_chamber.discourse_views.add(view)
    return view


@pytest.fixture
def word_1():
    word = Mock()
    word.lexeme = Mock()
    word.word_form = Mock()
    word.lexeme.forms = {word.word_form: Mock()}
    word.location.coordinates = [[0]]
    return word


@pytest.fixture
def word_2():
    word = Mock()
    word.lexeme = Mock()
    word.word_form = Mock()
    word.lexeme.forms = {word.word_form: Mock()}
    word.location.coordinates = [[1]]
    return word


@pytest.fixture
def original_phrase(word_1, word_2):
    phrase = Mock()
    phrase.is_word = False
    phrase.is_phrase = True
    phrase.left_branch = word_1
    phrase.right_branch = word_2
    return phrase


@pytest.fixture
def target_correspondence(target_view, input_space, frame, original_phrase):
    correspondence = Mock()
    correspondence.activation = 1.0
    correspondence.start = original_phrase
    correspondence.start_space = input_space
    correspondence.end_space = frame
    correspondence.parent_view = target_view
    correspondence.start.has_correspondence_to_space.return_value = False
    target_view.members.add(correspondence)
    return correspondence


def test_gives_high_confidence_for_highly_activated_correspondence(
    bubble_chamber, target_correspondence
):
    target_structures = {"target_correspondence": target_correspondence}
    suggester = PhraseProjectionSuggester(
        Mock(), Mock(), bubble_chamber, target_structures, 1
    )
    result = suggester.run()
    assert CodeletResult.SUCCESS == result
    assert suggester.confidence == 1
    assert 1 == len(suggester.child_codelets)
    assert isinstance(suggester.child_codelets[0], PhraseProjectionBuilder)


def test_fizzles_if_phrase_already_has_correspondence_in_output(
    bubble_chamber, target_correspondence
):
    target_correspondence.start.has_correspondence_to_space.return_value = True
    target_structures = {"target_correspondence": target_correspondence}
    suggester = PhraseProjectionSuggester("", "", bubble_chamber, target_structures, 1)
    suggester.run()
    assert CodeletResult.FIZZLE == suggester.result