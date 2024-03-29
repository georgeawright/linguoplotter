from linguoplotter import fuzzy
from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.suggesters import RelationSuggester
from linguoplotter.errors import MissingStructureError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.structure_collections import StructureSet
from linguoplotter.structure_collection_keys import activation, relating_salience
from linguoplotter.structures.links import Relation
from linguoplotter.structures.nodes import Concept


class CrossViewRelationSuggester(RelationSuggester):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.builders.relation_builders import (
            CrossViewRelationBuilder,
        )

        return CrossViewRelationBuilder

    @classmethod
    def make(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        urgency: FloatBetweenOneAndZero = None,
    ):
        targets = bubble_chamber.new_dict(name="targets")
        if urgency is None:
            urgency = bubble_chamber.unrelatedness_of_letter_chunks
        return cls.spawn(parent_id, bubble_chamber, targets, urgency)

    @classmethod
    def make_top_down(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        parent_concept: Concept,
        urgency: FloatBetweenOneAndZero = None,
    ):
        targets = bubble_chamber.new_dict({"concept": parent_concept}, name="targets")
        urgency = urgency if urgency is not None else targets["concept"].activation
        return cls.spawn(parent_id, bubble_chamber, targets, urgency)

    def _passes_preliminary_checks(self):
        if None not in [
            self.targets["concept"],
            self.targets["space"],
            self.targets["end"],
        ]:
            start = (
                self.targets["start"]
                if not self.targets["start"].is_slot
                else self.targets["start"].non_slot_value
            )
            end = (
                self.targets["end"]
                if not self.targets["end"].is_slot
                else self.targets["end"].non_slot_value
            )
            classification = self.targets["concept"].classifier.classify(
                concept=self.targets["concept"],
                space=self.targets["space"],
                start=start,
                end=end,
            )
            self.bubble_chamber.loggers["activity"].log(
                f"Preliminary classification: {classification}"
            )
            if classification < self.bubble_chamber.random_machine.generate_number():
                return False
            return True
        if self.targets["concept"] is None:
            possible_concepts = self.bubble_chamber.concepts.where(
                structure_type=Relation, is_slot=False
            ).where_not(classifier=None)
        else:
            possible_concepts = [self.targets["concept"]]
        possible_views = self.bubble_chamber.views.filter(
            lambda x: x.unhappiness < self.FLOATING_POINT_TOLERANCE
            and x.parent_frame.parent_concept.location_in_space(
                self.bubble_chamber.spaces["grammar"]
            )
            == self.bubble_chamber.concepts["sentence"].location_in_space(
                self.bubble_chamber.spaces["grammar"]
            )
        )
        try:
            if self.targets["start"] is None:
                self.targets["start_view"] = possible_views.get(key=activation)
                self.targets["start"] = StructureSet.union(
                    self.targets["start_view"].output_space.contents.filter(
                        lambda x: x.is_letter_chunk
                        and not x.is_slot
                        and x.labels.not_empty
                    ),
                    self.targets["start_view"].parent_frame.input_space.contents.filter(
                        lambda x: x.is_chunk and (not x.is_slot or x.is_filled_in)
                    ),
                ).get(key=relating_salience)
        except MissingStructureError:
            return False
        if self.targets["space"] is None:
            possible_spaces = self.targets["start"].parent_spaces.where(
                is_conceptual_space=True
            )
        else:
            possible_spaces = [self.targets["space"]]
        try:
            if self.targets["end"] is None:
                self.targets["end_view"] = possible_views.excluding(
                    self.targets["start_view"]
                ).get(key=lambda x: x.cohesiveness_with(self.targets["start_view"]))
                possible_ends = (
                    self.targets["end_view"].output_space.contents.filter(
                        lambda x: x.is_letter_chunk
                        and not x.is_slot
                        and x.labels.not_empty
                    )
                    if self.targets["start"].is_letter_chunk
                    else self.targets[
                        "end_view"
                    ].parent_frame.input_space.contents.filter(
                        lambda x: x.is_chunk and (not x.is_slot or x.is_filled_in)
                    )
                )
                self.targets["end"] = possible_ends.get(
                    key=lambda x: fuzzy.OR(
                        *[
                            space.proximity_between(x, self.targets["start"])
                            for space in possible_spaces.filter(
                                lambda s: s in x.parent_spaces
                            )
                        ]
                    )
                )
        except MissingStructureError:
            return False
        possible_target_combos = [
            self.bubble_chamber.new_dict(
                {
                    "start": self.targets["start"],
                    "end": self.targets["end"],
                    "space": space,
                    "concept": concept,
                },
                name="targets",
            )
            for space in possible_spaces
            for concept in possible_concepts
            if space in self.targets["end"].parent_spaces
            and (
                space.no_of_dimensions == 1 and not space.is_symbolic
                if concept.parent_space.name == "more-less"
                else True
            )
            and (
                concept == self.bubble_chamber.concepts["same"]
                if space == self.bubble_chamber.spaces["string"]
                else True
            )
            and (
                concept.parent_space
                in (
                    self.bubble_chamber.spaces["more-less"],
                    self.bubble_chamber.spaces["same-different"],
                )
                if self.targets["start"].is_chunk
                else True
            )
        ]
        if possible_target_combos == []:
            return False
        targets = self.bubble_chamber.random_machine.select(
            possible_target_combos,
            key=lambda x: x["concept"].classifier.classify(
                start=x["start"],
                end=x["end"],
                concept=x["concept"],
                space=x["space"],
            )
            / x["concept"].number_of_components,
        )
        (
            self.targets["concept"],
            self.targets["start"],
            self.targets["end"],
            self.targets["space"],
        ) = (
            targets["concept"],
            targets["start"],
            targets["end"],
            targets["space"],
        )
        return True

    def _calculate_confidence(self):
        start = (
            self.targets["start"]
            if not self.targets["start"].is_slot
            else self.targets["start"].non_slot_value
        )
        end = (
            self.targets["end"]
            if not self.targets["end"].is_slot
            else self.targets["end"].non_slot_value
        )
        classification = self.targets["concept"].classifier.classify(
            concept=self.targets["concept"],
            space=self.targets["space"],
            start=start,
            end=end,
        )
        self.bubble_chamber.loggers["activity"].log(f"Classification: {classification}")
        self.confidence = classification / (
            1
            if not self.targets["concept"].is_compound_concept
            else self.targets["concept"].number_of_components - 1
        )
