import pytest
import random
from unittest.mock import Mock, patch

from homer.codelet_result import CodeletResult
from homer.codelets.builders.phrase_builders import PhraseProjectionBuilder
from homer.codelets.selectors.phrase_selectors import PhraseProjectionSelector
from homer.structure_collection import StructureCollection
from homer.tools import hasinstance


@pytest.fixture
def target_view():
    correspondence = Mock()
    correspondence.start.has_correspondence_to_space.return_value = False
    view = Mock()
    view.members = StructureCollection({correspondence})
    return view


@pytest.fixture
def bubble_chamber(target_view):
    chamber = Mock()
    chamber.concepts = {"phrase": Mock(), "select": Mock()}
    chamber.discourse_views = StructureCollection({target_view})
    return chamber


@pytest.mark.parametrize(
    "champion_quality, champion_activation, "
    + "challenger_quality, challenger_activation, "
    + "random_number, expected_winner",
    [
        (1.0, 0.5, 0.0, 0.5, 0.5, "champion"),  # champion is better
        (0.5, 1.0, 1.0, 0.0, 0.5, "challenger"),  # challenger is better
        (0.5, 1.0, 1.0, 0.0, 0.1, "champion"),  # challenger is better but rand too low
        (1.0, 1.0, 0.5, 0.0, 0.9, "challenger"),  # champion is better but rand too high
    ],
)
def test_winner_is_boosted_follow_up_is_spawned(
    champion_quality,
    champion_activation,
    challenger_quality,
    challenger_activation,
    random_number,
    expected_winner,
    bubble_chamber,
):
    with patch.object(random, "random", return_value=random_number):
        champion = Mock()
        champion.size = 2
        champion.quality = champion_quality
        champion.activation = champion_activation
        challenger = Mock()
        challenger.size = 2
        challenger.quality = challenger_quality
        challenger.activation = challenger_activation
        selector = PhraseProjectionSelector(
            Mock(),
            Mock(),
            bubble_chamber,
            StructureCollection({champion}),
            Mock(),
            challengers=StructureCollection({challenger}),
        )
        selector.run()
        assert CodeletResult.SUCCESS == selector.result
        if expected_winner == "champion":
            assert champion.boost_activation.is_called()
            assert challenger.decay_activation.is_called()
        else:
            assert challenger.boost_activation.is_called()
            assert champion.decay_activation.is_called()
        assert 2 == len(selector.child_codelets)
        assert hasinstance(selector.child_codelets, PhraseProjectionBuilder)
        assert hasinstance(selector.child_codelets, PhraseProjectionSelector)