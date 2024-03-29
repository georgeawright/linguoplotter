from __future__ import annotations
from typing import List

from linguoplotter.errors import MissingStructureError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.location import Location
from linguoplotter.structure import Structure
from linguoplotter.structure_collections import StructureSet
from linguoplotter.structures import Link, View
from linguoplotter.structures.nodes import Concept
from linguoplotter.structures.spaces import ConceptualSpace


class Correspondence(Link):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        start: Structure,
        end: Structure,
        arguments: StructureSet,
        locations: List[Location],
        parent_concept: Concept,
        conceptual_space: ConceptualSpace,
        parent_view: View,
        quality: FloatBetweenOneAndZero,
        links_in: StructureSet,
        links_out: StructureSet,
        parent_spaces: StructureSet,
        champion_labels: StructureSet,
        champion_relations: StructureSet,
        is_privileged: bool = False,
        is_bidirectional: bool = True,
        is_excitatory: bool = True,
        is_projection: bool = False,
    ):
        Link.__init__(
            self,
            structure_id,
            parent_id,
            start,
            end,
            arguments,
            locations,
            parent_concept,
            quality,
            links_in=links_in,
            links_out=links_out,
            parent_spaces=parent_spaces,
            champion_labels=champion_labels,
            champion_relations=champion_relations,
        )
        self.conceptual_space = conceptual_space
        self.parent_view = parent_view
        self.is_privileged = is_privileged
        self.is_bidirectional = is_bidirectional
        self.is_excitatory = is_excitatory
        self.is_projection = is_projection
        self.is_correspondence = True

    def __dict__(self) -> dict:
        return {
            "structure_id": self.structure_id,
            "parent_id": self.parent_id,
            "parent_concept": self.parent_concept.structure_id,
            "conceptual_space": self.conceptual_space.structure_id
            if self.conceptual_space is not None
            else None,
            "start": self.start.structure_id,
            "end": self.end.structure_id,
            "locations": [str(location) for location in self.locations],
            "parent_view": self.parent_view.structure_id
            if self.parent_view is not None
            else None,
            "quality": self.quality,
            "activation": self.activation,
        }

    @classmethod
    def get_builder_class(cls):
        from linguoplotter.codelets.builders import CorrespondenceBuilder

        return CorrespondenceBuilder

    @classmethod
    def get_evaluator_class(cls):
        from linguoplotter.codelets.evaluators import CorrespondenceEvaluator

        return CorrespondenceEvaluator

    @classmethod
    def get_selector_class(cls):
        from linguoplotter.codelets.selectors import CorrespondenceSelector

        return CorrespondenceSelector

    @property
    def node_pairs(self) -> list:
        if self.start.is_node:
            return [(self.start, self.end)]
        if self.start.is_label:
            return [(self.start.start, self.end.start)]
        return [(self.start.start, self.end.start), (self.start.end, self.end.end)]

    @property
    def is_leaf(self) -> bool:
        return False

    def nearby(self):
        return StructureSet.difference(
            StructureSet.union(
                self.start.correspondences_to_space(self.end.parent_space),
                self.end.correspondences_to_space(self.start.parent_space),
            ),
            StructureSet.intersection(
                self.start.correspondences_to_space(self.end.parent_space),
                self.end.correspondences_to_space(self.start.parent_space),
            ),
        )

    @property
    def slot_argument(self):
        if self.start.is_slot:
            return self.start
        if self.end.is_slot:
            return self.end
        raise MissingStructureError("Correspondence has no slot argument")

    @property
    def non_slot_argument(self):
        if not self.start.is_slot:
            return self.start
        if not self.end.is_slot:
            return self.end
        raise Exception("Correspondence has no non slot argument")

    def common_arguments_with(self, other: Correspondence) -> StructureSet:
        return StructureSet.intersection(self.arguments, other.arguments)

    def recalculate_activation(self):
        pass

    def __repr__(self) -> str:
        return (
            f"<{self.structure_id} {self.parent_concept.name}("
            + f"{self.start.structure_id}, {self.end.structure_id}) "
            + f"in {self.parent_view.structure_id}>"
            if self.parent_view is not None
            else ">"
        )
