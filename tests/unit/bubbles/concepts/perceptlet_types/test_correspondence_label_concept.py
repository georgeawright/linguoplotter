import random
from unittest.mock import Mock, patch

from homer.bubble_chamber import BubbleChamber
from homer.codelets.correspondence_labeler import CorrespondenceLabeler
from homer.bubbles.concepts.perceptlet_types import CorrespondenceLabelConcept
from homer.perceptlet_collection import PerceptletCollection


def test_spawn_codelet(target_perceptlet):
    conceptual_space = Mock()
    with patch.object(
        PerceptletCollection, "get_random", return_value=target_perceptlet
    ), patch.object(
        BubbleChamber, "get_random_conceptual_space", return_value=conceptual_space
    ), patch.object(
        random, "random", return_value=-1
    ):
        workspace = Mock()
        workspace.correspondences = PerceptletCollection()
        bubble_chamber = BubbleChamber(Mock(), Mock(), workspace, Mock(), Mock())
        correspondence_label_concept = CorrespondenceLabelConcept()
        codelet = correspondence_label_concept.spawn_codelet(bubble_chamber)
        assert CorrespondenceLabeler == type(codelet)
