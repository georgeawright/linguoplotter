from homer.location import Location
from homer.codelets.builders import ProjectionBuilder
from homer.structure_collection_keys import activation


class LetterChunkProjectionBuilder(ProjectionBuilder):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.evaluators.projection_evaluators import (
            LetterChunkProjectionEvaluator,
        )

        return LetterChunkProjectionEvaluator

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["word"]

    def _process_structure(self):
        if not self.target_projectee.is_slot:
            abstract_word = self.target_projectee.abstract_word
        elif not self.target_projectee.correspondences.is_empty():
            abstract_word = self.target_projectee.correspondees.get().abstract_word
        elif not self.target_projectee.relations.is_empty():
            relation = self.target_projectee.relations.get()
            relative = self.target_projectee.relatives.get()
            abstract_relation = relative.abstract_word.relations.where(
                parent_concept=relation.parent_concept
            )
            abstract_word = abstract_relation.arguments.get(
                exclude=[relative.abstract_word]
            )
        else:
            grammar_label = self.target_projectee.labels.where(
                parent_space=self.bubble_chamber.conceptual_spaces["grammar"]
            ).get()
            grammar_concept = grammar_label.parent_concept
            meaning_label = self.target_projectee.labels.where_not(
                parent_space=self.bubble_chamber.conceptual_spaces["grammar"]
            ).get()
            meaning_concept = meaning_label.parent_concept
            abstract_word = (
                meaning_concept.relations.where(parent_concept=grammar_concept)
                .get(key=activation)
                .get()
                .end
            )
        output_location = Location(
            self.target_projectee.location.coordinates,
            self.target_view.output_space,
        )
        word = abstract_word.copy_to_location(
            output_location,
            parent_id=self.codelet_id,
            bubble_chamber=self.bubble_chamber,
        )
        self.target_view.output_space.add(word)
        self.bubble_chamber.words.add(word)
        for location in word.locations:
            self.bubble_chamber.logger.log(location.space)
        self.bubble_chamber.logger.log(word)
        frame_to_output_correspondence = self.bubble_chamber.new_correspondence(
            parent_id=self.codelet_id,
            start=self.target_projectee,
            end=word,
            locations=[self.target_projectee.location, word.location],
            parent_concept=self.bubble_chamber.concepts["same"],
            conceptual_space=self.bubble_chamber.conceptual_spaces["grammar"],
            parent_view=self.target_view,
            quality=0.0,
        )
        self.child_structures = self.bubble_chamber.new_structure_collection(
            word, frame_to_output_correspondence
        )
