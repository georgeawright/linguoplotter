from homer.bubble_chamber import BubbleChamber
from homer.codelet import Codelet
from homer.codelet_result import CodeletResult
from homer.codelets.builders import (
    ChunkBuilder,
    CorrespondenceBuilder,
    LabelBuilder,
    RelationBuilder,
    ViewBuilder,
    WordBuilder,
)
from homer.codelets.evaluators import (
    ChunkEvaluator,
    CorrespondenceEvaluator,
    LabelEvaluator,
    RelationEvaluator,
    ViewEvaluator,
)
from homer.codelets.selectors import (
    ChunkSelector,
    CorrespondenceSelector,
    LabelSelector,
    RelationSelector,
    ViewSelector,
)
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure_collection import StructureCollection
from homer.structures import Concept


class FactoryCodelet(Codelet):
    """Spawns a new codelet according to concept activations in the bubble chamber."""

    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero,
    ):
        Codelet.__init__(self, codelet_id, parent_id, urgency)
        self.bubble_chamber = bubble_chamber

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(codelet_id, parent_id, bubble_chamber, urgency)

    def run(self) -> CodeletResult:
        try:
            self._engender_follow_up()
        except MissingStructureError:
            return self.run()
        self.child_codelets.append(
            self.spawn(
                self.codelet_id,
                self.bubble_chamber,
                1 - self.bubble_chamber.satisfaction,
            )
        )
        self.result = CodeletResult.SUCCESS
        return self.result

    def _engender_follow_up(self):
        action_type = self.bubble_chamber.spaces["activities"].contents.get_active()
        links_to_structure_nodes = StructureCollection(
            {
                link
                for link in action_type.links_out
                if link.end in self.bubble_chamber.spaces["structures"].contents
            }
        )
        structure_type = links_to_structure_nodes.get_active().end
        if action_type == self.bubble_chamber.concepts["build"]:
            if structure_type == self.bubble_chamber.concepts["chunk"]:
                target = self.bubble_chamber.chunks.get_unhappy()
                follow_up = ChunkBuilder.spawn(
                    self.codelet_id, self.bubble_chamber, target, target.unhappiness
                )
            elif structure_type == self.bubble_chamber.concepts["correspondence"]:
                raise MissingStructureError
                target_space = self.bubble_chamber.working_spaces.get_active()
                target = target_space.contents.get_unhappy()
                follow_up = CorrespondenceBuilder.spawn(
                    self.codelet_id,
                    self.bubble_chamber,
                    target_space,
                    target,
                    target.unhappiness,
                )
            elif structure_type == self.bubble_chamber.concepts["label"]:
                target = self.bubble_chamber.chunks.get_unhappy()
                follow_up = LabelBuilder.spawn(
                    self.codelet_id, self.bubble_chamber, target, target.unhappiness
                )
            elif structure_type == self.bubble_chamber.concepts["relation"]:
                target = self.bubble_chamber.chunks.get_unhappy()
                target_space = target.parent_spaces.get_random()
                follow_up = RelationBuilder.spawn(
                    self.codelet_id,
                    self.bubble_chamber,
                    target_space,
                    target,
                    target.unhappiness,
                )
            elif structure_type == self.bubble_chamber.concepts["view"]:
                raise MissingStructureError
                target = self.bubble_chamber.correspondences.get_unhappy()
                follow_up = ViewBuilder.spawn(
                    self.codelet_id,
                    self.bubble_chamber,
                    target,
                    target.unhappiness,
                )
            elif structure_type == self.bubble_chamber.concepts["word"]:
                raise MissingStructureError
                target_view = self.bubble_chamber.views.get_unhappy()
                target_correspondence = (
                    self.bubble_chamber.correspondences.get_unhappy()
                )
                follow_up = WordBuilder.spawn(
                    self.codelet_id,
                    self.bubble_chamber,
                    target_view,
                    target_correspondence,
                    target_correspondence.unhappiness,
                )
            else:
                raise Exception("unknown structure type")
        elif action_type == self.bubble_chamber.concepts["evaluate"]:
            if structure_type == self.bubble_chamber.concepts["chunk"]:
                target = self.bubble_chamber.chunks.get_active()
                follow_up = ChunkEvaluator.spawn(
                    self.codelet_id,
                    self.bubble_chamber,
                    target,
                    structure_type.activation,
                )
            elif structure_type == self.bubble_chamber.concepts["correspondence"]:
                raise MissingStructureError
                target = self.bubble_chamber.correspondences.get_active()
                follow_up = CorrespondenceEvaluator.spawn(
                    self.codelet_id,
                    self.bubble_chamber,
                    target,
                    structure_type.activation,
                )
            elif structure_type == self.bubble_chamber.concepts["label"]:
                target = self.bubble_chamber.labels.get_active()
                follow_up = LabelEvaluator.spawn(
                    self.codelet_id,
                    self.bubble_chamber,
                    target,
                    structure_type.activation,
                )
            elif structure_type == self.bubble_chamber.concepts["relation"]:
                target = self.bubble_chamber.relations.get_active()
                follow_up = RelationEvaluator.spawn(
                    self.codelet_id,
                    self.bubble_chamber,
                    target,
                    structure_type.activation,
                )
            elif structure_type == self.bubble_chamber.concepts["view"]:
                raise MissingStructureError
                target = self.bubble_chamber.views.get_active()
                follow_up = ViewEvaluator.spawn(
                    self.codelet_id,
                    self.bubble_chamber,
                    target,
                    structure_type.activation,
                )
            else:
                raise Exception("unknown structure type")
        elif action_type == self.bubble_chamber.concepts["select"]:
            raise MissingStructureError
            if structure_type == self.bubble_chamber.concepts["chunk"]:
                champion = self.bubble_chamber.chunks.get_active()
                target_space = champion.parent_spaces.get_random()
                follow_up = ChunkSelector.spawn(
                    self.codelet_id,
                    self.bubble_chamber,
                    target_space,
                    champion,
                    champion.activation,
                )
            elif structure_type == self.bubble_chamber.concepts["correspondence"]:
                champion = self.bubble_chamber.correspondences.get_active()
                follow_up = CorrespondenceSelector.spawn(
                    self.codelet_id,
                    self.bubble_chamber,
                    champion,
                    champion.activation,
                )
            elif structure_type == self.bubble_chamber.concepts["label"]:
                champion = self.bubble_chamber.labels.get_active()
                follow_up = LabelSelector.spawn(
                    self.codelet_id,
                    self.bubble_chamber,
                    champion,
                    champion.activation,
                )
            elif structure_type == self.bubble_chamber.concepts["relation"]:
                champion = self.bubble_chamber.relations.get_active()
                follow_up = RelationSelector.spawn(
                    self.codelet_id,
                    self.bubble_chamber,
                    champion,
                    champion.activation,
                )
            elif structure_type == self.bubble_chamber.concepts["view"]:
                champion = self.bubble_chamber.views.get_active()
                follow_up = ViewSelector.spawn(
                    self.codelet_id,
                    self.bubble_chamber,
                    champion,
                    champion.activation,
                )
            else:
                raise Exception("unknown structure type")
        else:
            raise Exception("unknown activity type")
        self.child_codelets.append(follow_up)
