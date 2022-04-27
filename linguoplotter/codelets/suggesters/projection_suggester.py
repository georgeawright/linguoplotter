from __future__ import annotations

import statistics

from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets import Suggester
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.id import ID


class ProjectionSuggester(Suggester):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        Suggester.__init__(
            self, codelet_id, parent_id, bubble_chamber, target_structures, urgency
        )
        self.target_view = target_structures.get("target_view")
        self.target_projectee = target_structures.get("target_projectee")
        self.frame = target_structures.get("frame")

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            target_structures,
            urgency,
        )

    @property
    def targets_dict(self):
        return {
            "target_view": self.target_view,
            "target_projectee": self.target_projectee,
            "frame": self.frame,
        }

    def _passes_preliminary_checks(self):
        raise NotImplementedError

    def _calculate_confidence(self):
        self.confidence = (
            statistics.fmean(
                [correspondence.quality for correspondence in self.target_view.members]
            )
            if not self.target_view.members.is_empty()
            else 0.0
        )

    def _fizzle(self):
        pass
