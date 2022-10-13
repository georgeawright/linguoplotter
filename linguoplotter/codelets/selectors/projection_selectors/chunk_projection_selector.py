from linguoplotter.codelets.selectors import ProjectionSelector
from linguoplotter.codelets.suggesters.projection_suggesters import (
    ChunkProjectionSuggester,
)
from linguoplotter.errors import MissingStructureError
from linguoplotter.structure_collection_keys import uncorrespondedness


class ChunkProjectionSelector(ProjectionSelector):
    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["chunk"]

    def _passes_preliminary_checks(self):
        return True

    def _engender_follow_up(self):
        try:
            correspondence_from_frame = self.bubble_chamber.new_structure_collection(
                *[
                    correspondence
                    for correspondence in self.winners.where(is_correspondence=True)
                    if correspondence.start.parent_space.parent_concept
                    == correspondence.end.parent_space.parent_concept
                ]
            ).get()
            frame_output = correspondence_from_frame.start.parent_space
            new_target = frame_output.contents.where(is_chunk=True).get(
                key=uncorrespondedness, exclude=[correspondence_from_frame.start]
            )
            self.child_codelets.append(
                ChunkProjectionSuggester.spawn(
                    self.codelet_id,
                    self.bubble_chamber,
                    {
                        "target_view": correspondence_from_frame.parent_view,
                        "target_projectee": new_target,
                    },
                    new_target.unhappiness,
                )
            )
        except MissingStructureError:
            pass
