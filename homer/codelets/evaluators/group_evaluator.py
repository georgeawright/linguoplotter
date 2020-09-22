import statistics

from homer.bubble_chamber import BubbleChamber
from homer.bubbles import Perceptlet
from homer.bubbles.concepts.perceptlet_type import PerceptletType
from homer.codelets.evaluator import Evaluator
from homer.codelets.selectors.group_selector import GroupSelector


class GroupEvaluator(Evaluator):
    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        perceptlet_type: PerceptletType,
        target_type: PerceptletType,
        target_group: Perceptlet,
        urgency: float,
        parent_id: str,
    ):
        Evaluator.__init__(
            self,
            bubble_chamber,
            perceptlet_type,
            target_type,
            target_group,
            urgency,
            parent_id,
        )
        self.target_group = target_group

    def _passes_preliminary_checks(self) -> bool:
        return len(self.target_group.labels) > 0

    def _calculate_confidence(self):
        conceptual_spaces = {
            label.parent_concept.space for label in self.target_group.labels
        }
        proximities = [
            space.proximity_between(
                self.target_group.get_value(space), member.get_value(space)
            )
            for space in conceptual_spaces
            for member in self.target_group.members
        ]
        quality_estimate = statistics.fmean(proximities)
        # or fuzzy.AND?
        self.confidence = quality_estimate - self.target_group.quality

    def _engender_follow_up(self) -> GroupSelector:
        return GroupSelector(
            self.bubble_chamber,
            self.bubble_chamber.concept_space["group-selection"],
            self.target_type,
            self.bubble_chamber.workspace.groups.at(self.location).get_most_active(),
            self.urgency,
            self.codelet_id,
        )