from __future__ import annotations
from abc import ABC
import random
import statistics
from typing import List

from .errors import MissingStructureError
from .float_between_one_and_zero import FloatBetweenOneAndZero
from .hyper_parameters import HyperParameters
from .location import Location
from .structure_collection import StructureCollection


class Structure(ABC):

    MINIMUM_ACTIVATION_UPDATE = HyperParameters.MINIMUM_ACTIVATION_UPDATE
    ACTIVATION_UPDATE_COEFFICIENT = HyperParameters.ACTIVATION_UPDATE_COEFFICIENT

    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        locations: List[Location],
        quality: FloatBetweenOneAndZero,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
        stable_activation: float = None,
    ):
        self.structure_id = structure_id
        self.parent_id = parent_id
        self._locations = locations
        self._quality = quality
        self.links_in = StructureCollection() if links_in is None else links_in
        self.links_out = StructureCollection() if links_out is None else links_out
        self._activation = FloatBetweenOneAndZero(
            random.random() if stable_activation is None else stable_activation
        )
        self.stable = stable_activation is not None
        self._activation_buffer = 0.0
        self._activation_update_coefficient = self.ACTIVATION_UPDATE_COEFFICIENT
        self._parent_concept = None

    @classmethod
    def get_builder_class(cls):
        raise NotImplementedError

    @classmethod
    def get_evaluator_class(cls):
        raise NotImplementedError

    @classmethod
    def get_selector_class(cls):
        raise NotImplementedError

    @property
    def parent_concept(self) -> Structure:
        return self._parent_concept

    @property
    def location(self) -> Location:
        try:
            return self.locations[0]
        except TypeError:
            return None
        except IndexError:
            return None

    @property
    def locations(self) -> List[Location]:
        return self._locations

    @locations.setter
    def locations(self, locations: List[Location]):
        self._locations = locations

    @property
    def size(self) -> int:
        return 1

    @property
    def coordinates(self) -> list:
        for location in self.locations:
            if location.space.value == "input":
                return location.coordinates
        raise Exception(f"{self.structure_id} has no location in input space")

    @property
    def is_slot(self) -> bool:
        return False

    @property
    def parent_spaces(self) -> StructureCollection:
        return StructureCollection({location.space for location in self.locations})

    @property
    def exigency(self) -> FloatBetweenOneAndZero:
        return statistics.fmean([self.activation, self.unhappiness])

    @property
    def quality(self) -> FloatBetweenOneAndZero:
        return self._quality

    @quality.setter
    def quality(self, q: FloatBetweenOneAndZero):
        self._quality = q

    @property
    def activation(self) -> FloatBetweenOneAndZero:
        return self._activation

    @activation.setter
    def activation(self, a: FloatBetweenOneAndZero):
        self._activation = a

    @property
    def unhappiness(self) -> FloatBetweenOneAndZero:
        # probably should just return unlinkedness
        return statistics.fmean([self.unchunkedness, self.unlinkedness])

    @property
    def unchunkedness(self) -> FloatBetweenOneAndZero:
        return 0

    @property
    def unlinkedness(self) -> FloatBetweenOneAndZero:
        return 0.5 ** len(self.links)

    @property
    def links(self) -> StructureCollection:
        return StructureCollection.union(self.links_in, self.links_out)

    @property
    def correspondences(self) -> StructureCollection:
        from homer.structures.links import Correspondence

        return StructureCollection(
            set.union(
                {link for link in self.links_in if isinstance(link, Correspondence)},
                {link for link in self.links_out if isinstance(link, Correspondence)},
            )
        )

    @property
    def correspondees(self) -> StructureCollection:
        return StructureCollection(
            set.union(
                {
                    correspondence.start
                    for correspondence in self.correspondences
                    if self != correspondence.start
                },
                {
                    correspondence.end
                    for correspondence in self.correspondences
                    if self != correspondence.end
                },
            )
        )

    @property
    def labels(self) -> StructureCollection:
        from homer.structures.links import Label

        return StructureCollection(
            {link for link in self.links_out if isinstance(link, Label)}
        )

    @property
    def relations(self) -> StructureCollection:
        from homer.structures.links import Relation

        return StructureCollection(
            set.union(
                {link for link in self.links_in if isinstance(link, Relation)},
                {link for link in self.links_out if isinstance(link, Relation)},
            )
        )

    @property
    def lexemes(self) -> StructureCollection:
        from homer.structures.nodes import Lexeme

        return StructureCollection(
            {link.end for link in self.links_out if isinstance(link.end, Lexeme)}
        )

    def nearby(self, space: Structure = None):
        raise NotImplementedError

    def is_near(self, other: Structure) -> bool:
        for other_location in other.locations:
            for self_location in self.locations:
                if self_location.is_near(other_location):
                    return True
        return False

    def has_location_in_space(self, space: Structure) -> bool:
        try:
            self.location_in_space(space)
            return True
        except Exception:
            return False

    def location_in_space(self, space: Structure) -> Location:
        for location in self.locations:
            if location is not None and location.space == space:
                return location
        raise Exception(
            f"{self.structure_id} has no location in space {space.structure_id}"
        )

    def has_link(self, structure: Structure, start: Structure = None) -> bool:
        from homer.structures.links import Correspondence, Label, Relation

        if isinstance(structure, Label):
            return self.has_label(structure.parent_concept)
        if isinstance(structure, Relation):
            return self.has_relation(
                structure.parent_space,
                structure.parent_concept,
                structure.start,
                structure.end,
            )
        start = start if start is not None else self
        other_arg = structure.end if start == structure.start else structure.start
        if isinstance(structure, Correspondence):
            return self.has_correspondence(
                structure.parent_space, structure.parent_concept, other_arg
            )
        return False

    def has_label(self, concept: Structure) -> bool:
        for label in self.labels:
            if label.parent_concept == concept:
                return True
        return False

    def label_of_type(self, concept: Structure):
        for label in self.labels:
            if label.parent_concept == concept:
                return label
        raise MissingStructureError

    def labels_in_space(self, space: Structure) -> StructureCollection:
        return StructureCollection(
            {label for label in self.labels if label in space.contents}
        )

    def has_relation(
        self,
        space: Structure,
        concept: Structure,
        first_argument: Structure,
        second_argument: Structure,
    ) -> bool:
        for relation in self.relations:
            if (
                relation.parent_concept == concept
                and relation.start == first_argument
                and relation.end == second_argument
                and relation.parent_space == space
            ):
                return True
        return False

    def relations_in_space_with(
        self, space: Structure, other: Structure
    ) -> StructureCollection:
        return StructureCollection(
            {
                relation
                for relation in self.relations
                if relation in space.contents
                and other in {relation.start, relation.end}
            }
        )

    def relations_with(self, other: Structure) -> StructureCollection:
        return StructureCollection(
            {
                relation
                for relation in self.relations
                if other in {relation.start, relation.end}
            }
        )

    def has_correspondence(
        self, space: Structure, concept: Structure, second_argument: Structure
    ) -> bool:
        for correspondence in self.correspondences:
            if (
                correspondence.parent_concept == concept
                and correspondence.parent_space == space
                and second_argument in (correspondence.start, correspondence.end)
            ):
                return True
        return False

    def has_correspondence_to_space(self, space: Structure) -> bool:
        return len(self.correspondences_to_space(space)) > 0

    def correspondences_with(self, other: Structure):
        return StructureCollection(
            {
                correspondence
                for correspondence in self.correspondences
                if correspondence.start == self
                and correspondence.end == other
                or correspondence.start == other
                and correspondence.end == self
            }
        )

    def correspondences_to_space(self, space: Structure):
        return StructureCollection(
            {
                correspondence
                for correspondence in self.correspondences
                if correspondence.start == self
                and correspondence.end_space == space
                or correspondence.end == self
                and correspondence.start_space == space
            }
        )

    def is_fully_active(self) -> bool:
        return self.activation == 1.0

    def boost_activation(self, amount: float = None):
        if self.stable:
            return
        if amount is None:
            amount = self.MINIMUM_ACTIVATION_UPDATE
        self._activation_buffer += self._activation_update_coefficient * amount

    def decay_activation(self, amount: float = None):
        if self.stable:
            return
        if amount is None:
            amount = self.MINIMUM_ACTIVATION_UPDATE
        self._activation_buffer -= self._activation_update_coefficient * amount

    def spread_activation(self):
        if not self.is_fully_active():
            return
        if self.parent_concept is not None:
            self.parent_concept.boost_activation(self.activation)
        for link in self.links:
            try:
                link.end.boost_activation(link.activation)
            except AttributeError:  # labels have no end
                pass

    def update_activation(self):
        if self._activation_buffer == 0.0:
            self.decay_activation()
        self._activation = FloatBetweenOneAndZero(
            self._activation + self._activation_buffer
        )
        self._activation_buffer = 0.0
