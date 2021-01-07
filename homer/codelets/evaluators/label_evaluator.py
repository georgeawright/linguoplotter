from homer.bubble_chamber import BubbleChamber
from homer.codelets.evaluator import Evaluator
from homer.codelets.selectors import LabelSelector
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structures.links import Label


class LabelEvaluator(Evaluator):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structure: Label,
        urgency: FloatBetweenOneAndZero,
    ):
        Evaluator.__init__(
            self, codelet_id, parent_id, bubble_chamber, target_structure, urgency
        )
        self.original_confidence = self.target_structure.quality

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structure: Label,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(codelet_id, parent_id, bubble_chamber, target_structure, urgency)

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        structure_type = bubble_chamber.concepts["label"]
        target = bubble_chamber.labels.get_active()
        return cls.spawn(parent_id, bubble_chamber, target, structure_type.activation)

    @property
    def _parent_link(self):
        structure_concept = self.bubble_chamber.concepts["label"]
        return structure_concept.relations_with(self._evaluate_concept).get_random()

    def _calculate_confidence(self):
        self.confidence = self.target_structure.parent_concept.classifier.classify(
            {
                "start": self.target_structure.start,
                "concept": self.target_structure.parent_concept,
            }
        )
        self.change_in_confidence = abs(self.confidence - self.original_confidence)

    def _engender_follow_up(self):
        self.child_codelets.append(
            LabelSelector.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.target_structure,
                self.change_in_confidence,
            )
        )
