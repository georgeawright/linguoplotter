from homer import fuzzy
from homer.bubble_chamber import BubbleChamber
from homer.codelets.evaluators import ProjectionEvaluator
from homer.errors import MissingStructureError
from homer.structure_collection import StructureCollection


class RelationProjectionEvaluator(ProjectionEvaluator):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.selectors.projection_selectors import (
            RelationProjectionSelector,
        )

        return RelationProjectionSelector

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber):
        structure_type = bubble_chamber.concepts["relation"]
        input_concept = bubble_chamber.concepts["input"]
        view = bubble_chamber.new_structure_collection(
            view
            for view in bubble_chamber.views
            if view.output_space.parent_concept == input_concept
            and not view.contents.where(is_relation=True).is_empty()
        ).get()
        relation = view.ouptut_space.contents.where(is_relation=True).get()
        correspondences = relation.correspondences.where(end=relation)
        target_structures = StructureCollection.union(
            bubble_chamber.new_structure_collection({relation}), correspondences
        )
        return cls.spawn(
            parent_id,
            bubble_chamber,
            target_structures,
            structure_type.activation,
        )

    @property
    def _parent_link(self):
        structure_concept = self.bubble_chamber.concepts["relation"]
        return structure_concept.relations_with(self._evaluate_concept).get()

    def _calculate_confidence(self):
        try:
            non_frame_item = (
                self.target_structures.where(is_correspondence=True)
                .filter(lambda x: not x.start.is_slot)
                .get()
                .start
            )
            frame_item = (
                self.target_structures.where(is_correspondence=True)
                .filter(lambda x: x.start.is_slot)
                .get()
                .start
            )
            correspondence_to_frame = non_frame_item.correspondences_with(
                frame_item
            ).get()
            self.confidence = fuzzy.AND(
                non_frame_item.quality, correspondence_to_frame.quality
            )
        except MissingStructureError:
            self.confidence = 1.0
        self.change_in_confidence = abs(self.confidence - self.original_confidence)
