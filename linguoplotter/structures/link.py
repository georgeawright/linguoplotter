from typing import List
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.location import Location
from linguoplotter.structure import Structure
from linguoplotter.structure_collections import StructureSet

from .space import Space


class Link(Structure):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        start: Structure,
        end: Structure,
        arguments: StructureSet,
        locations: List[Location],
        parent_concept: "Concept",
        quality: FloatBetweenOneAndZero,
        links_in: StructureSet,
        links_out: StructureSet,
        parent_spaces: StructureSet,
        champion_labels: StructureSet,
        champion_relations: StructureSet,
    ):
        Structure.__init__(
            self,
            structure_id,
            parent_id,
            locations,
            quality,
            links_in=links_in,
            links_out=links_out,
            parent_spaces=parent_spaces,
            champion_labels=champion_labels,
            champion_relations=champion_relations,
        )
        self.start = start
        self.end = end
        self.arguments = arguments
        self._parent_concept = parent_concept
        self.value = parent_concept.name if hasattr(parent_concept, "name") else None
        self.is_excitatory = True
        self.is_link = True

    @property
    def parent_space(self) -> Space:
        return self._parent_space

    @property
    def is_slot(self) -> bool:
        return self.parent_concept.is_slot

    @property
    def is_leaf(self) -> bool:
        return self.correspondences.is_empty

    @property
    def is_recyclable(self) -> bool:
        return (
            self.parent_space is not None
            and self.parent_space.is_main_input
            and self.activation == 0.0
            and self.links.is_empty
        )

    def recalculate_unlabeledness(self):
        self.unlabeledness = 0.5 * 0.5 ** sum(link.activation for link in self.labels)

    def recalculate_unrelatedness(self):
        self.unrelatedness = 0.5 * 0.5 ** sum(
            link.activation for link in self.relations
        )

    def is_between(self, a: Structure, b: Structure):
        return self.start == a and self.end == b or self.end == a and self.start == a

    def __repr__(self) -> str:
        concept = "none" if self.parent_concept is None else self.parent_concept.name
        args = f"{self.start.structure_id}"
        if self.end is not None:
            args += f", {self.end.structure_id}"
        spaces = ", ".join([location.space.name for location in self.locations])
        return f"<{self.structure_id} {concept}({args}) in {spaces}>"
