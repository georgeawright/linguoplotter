from __future__ import annotations
import statistics
from typing import List

from linguoplotter.errors import MissingStructureError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.location import Location
from linguoplotter.structure_collection_keys import relating_salience
from linguoplotter.structure_collections import StructureSet
from linguoplotter.structures import Node, Space

from .concept import Concept


class Chunk(Node):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        locations: List[Location],
        members: StructureSet,
        parent_space: Space,
        quality: FloatBetweenOneAndZero,
        links_in: StructureSet,
        links_out: StructureSet,
        parent_spaces: StructureSet,
        instances: StructureSet,
        super_chunks: StructureSet,
        sub_chunks: StructureSet,
        champion_labels: StructureSet,
        champion_relations: StructureSet,
        abstract_chunk: Chunk = None,
        is_raw: bool = False,
    ):
        Node.__init__(
            self,
            structure_id,
            parent_id,
            locations=locations,
            parent_space=parent_space,
            quality=quality,
            links_in=links_in,
            links_out=links_out,
            parent_spaces=parent_spaces,
            instances=instances,
            champion_labels=champion_labels,
            champion_relations=champion_relations,
        )
        self.abstract_chunk = abstract_chunk
        self.members = members
        self.super_chunks = super_chunks
        self.sub_chunks = sub_chunks
        self._parent_space = parent_space
        self.is_raw = is_raw
        self.is_chunk = True

    def __dict__(self) -> dict:
        return {
            "structure_id": self.structure_id,
            "parent_id": self.parent_id,
            "locations": [str(location) for location in self.locations],
            "parent_space": self.parent_space.structure_id
            if self.parent_space is not None
            else None,
            "super_chunks": [member.structure_id for member in self.super_chunks],
            "sub_chunks": [member.structure_id for member in self.sub_chunks],
            "members": [member.structure_id for member in self.members],
            "links_out": [link.structure_id for link in self.links_out],
            "links_in": [link.structure_id for link in self.links_in],
            "quality": self.quality,
            "activation": self.activation,
            "unchunkedness": self.unchunkedness,
        }

    @classmethod
    def get_builder_class(cls):
        from linguoplotter.codelets.builders import ChunkBuilder

        return ChunkBuilder

    @classmethod
    def get_evaluator_class(cls):
        from linguoplotter.codelets.evaluators import ChunkEvaluator

        return ChunkEvaluator

    @classmethod
    def get_selector_class(cls):
        from linguoplotter.codelets.selectors import ChunkSelector

        return ChunkSelector

    @property
    def size(self) -> int:
        return (
            1 if len(self.members) == 0 else sum(member.size for member in self.members)
        )

    @property
    def raw_members(self) -> StructureSet:
        if self.is_raw:
            raw_members = self.members.copy()
            raw_members.add(self)
            return raw_members
        return StructureSet.union(
            *[chunk.raw_members for chunk in self.members.where(is_slot=False)]
        )

    @property
    def is_abstract(self):
        return self.parent_space is None

    @property
    def is_leaf(self) -> bool:
        return self.super_chunks.is_empty and self.links.is_empty

    def recalculate_unhappiness(self) -> FloatBetweenOneAndZero:
        self.recalculate_unchunkedness()
        self.recalculate_unlabeledness()
        self.recalculate_unrelatedness()
        self.recalculate_uncorrespondedness()
        return statistics.fmean(
            [
                self.unchunkedness,
                self.unlabeledness,
                self.unrelatedness,
                self.uncorrespondedness,
            ]
        )

    def recalculate_unchunkedness(self):
        self.unchunkedness = 0.1 ** len(self.super_chunks)

    def recalculate_labeling_salience(self):
        self.labeling_salience = statistics.fmean(
            [self.activation, self.unlabeledness, self.unchunkedness]
        )

    def recalculate_relating_salience(self):
        self.relating_salience = statistics.fmean(
            [self.activation, self.unrelatedness, self.unchunkedness]
        )

    @property
    def potential_chunk_mates(self) -> StructureSet:
        return self.nearby().filter(
            lambda x: x not in self.sub_chunks and x not in self.super_chunks
        )

    @property
    def is_recyclable(self) -> bool:
        return (
            not self.is_raw
            and self.parent_space is not None
            and self.parent_space.is_main_input
            and self.activation == 0.0
        )

    def nearby(self, space: Space = None) -> StructureSet:
        if self.is_raw:
            if space is not None:
                return (
                    space.contents.where(is_chunk=True)
                    .near(self.location_in_space(space))
                    .excluding(self),
                )
            return StructureSet.intersection(
                *[
                    location.space.contents.where(
                        is_chunk=True, parent_space=self.parent_space
                    ).near(location)
                    for location in self.locations
                    if location.space.is_conceptual_space
                    and location.space.is_basic_level
                    and location.space.name != "size"
                ]
            ).excluding(self)
        return (
            StructureSet.union(*[member.nearby(space=space) for member in self.members])
            .filter(lambda x: self not in x.super_chunks and x not in self.super_chunks)
            .excluding(self)
        )

    def get_potential_relative(
        self, space: Space = None, concept: Concept = None
    ) -> Chunk:
        space = self.parent_space if space is None else space
        try:
            return self.relatives.filter(
                lambda x: self.relations.where(end=x, conceptual_space=space).is_empty
            ).get(key=relating_salience)
        except MissingStructureError:
            pass
        chunks = space.contents.filter(
            lambda x: x.is_chunk
            and not x.is_letter_chunk
            and not x.is_slot
            and x.parent_space == self.parent_space
            and x.quality > 0
        )
        key = lambda x: concept.classifier.classify(start=self, end=x, space=space)
        return chunks.get(key=key, exclude=[self])

    def copy_to_location(
        self, location: Location, bubble_chamber: "BubbleChamber", parent_id: str = ""
    ):
        chunk_copy, _ = self.copy_with_contents({}, bubble_chamber, parent_id, location)
        return chunk_copy

    def copy_with_contents(
        self,
        copies: dict,
        bubble_chamber: "BubbleChamber",
        parent_id: str,
        new_location: Location,
    ):
        new_locations = [
            location.copy()
            for location in self.locations
            if location.space.is_conceptual_space
        ] + [new_location]
        new_members = bubble_chamber.new_set()
        for member in self.members:
            if member not in copies:
                copies[member], copies = member.copy_with_contents(
                    copies=copies,
                    bubble_chamber=bubble_chamber,
                    parent_id=parent_id,
                    new_location=new_location,
                )
            new_members.add(copies[member])
        chunk_copy = bubble_chamber.new_chunk(
            parent_id=parent_id,
            locations=new_locations,
            parent_space=new_location.space,
            members=new_members,
            is_raw=self.is_raw,
            quality=self.quality,
        )
        return (chunk_copy, copies)

    def __repr__(self) -> str:
        members = "{" + ",".join([member.structure_id for member in self.members]) + "}"
        if self.parent_space is None:
            return f"<{self.structure_id} {members}>"
        return (
            f"<{self.structure_id} {members} in {self.parent_space.structure_id}\n"
            + "\n".join([f"    {location}" for location in self.locations])
            + ">"
        )
