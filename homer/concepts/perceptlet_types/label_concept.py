import random
from typing import Optional

from homer.bubble_chamber import BubbleChamber
from homer.codelets.bottom_up_raw_perceptlet_labeler import BottomUpRawPerceptletLabeler
from homer.concept import Concept
from homer.concepts.perceptlet_type import PerceptletType
from homer.workspace_location import WorkspaceLocation


class LabelConcept(PerceptletType):
    def __init__(self, name: str = "label"):
        PerceptletType.__init__(self, name)

    def spawn_codelet(
        self, bubble_chamber: BubbleChamber
    ) -> Optional[BottomUpRawPerceptletLabeler]:
        if self.activation_pattern.is_high():
            target_perceptlet = bubble_chamber.get_unhappy_raw_perceptlet()
            return BottomUpRawPerceptletLabeler(
                bubble_chamber,
                self,
                target_perceptlet,
                target_perceptlet.exigency,
                self.concept_id,
            )

    def spawn_top_down_codelet(
        self,
        bubble_chamber: BubbleChamber,
        location: WorkspaceLocation,
        parent_concept: Concept,
    ):
        raise NotImplementedError
