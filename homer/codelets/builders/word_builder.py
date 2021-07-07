from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import View
from homer.structures.links import Correspondence
from homer.structures.nodes import Word
from homer.structures.spaces import Frame


# TODO: rename to WordProjectionBuilder?
class WordBuilder(Builder):
    """Builds a word in an output space
    and correspondences to the items it refers to in input spaces"""

    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        Builder.__init__(self, codelet_id, parent_id, bubble_chamber, urgency)
        self._target_structures = target_structures
        self.target_view = None
        self.non_frame = None
        self.target_word = None
        self.target_correspondence = None
        self.word_correspondee = None
        self.non_frame_item = None

    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.evaluators import WordEvaluator

        return WordEvaluator

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
    def _structure_concept(self):
        return self.bubble_chamber.concepts["word"]

    @property
    def target_structures(self):
        return StructureCollection({self.target_view, self.target_word})

    def _passes_preliminary_checks(self):
        self.target_view = self._target_structures["target_view"]
        self.target_word = self._target_structures["target_word"]
        self.word_correspondee = self._target_structures["word_correspondee"]
        self.non_frame = self._target_structures["non_frame"]
        self.non_frame_item = self._target_structures["non_frame_item"]
        if self.target_word.is_slot:
            return (
                self.word_correspondee.structure_id in self.target_view.slot_values
                and self.target_word.structure_id not in self.target_view.slot_values
            )
        return not self.target_word.has_correspondence_to_space(
            self.target_view.output_space
        )

    def _process_structure(self):
        if self.target_word.is_slot:
            word_concept = self.target_view.slot_values[
                self.word_correspondee.structure_id
            ]
            lexeme = word_concept.lexemes.get()
            word_form = self.target_word.word_form
            abstract_word = lexeme.word_forms[word_form]
            word_name = abstract_word.name
            self.target_view.slot_values[self.target_word.structure_id] = word_name
            word_locations = [
                Location(
                    location.coordinates,
                    location.space.instance_in_space(self.target_view.output_space),
                )
                for location in abstract_word.locations
            ]
        else:
            lexeme = self.target_word.lexeme
            word_form = self.target_word.word_form
            word_name = self.target_word.name
            word_locations = [
                Location(
                    location.coordinates,
                    location.space.conceptual_space.instance_in_space(
                        self.target_view.output_space
                    ),
                )
                for location in self.target_word.locations
                if not location.space.is_frame
            ]
        word_locations += [
            Location(
                self.target_word.location.coordinates,
                self.target_view.output_space,
            )
        ]
        word = Word(
            ID.new(Word),
            self.codelet_id,
            name=word_name,
            lexeme=lexeme,
            word_form=word_form,
            locations=word_locations,
            parent_space=self.target_view.output_space,
            quality=0.0,
        )
        self.target_view.output_space.add(word)
        self.bubble_chamber.words.add(word)
        for location in word_locations:
            self.bubble_chamber.logger.log(location.space)
        self.bubble_chamber.logger.log(word)
        frame_to_output_correspondence = Correspondence(
            ID.new(Correspondence),
            self.codelet_id,
            start=self.target_word,
            end=word,
            start_space=self.target_word.parent_space,
            end_space=self.target_view.output_space,
            locations=[self.target_word.location, word.location],
            parent_concept=self.bubble_chamber.concepts["same"],
            conceptual_space=self.target_view.output_space.conceptual_space,
            parent_view=self.target_view,
            quality=0.0,
        )
        self.child_structures = StructureCollection(
            {word, frame_to_output_correspondence}
        )
        self.bubble_chamber.correspondences.add(frame_to_output_correspondence)
        self.bubble_chamber.logger.log(frame_to_output_correspondence)
        self.target_view.members.add(frame_to_output_correspondence)
        self.target_word.links_in.add(frame_to_output_correspondence)
        self.target_word.links_out.add(frame_to_output_correspondence)
        word.links_in.add(frame_to_output_correspondence)
        word.links_out.add(frame_to_output_correspondence)
        for location in frame_to_output_correspondence.locations:
            location.space.add(frame_to_output_correspondence)
        if self.target_word.is_slot:
            non_frame_to_output_correspondence = Correspondence(
                ID.new(Correspondence),
                self.codelet_id,
                start=self.non_frame_item,
                end=word,
                start_space=self.non_frame,
                end_space=self.target_view.output_space,
                locations=[
                    self.non_frame_item.location_in_space(self.non_frame),
                    word.location,
                ],
                parent_concept=self.bubble_chamber.concepts["same"],
                conceptual_space=self.target_view.output_space.conceptual_space,
                parent_view=self.target_view,
                quality=0.0,
            )
            self.child_structures.add(non_frame_to_output_correspondence)
            self.bubble_chamber.correspondences.add(non_frame_to_output_correspondence)
            self.bubble_chamber.logger.log(non_frame_to_output_correspondence)
            self.target_view.members.add(non_frame_to_output_correspondence)
            word.links_in.add(non_frame_to_output_correspondence)
            word.links_out.add(non_frame_to_output_correspondence)
            self.non_frame_item.links_in.add(non_frame_to_output_correspondence)
            self.non_frame_item.links_out.add(non_frame_to_output_correspondence)
            self.bubble_chamber.logger.log(non_frame_to_output_correspondence)
            for location in non_frame_to_output_correspondence.locations:
                location.space.add(non_frame_to_output_correspondence)
        self.bubble_chamber.logger.log(self.target_view)

    def _fizzle(self):
        pass
