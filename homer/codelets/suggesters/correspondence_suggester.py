from __future__ import annotations

from homer.bubble_chamber import BubbleChamber
from homer.codelets import Suggester
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure import Structure
from homer.structure_collection import StructureCollection
from homer.structures import Space, View
from homer.structures.nodes import Concept
from homer.structures.links import Correspondence
from homer.structures.spaces import ConceptualSpace, WorkingSpace


class CorrespondenceSuggester(Suggester):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        Suggester.__init__(
            self, codelet_id, parent_id, bubble_chamber, target_structures, urgency
        )
        self.target_view = None
        self.target_space_one = None
        self.target_structure_one = None
        self.target_space_two = None
        self.target_structure_two = None
        self.target_conceptual_space = None
        self.parent_concept = None
        self.parent_space = None
        self.correspondence = None
        self.child_structure = None

    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.builders import CorrespondenceBuilder

        return CorrespondenceBuilder

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        qualifier = (
            "TopDown" if target_structures["parent_concept"] is not None else "BottomUp"
        )
        codelet_id = ID.new(cls, qualifier)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            target_structures,
            urgency,
        )

    @classmethod
    def make(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero = None,
    ):
        target_view = bubble_chamber.production_views.get_active()
        target_space = (
            target_view.input_working_spaces.get_random()
            .contents.of_type(Space)
            .where(is_basic_level=True)
            .get_active()
        )
        target = (
            target_space.contents.not_of_type(Space)
            .not_of_type(Correspondence)
            .get_exigent()
        )
        urgency = urgency if urgency is not None else target.exigency
        return cls.spawn(
            parent_id,
            bubble_chamber,
            {
                "target_view": target_view,
                "target_space_one": target_space,
                "target_structure_one": target,
                "target_space_two": target_space,
                "target_structure_two": target,
                "target_conceptual_space": None,
                "parent_concept": None,
            },
            urgency,
        )

    @classmethod
    def make_top_down(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        parent_concept: Concept,
        urgency: FloatBetweenOneAndZero = None,
    ):
        target_view = bubble_chamber.production_views.get_active()
        target_space = (
            target_view.input_working_spaces.get_random()
            .contents.of_type(Space)
            .where(is_basic_level=True)
            .get_active()
        )
        target = (
            target_space.contents.not_of_type(Space)
            .not_of_type(Correspondence)
            .get_exigent()
        )
        urgency = urgency if urgency is not None else target.exigency
        return cls.spawn(
            parent_id,
            bubble_chamber,
            {
                "target_view": target_view,
                "target_space_one": target_space,
                "target_structure_one": target,
                "target_space_two": target_space,
                "target_structure_two": target,
                "target_conceptual_space": None,
                "parent_concept": parent_concept,
            },
            urgency,
        )

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["correspondence"]

    def _passes_preliminary_checks(self):
        self.target_view = self._target_structures["target_view"]
        self.target_structure_one = self._target_structures["target_structure_one"]
        self.target_structure_two = self._target_structures["target_structure_two"]
        self.target_space_one = self._target_structures["target_space_one"]
        self.target_space_two = self._target_structures["target_space_two"]
        self.target_conceptual_space = self._target_structures[
            "target_conceptual_space"
        ]
        self.parent_concept = self._target_structures["parent_concept"]
        if self.target_space_two is None:
            try:
                self.target_space_two = (
                    self.target_view.input_spaces.get_active(
                        exclude=list(self.target_space_one.parent_spaces)
                    )
                    .contents.of_type(WorkingSpace)
                    .where(is_basic_level=True)
                    .where(conceptual_space=self.target_space_one.conceptual_space)
                    .get_random()
                )
                self._target_structures["target_space_two"] = self.target_space_two
            except MissingStructureError:
                return False
        try:
            if self.target_structure_two is None:
                self.target_structure_two = self.target_space_two.contents.of_type(
                    type(self.target_structure_one)
                ).get_exigent()
                self._target_structures[
                    "target_structure_two"
                ] = self.target_structure_two
        except MissingStructureError:
            return False
        if self.target_conceptual_space is None:
            self.target_conceptual_space = self.target_space_one.conceptual_space
            self._target_structures[
                "target_conceptual_space"
            ] = self.target_conceptual_space
        if self.target_conceptual_space != self.target_space_two.conceptual_space:
            return False
        if self.parent_concept is None:
            self.parent_concept = (
                self.bubble_chamber.spaces["correspondential concepts"]
                .contents.of_type(ConceptualSpace)
                .get_random()
                .contents.of_type(Concept)
                .get_random()
            )
            self._target_structures["parent_concept"] = self.parent_concept
        if self.target_view.has_member(
            self.parent_concept,
            self.target_structure_one,
            self.target_structure_two,
            self.target_space_one,
            self.target_space_two,
        ):
            return False
        self.correspondence = Correspondence(
            None,
            self.codelet_id,
            self.target_structure_one,
            self.target_structure_two,
            self.target_space_one,
            self.target_space_two,
            [
                self.target_structure_one.location_in_space(self.target_space_one),
                self.target_structure_two.location_in_space(self.target_space_two),
            ],
            self.parent_concept,
            self.target_conceptual_space,
            self.target_view,
            0,
        )
        for correspondence in self.target_view.members:
            if not correspondence.is_compatible_with(self.correspondence):
                return False
        return True

    def _calculate_confidence(self):
        self.confidence = self.parent_concept.classifier.classify(
            concept=self.parent_concept,
            space=self.target_conceptual_space,
            start=self.target_structure_one,
            end=self.target_structure_two,
            view=self.target_view,
        )

    def _fizzle(self):
        pass