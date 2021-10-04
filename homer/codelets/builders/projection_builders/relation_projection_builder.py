from homer.id import ID
from homer.codelets.builders import ProjectionBuilder
from homer.structure_collection import StructureCollection
from homer.structures.links import Correspondence, Relation


class RelationProjectionBuilder(ProjectionBuilder):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.evaluators.projection_evaluators import (
            RelationProjectionEvaluator,
        )

        return RelationProjectionEvaluator

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["relation"]

    def _process_structure(self):
        start_correspondence = self.target_projectee.start.correspondences_to_space(
            self.target_view.output_space
        ).get()
        corresponding_start = start_correspondence.end
        end_correspondence = self.target_projectee.end.correspondences_to_space(
            self.target_view.output_space
        ).get()
        corresponding_end = end_correspondence.end
        parent_concept = self.target_view.slot_values[
            self.frame_correspondee.structure_id
        ]
        conceptual_location = self.target_projectee.location_in_space(
            parent_concept.parent_space
        )
        output_location = corresponding_start.location_in_space(
            self.target_view.output_space
        )
        locations = [conceptual_location, output_location]
        relation = Relation(
            ID.new(Relation),
            self.codelet_id,
            corresponding_start,
            corresponding_end,
            parent_concept,
            locations,
            0.0,
        )
        corresponding_start.links_out.add(relation)
        corresponding_end.links_in.add(relation)
        self.bubble_chamber.relations.add(relation)
        self.bubble_chamber.logger.log(relation)
        for location in [output_location, conceptual_location]:
            location.space.add(relation)
            self.bubble_chamber.logger.log(location.space)
        frame_to_output_correspondence = Correspondence(
            ID.new(Correspondence),
            self.codelet_id,
            start=self.target_projectee,
            end=relation,
            locations=[self.target_projectee.location, relation.location],
            parent_concept=self.bubble_chamber.concepts["same"],
            conceptual_space=self.bubble_chamber.conceptual_spaces["grammar"],
            parent_view=self.target_view,
            quality=0.0,
        )
        self.child_structures = StructureCollection(
            {relation, frame_to_output_correspondence}
        )
        self.bubble_chamber.correspondences.add(frame_to_output_correspondence)
        self.bubble_chamber.logger.log(frame_to_output_correspondence)
        self.target_view.members.add(frame_to_output_correspondence)
        self.target_projectee.links_in.add(frame_to_output_correspondence)
        self.target_projectee.links_out.add(frame_to_output_correspondence)
        relation.links_in.add(frame_to_output_correspondence)
        relation.links_out.add(frame_to_output_correspondence)
        for location in frame_to_output_correspondence.locations:
            location.space.add(frame_to_output_correspondence)
        if self.target_projectee.is_slot:
            non_frame_to_output_correspondence = Correspondence(
                ID.new(Correspondence),
                self.codelet_id,
                start=self.non_frame_correspondee,
                end=relation,
                locations=[
                    self.non_frame_correspondee.location_in_space(self.non_frame),
                    relation.location,
                ],
                parent_concept=self.bubble_chamber.concepts["same"],
                conceptual_space=self.target_correspondence.conceptual_space,
                parent_view=self.target_view,
                quality=0.0,
            )
            self.child_structures.add(non_frame_to_output_correspondence)
            self.bubble_chamber.correspondences.add(non_frame_to_output_correspondence)
            self.bubble_chamber.logger.log(non_frame_to_output_correspondence)
            self.target_view.members.add(non_frame_to_output_correspondence)
            relation.links_in.add(non_frame_to_output_correspondence)
            relation.links_out.add(non_frame_to_output_correspondence)
            self.non_frame_correspondee.links_in.add(non_frame_to_output_correspondence)
            self.non_frame_correspondee.links_out.add(
                non_frame_to_output_correspondence
            )
            self.bubble_chamber.logger.log(non_frame_to_output_correspondence)
            for location in non_frame_to_output_correspondence.locations:
                location.space.add(non_frame_to_output_correspondence)
        self.bubble_chamber.logger.log(self.target_view)