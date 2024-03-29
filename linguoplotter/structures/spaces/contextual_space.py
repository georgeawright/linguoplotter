from __future__ import annotations
import statistics

from linguoplotter import fuzzy
from linguoplotter.errors import MissingStructureError
from linguoplotter.location import Location
from linguoplotter.locations import TwoPointLocation
from linguoplotter.structure import Structure
from linguoplotter.structure_collections import StructureSet
from linguoplotter.structures import Space
from linguoplotter.structures.nodes import Concept


class ContextualSpace(Space):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        name: str,
        parent_concept: Concept,
        contents: StructureSet,
        conceptual_spaces: StructureSet,
        links_in: StructureSet,
        links_out: StructureSet,
        parent_spaces: StructureSet,
        champion_labels: StructureSet,
        champion_relations: StructureSet,
        is_main_input: bool = False,
    ):
        Space.__init__(
            self,
            structure_id=structure_id,
            parent_id=parent_id,
            name=name,
            parent_concept=parent_concept,
            contents=contents,
            quality=0.0,
            links_in=links_in,
            links_out=links_out,
            parent_spaces=parent_spaces,
            champion_labels=champion_labels,
            champion_relations=champion_relations,
        )
        self.parent_frame = None
        self.conceptual_spaces = conceptual_spaces
        self.is_main_input = is_main_input
        self.is_contextual_space = True

    def __dict__(self) -> dict:
        return {
            "structure_id": self.structure_id,
            "parent_id": self.parent_id,
            "name": self.name,
            "is_main_input": self.is_main_input,
            "contents": [item.structure_id for item in self.contents],
            "conceptual_spaces": [
                space.structure_id for space in self.conceptual_spaces
            ],
            "quality": self.quality,
            "activation": self.activation,
        }

    @property
    def conceptual_spaces_and_sub_spaces(self) -> StructureSet:
        return StructureSet.union(
            self.conceptual_spaces,
            *[space.sub_spaces for space in self.conceptual_spaces],
        )

    @property
    def quality(self):
        active_contents = self.contents.filter(
            lambda x: (x.is_chunk or x.is_label or x.is_relation)
            and x.activation > self.FLOATING_POINT_TOLERANCE
        )
        if active_contents.is_empty:
            return 0.0
        return statistics.fmean(
            [
                fuzzy.AND(structure.quality, structure.activation)
                for structure in active_contents
            ]
        )

    def add(self, structure: Structure):
        self.contents.add(structure)

    def remove(self, structure: Structure):
        self.contents.remove(structure)

    def add_conceptual_space(self, conceptual_space: "ConceptualSpace"):
        self.conceptual_spaces.add(conceptual_space)
        for node in self.contents.where(is_node=True):
            if node.has_location_in_space(conceptual_space):
                continue
            for location in node.locations:
                if location.space.is_conceptual_space:
                    try:
                        node.locations.append(
                            conceptual_space.location_from_super_space_location(
                                location
                            )
                        )
                        conceptual_space.add(node)
                        break
                    except KeyError:
                        pass

    def copy(self, **kwargs: dict) -> ContextualSpace:
        """Requires keyword arguments 'bubble_chamber' and 'parent_id'."""
        bubble_chamber = kwargs["bubble_chamber"]
        parent_id = kwargs["parent_id"]
        copies = kwargs.get("copies", {})
        new_space = bubble_chamber.new_contextual_space(
            parent_id=parent_id,
            name=self.name,
            parent_concept=self.parent_concept,
            conceptual_spaces=self.conceptual_spaces.copy(),
        )
        for old_item, new_item in copies.items():
            if old_item.has_location_in_space(self):
                old_location = old_item.location_in_space(self)
                try:
                    new_location = Location(old_location.coordinates, new_space)
                except NotImplementedError:
                    new_location = TwoPointLocation(
                        old_location.start_coordinates,
                        old_location.end_coordinates,
                        new_space,
                    )
                new_item.locations.append(new_location)
                new_item.parent_spaces.add(new_location.space)
                new_location.space.add(new_item)
        for item in self.contents.filter(lambda x: x.is_node and x not in copies):
            new_location = Location(item.location_in_space(self).coordinates, new_space)
            new_item, copies = item.copy_with_contents(
                copies=copies,
                bubble_chamber=bubble_chamber,
                parent_id=parent_id,
                new_location=new_location,
            )
            new_space.add(new_item)
            copies[item] = new_item
            for label in item.labels.where(is_cross_view=False):
                new_label = label.copy(
                    start=new_item,
                    parent_space=new_space,
                    parent_id=parent_id,
                    bubble_chamber=bubble_chamber,
                )
                new_item.links_out.add(new_label)
                new_space.add(new_label)
                copies[label] = new_label
            for relation in item.links_out.where(is_relation=True, is_cross_view=False):
                if relation in copies:
                    continue
                if relation.end not in copies:
                    continue
                new_end = copies[relation.end]
                new_relation = relation.copy(
                    start=new_item,
                    end=new_end,
                    parent_space=new_space,
                    bubble_chamber=bubble_chamber,
                    parent_id=parent_id,
                )
                new_end.links_in.add(new_relation)
                new_item.links_out.add(new_relation)
                new_space.add(new_relation)
                copies[relation] = new_relation
            for relation in item.links_in.where(is_relation=True, is_cross_view=False):
                if relation in copies:
                    continue
                if relation.start not in copies:
                    continue
                new_start = copies[relation.start]
                new_relation = relation.copy(
                    start=new_start,
                    end=new_item,
                    parent_space=new_space,
                    bubble_chamber=bubble_chamber,
                    parent_id=parent_id,
                )
                new_item.links_in.add(new_relation)
                new_start.links_out.add(new_relation)
                new_space.add(new_relation)
                copies[relation] = new_relation
        return new_space, copies
