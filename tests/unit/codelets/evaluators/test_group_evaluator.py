import math
import pytest
from unittest.mock import Mock

from homer.codelets.evaluators import GroupEvaluator
from homer.codelets.selectors import GroupSelector


FLOATING_POINT_TOLERANCE = 1e-1


@pytest.mark.parametrize("group_value, member_values, expected", [(10, [10, 9], 0.9)])
def test_calculate_confidence(group_value, member_values, expected):
    target_group = Mock()
    target_group.quality = 0.0
    target_group.location = [0, 0, 0]
    target_group.get_value.side_effect = [[group_value] for _ in member_values]
    target_group.members = []
    for member_value in member_values:
        member = Mock()
        member.get_value.side_effect = [[member_value]]
        target_group.members.append(member)
    label = Mock()
    label.parent_concept.space = Mock()
    label.parent_concept.space.relevant_value = "value"
    label.parent_concept.space.proximity_between.side_effect = [
        1.0
        if math.dist([group_value], [member_value]) == 0.0
        else 1 / math.dist([group_value], [member_value])
        for member_value in member_values
    ]
    target_group.labels = [label]
    evaluator = GroupEvaluator(Mock(), Mock(), Mock(), target_group, Mock(), Mock())
    evaluator._calculate_confidence()
    assert math.isclose(
        expected, evaluator.confidence, abs_tol=FLOATING_POINT_TOLERANCE
    )


def test_engender_follow_up():
    target_group = Mock()
    target_group.location = [0, 0, 0]
    bubble_chamber = Mock()
    bubble_chamber.concept_space = {"group-selection": Mock()}
    collection = Mock()
    collection.get_most_active.side_effect = [target_group]
    bubble_chamber.workspace.groups.at.side_effect = [collection]
    evaluator = GroupEvaluator(
        bubble_chamber, Mock(), Mock(), target_group, Mock(), Mock()
    )
    follow_up = evaluator._engender_follow_up()
    assert GroupSelector == type(follow_up)
