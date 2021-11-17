from __future__ import annotations

from typing import Callable, Dict, List

from homer.location import Location
from homer.structure import Structure
from homer.structure_collection import StructureCollection
from homer.structures import Space
from homer.structures.nodes import Concept


class ConceptualSpace(Space):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        name: str,
        parent_concept: Concept,
        contents: StructureCollection,
        no_of_dimensions: int,
        dimensions: List[ConceptualSpace],
        sub_spaces: List[ConceptualSpace],
        links_in: StructureCollection,
        links_out: StructureCollection,
        parent_spaces: StructureCollection,
        is_basic_level: bool = False,
        is_symbolic: bool = False,
        super_space_to_coordinate_function_map: Dict[str, Callable] = None,
    ):
        Space.__init__(
            self,
            structure_id=structure_id,
            parent_id=parent_id,
            name=name,
            parent_concept=parent_concept,
            contents=contents,
            quality=1.0,
            links_in=links_in,
            links_out=links_out,
            parent_spaces=parent_spaces,
        )
        self.no_of_dimensions = no_of_dimensions
        self._dimensions = dimensions
        self.sub_spaces = sub_spaces
        self.is_basic_level = is_basic_level
        self.is_symbolic = is_symbolic
        self.super_space_to_coordinate_function_map = (
            (super_space_to_coordinate_function_map)
            if super_space_to_coordinate_function_map is not None
            else {}
        )
        self.is_conceptual_space = True

    @property
    def instance_type(self):
        return self.parent_concept.instance_type

    @property
    def dimensions(self) -> List[Space]:
        if self.no_of_dimensions < 1:
            return []
        if self.no_of_dimensions == 1:
            return [self]
        return self._dimensions

    def add(self, structure: Structure):
        location_in_this_space = structure.location_in_space(self)
        if structure not in self.contents:
            self.contents.add(structure)
            for sub_space in self.sub_spaces:
                location_in_sub_space = sub_space.location_from_super_space_location(
                    location_in_this_space
                )
                structure.locations.append(location_in_sub_space)
                sub_space.add(structure)

    def location_from_super_space_location(self, location: Location) -> Location:
        if location.coordinates[0][0] is None:
            coordinates = [[None for _ in range(self.no_of_dimensions)]]
        else:
            coordinates_function = self.super_space_to_coordinate_function_map[
                location.space.name
            ]
            coordinates = coordinates_function(location)
        return Location(coordinates, self)

    def update_activation(self):
        if len(self.contents) == 0:
            self._activation = 0
        else:
            self._activation = max(item.activation for item in self.contents)
