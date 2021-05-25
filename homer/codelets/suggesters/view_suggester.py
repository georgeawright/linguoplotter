from __future__ import annotations
from abc import abstractclassmethod
import statistics

from homer.bubble_chamber import BubbleChamber
from homer.codelets import Suggester
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure_collection import StructureCollection
from homer.structures.spaces import Frame


class ViewSuggester(Suggester):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_spaces: StructureCollection,
        urgency: FloatBetweenOneAndZero,
    ):
        Suggester.__init__(
            self, codelet_id, parent_id, bubble_chamber, target_spaces, urgency
        )
        self.target_spaces = target_spaces
        self.second_target_view = None
        self.correspondences = None
        self.correspondences_to_add = None
        self.frame = None

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_spaces: StructureCollection,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            target_spaces,
            urgency,
        )

    @abstractclassmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber, urgency: float = None):
        pass

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["view"]

    @property
    def target_structures(self):
        return self.target_spaces

    def _passes_preliminary_checks(self):
        if self.frame is None:
            for space in self.target_spaces:
                if isinstance(space, Frame):
                    self.frame = space
        return True

    def _calculate_confidence(self):
        self.confidence = statistics.fmean(
            [space.activation for space in self.target_spaces]
        )

    def _fizzle(self):
        pass