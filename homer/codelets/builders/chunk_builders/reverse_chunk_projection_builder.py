from homer.bubble_chamber import BubbleChamber
from homer.codelets.builders import ChunkBuilder
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.links import Correspondence
from homer.structures.nodes import Chunk
from homer.tools import project_item_into_space


class ReverseChunkProjectionBuilder(ChunkBuilder):
    """Projects a raw chunk into an interpretation space as
    the member of an interpretation chunk according to the
    labels and relations of that chunk."""

    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        ChunkBuilder.__init__(
            self,
            codelet_id,
            parent_id,
            bubble_chamber,
            target_structures,
            urgency,
        )
        self.target_view = None
        self.target_interpretation_chunk = None
        self.target_raw_chunk = None
        self.correspondee_to_raw_chunk = None
        self.new_chunk = None
        self.confidence = 0.0

    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.evaluators.chunk_evaluators import (
            ReverseChunkProjectionEvaluator,
        )

        return ReverseChunkProjectionEvaluator

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
        return self.bubble_chamber.concepts["chunk"]

    def _passes_preliminary_checks(self):
        self.target_view = self._target_structures["target_view"]
        self.target_interpretation_chunk = self._target_structures[
            "target_interpretation_chunk"
        ]
        self.target_raw_chunk = self._target_structures["target_raw_chunk"]
        self.correspondee_to_raw_chunk = self._target_structures[
            "correspondee_to_raw_chunk"
        ]
        self.new_chunk = self._target_structures["new_chunk"]
        if self.target_raw_chunk.has_correspondence_to_space(
            self.target_interpretation_chunk.parent_space
        ):
            return False
        return True

    def _process_structure(self):
        self.correspondee_to_raw_chunk.structure_id = ID.new(Chunk)
        self.bubble_chamber.chunks.add(self.correspondee_to_raw_chunk)
        self.bubble_chamber.logger.log(self.correspondee_to_raw_chunk)
        self.new_chunk.structure_id = ID.new(Chunk)
        self.bubble_chamber.chunks.add(self.new_chunk)
        self.bubble_chamber.logger.log(self.new_chunk)
        for member in list(self.new_chunk.members.structures) + [
            self.target_interpretation_chunk
        ]:
            member.chunks_made_from_this_chunk.add(self.new_chunk)
        self._copy_across_links(self.target_interpretation_chunk, self.new_chunk)
        self.new_chunk._activation = self.target_interpretation_chunk.activation
        start = self.target_raw_chunk
        end = self.correspondee_to_raw_chunk
        correspondence = Correspondence(
            ID.new(Correspondence),
            self.codelet_id,
            start=start,
            end=end,
            start_space=start.parent_space,
            end_space=end.parent_space,
            locations=[
                start.location_in_space(start.parent_space),
                end.location_in_space(end.parent_space),
            ],
            parent_concept=self.bubble_chamber.concepts["same"],
            conceptual_space=None,
            parent_view=self.target_view,
            quality=0,
        )
        start.links_out.add(correspondence)
        start.links_in.add(correspondence)
        end.links_out.add(correspondence)
        end.links_in.add(correspondence)
        self.bubble_chamber.correspondences.add(correspondence)
        self.bubble_chamber.logger.log(correspondence)
        self.child_structures = StructureCollection(
            {self.new_chunk, correspondence, self.correspondee_to_raw_chunk}
        )
