import pytest
from unittest.mock import Mock

from homer.codelet_result import CodeletResult
from homer.codelets.builders.view_builders import DiscourseViewBuilder
from homer.codelets.evaluators.view_evaluators import DiscourseViewEvaluator
from homer.structure_collection import StructureCollection
from homer.structures.spaces import Frame
from homer.structures.views import DiscourseView
from homer.tools import hasinstance


@pytest.fixture
def bubble_chamber():
    chamber = Mock()
    chamber.has_view.return_value = False
    chamber.concepts = {
        "build": Mock(),
        "view-discourse": Mock(),
        "text": Mock(),
        "discourse": Mock(),
    }
    chamber.spaces = {"text": Mock(), "top level working": Mock(), "input": Mock()}
    chamber.views = StructureCollection()
    return chamber


@pytest.fixture
def input_space():
    space = Mock()
    space.activation = 1.0
    return space


@pytest.fixture
def frame():
    space = Frame(Mock(), Mock(), Mock(), Mock(), Mock(), Mock(), Mock())
    space.activation = 1.0
    return space


def test_successful_creates_view_and_spawns_follow_up(
    bubble_chamber, input_space, frame
):
    view_builder = DiscourseViewBuilder(
        Mock(),
        Mock(),
        bubble_chamber,
        StructureCollection({input_space, frame}),
        Mock(),
    )
    result = view_builder.run()
    assert CodeletResult.SUCCESS == result
    assert hasinstance(view_builder.child_structures, DiscourseView)
    assert len(view_builder.child_codelets) == 1
    assert isinstance(view_builder.child_codelets[0], DiscourseViewEvaluator)


def test_fails_when_space_activations_are_low(bubble_chamber, input_space, frame):
    input_space.activation = 0.1
    frame.activation = 0.1
    view_builder = DiscourseViewBuilder(
        Mock(), Mock(), bubble_chamber, StructureCollection({input_space, frame}), 1.0
    )
    result = view_builder.run()
    assert CodeletResult.FAIL == result
    assert len(view_builder.child_codelets) == 1
    assert isinstance(view_builder.child_codelets[0], DiscourseViewBuilder)