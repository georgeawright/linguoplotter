from unittest.mock import Mock, patch

from homer.bubble_chamber import BubbleChamber
from homer.codelets import CorrespondenceBuilder, CorrespondenceSuggester


def test_engender_follow_up():
    correspondence_suggester = CorrespondenceSuggester(
        Mock(), Mock(), Mock(), Mock(), Mock(), Mock(),
    )
    correspondence_suggester.parent_concept = Mock()
    follow_up = correspondence_suggester._engender_follow_up()
    assert CorrespondenceBuilder == type(follow_up)


def test_engender_fail():
    with patch.object(
        BubbleChamber, "get_random_groups", return_value=[Mock(), Mock()]
    ):
        bubble_chamber = BubbleChamber(Mock(), Mock(), Mock(), Mock(), Mock())
        correspondence_suggester = CorrespondenceSuggester(
            bubble_chamber, Mock(), Mock(), Mock(), 1, Mock()
        )
        alternative_follow_up = correspondence_suggester._fail()
        assert CorrespondenceSuggester == type(alternative_follow_up)
