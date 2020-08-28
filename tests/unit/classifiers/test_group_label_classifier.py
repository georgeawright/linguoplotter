import math
import pytest
from unittest.mock import Mock

from homer.classifiers import GroupLabelClassifier

FLOAT_COMPARISON_TOLERANCE = 1e-1


@pytest.mark.parametrize(
    "label_strengths, group_size, expected",
    [([0.5, 0.5], 2, 0.5), ([0.5, 0.5], 4, 0.25)],
)
def test_calculate_confidence(label_strengths, group_size, expected):
    concept = Mock()
    group = Mock()
    group.location = [0, 0, 0]
    group.size = group_size
    group.members = set()
    for label_strength in label_strengths:
        label = Mock()
        label.parent_concept = concept
        label.activation.as_scalar.side_effect = [label_strength]
        member = Mock()
        member.labels = {label}
        group.members.add(member)
    classifier = GroupLabelClassifier()
    confidence = classifier.confidence(group, concept)
    assert math.isclose(expected, confidence, abs_tol=FLOAT_COMPARISON_TOLERANCE)
