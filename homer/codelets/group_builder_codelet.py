from typing import Optional

from homer import fuzzy
from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.concept import Concept
from homer.hyper_parameters import HyperParameters
from homer.perceptlet import Perceptlet

from homer.codelets.group_extender_codelet import GroupExtenderCodelet
from homer.perceptlets.group import Group


class GroupBuilderCodelet(Codelet):

    CONFIDENCE_THRESHOLD = HyperParameters.CONFIDENCE_THRESHOLD

    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        parent_concept: Concept,
        target_perceptlet: Optional[Perceptlet],
        urgency: float,
    ):
        Codelet.__init__(self, bubble_chamber)
        self.parent_concept = parent_concept
        self.target_perceptlet = target_perceptlet
        self.urgency = urgency

    def run(self) -> Optional[Codelet]:
        neighbour = self.target_perceptlet.get_random_neighbour()
        confidence_of_group_affinity = self._calculate_confidence(
            self.target_perceptlet, neighbour
        )
        if confidence_of_group_affinity > self.CONFIDENCE_THRESHOLD:
            group = self.bubble_chamber.create_group(
                [self.target_perceptlet, neighbour], confidence_of_group_affinity
            )
            self.target_perceptlet.add_group(group)
            self.neighbour.add_group(group)
            return self.engender_follow_up(confidence_of_group_affinity)
        return None

    def _calculate_confidence(
        self, perceptlet_a: Perceptlet, perceptlet_b: Perceptlet,
    ) -> float:
        common_concepts = {
            label.parent_concept for label in perceptlet_a.labels
        }.intersection({label.parent_concept for label in perceptlet_b.labels})
        distances = [
            concept.distance_between(perceptlet_a.value, perceptlet_b.value)
            for concept in common_concepts
        ]
        return fuzzy.OR(distances)

    def engender_follow_up(self, group: Group, confidence: float) -> Codelet:
        return GroupExtenderCodelet(self.bubble_chamber, group, confidence)
