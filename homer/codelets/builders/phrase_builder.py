import statistics
from typing import Union

from homer.bubble_chamber import BubbleChamber
from homer.codelets.builder import Builder
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.links import Label
from homer.structures.nodes import Chunk, Concept, Phrase, Rule, Word


class PhraseBuilder(Builder):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        Builder.__init__(self, codelet_id, parent_id, bubble_chamber, urgency)
        self._target_structures = target_structures
        self.target_rule = None
        self.target_root = None
        self.target_left_branch = None
        self.target_right_branch = None
        self.parent_space = None

    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.evaluators import PhraseEvaluator

        return PhraseEvaluator

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        target_structures: dict,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            target_structures,
            urgency,
        )

    @classmethod
    def arrange_targets(cls, targets: StructureCollection):
        root = None
        for target in targets:
            remaining_targets = StructureCollection.difference(
                targets, StructureCollection({target})
            )
            if hasattr(target, "members") and target.members == remaining_targets:
                root = target
                left_branch = root.left_branch
                right_branch = root.right_branch
        if root is None:
            branch_one = targets.get()
            branch_two = targets.get(exclude=[branch_one])
            if (
                branch_one.location.coordinates[0][0]
                < branch_two.location.coordinates[0][0]
            ):
                left_branch = branch_one
                right_branch = branch_two
            else:
                left_branch = branch_two
                right_branch = branch_one
        return (root, left_branch, right_branch)

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["phrase"]

    @property
    def target_structures(self):
        targets = [
            self.target_root,
            self.target_left_branch,
            self.target_right_branch,
        ]
        return StructureCollection({target for target in targets if target is not None})

    def _passes_preliminary_checks(self):
        self.target_rule = self._target_structures["target_rule"]
        self.target_root = self._target_structures["target_root"]
        self.target_left_branch = self._target_structures["target_left_branch"]
        self.target_right_branch = self._target_structures["target_right_branch"]
        self.parent_space = (
            self.target_structures.get().parent_space
            if not self.target_structures.is_empty()
            else None
        )
        if len(self.target_structures) < 2:
            return False
        if self.target_rule is None:
            try:
                self.target_rule = StructureCollection(
                    {
                        rule
                        for rule in self.bubble_chamber.rules
                        if self._rule_is_compatible_with_targets(rule)
                    }
                ).get()
            except MissingStructureError:
                return False
        elif not self._rule_is_compatible_with_targets(self.target_rule):
            return False
        if len(self.target_structures) == 3:
            return any([target.is_slot for target in self.target_structures])
        for phrase in self.bubble_chamber.phrases:
            if (
                phrase.rule == self.target_rule
                and phrase.left_branch == self.target_left_branch
                and phrase.right_branch == self.target_right_branch
            ):
                return False
        return True

    def _process_structure(self):
        if len(self.target_structures) == 2:
            chunk = Chunk(
                structure_id=ID.new(Chunk),
                parent_id=self.codelet_id,
                locations=[
                    Location(
                        [[None for _ in range(self.parent_space.no_of_dimensions)]],
                        self.parent_space,
                    )
                ],
                members=StructureCollection(),
                parent_space=self.parent_space,
                quality=1.0,
            )
            label = Label(
                structure_id=ID.new(Label),
                parent_id=self.codelet_id,
                start=chunk,
                parent_concept=self.target_rule.root,
                parent_space=self.parent_space,
                quality=1.0,
            )
            phrase = Phrase(
                structure_id=ID.new(Phrase),
                parent_id=self.codelet_id,
                chunk=chunk,
                label=label,
                quality=0.0,
                rule=self.target_rule,
            )
            phrase.activation = self.INITIAL_STRUCTURE_ACTIVATION
            self.parent_space.add(phrase)
            self.bubble_chamber.phrases.add(phrase)
            self.bubble_chamber.logger.log(chunk)
            self.bubble_chamber.logger.log(label)
            self.bubble_chamber.logger.log(phrase)
            self.child_structures = StructureCollection({phrase})
            if self.target_root is None:
                self.target_root = phrase
            elif self.target_left_branch is None:
                self.target_left_branch = phrase
            elif self.target_right_branch is None:
                self.target_right_branch = phrase
        slot_target = [target for target in self.target_structures if target.is_slot][0]
        if slot_target in [self.target_left_branch, self.target_right_branch]:
            self.target_root.chunk.members.add(slot_target)
        if slot_target == self.target_root:
            self.target_root.chunk.members.add(self.target_left_branch)
            self.target_root.chunk.members.add(self.target_right_branch)
            self.target_root.left_branch = self.target_left_branch
            self.target_root.right_branch = self.target_right_branch
            self.target_root.chunk.value = (
                f"{self.target_left_branch.value} {self.target_right_branch.value}"
            )
            self.target_root.chunk.locations = [
                Location.merge(
                    self.target_left_branch.location, self.target_right_branch.location
                )
            ]
            self.child_structures = StructureCollection({self.target_root})
        self.bubble_chamber.logger.log(self.target_root.chunk)
        self.bubble_chamber.logger.log(self.target_root)

    def _fizzle(self):
        pass

    def _rule_is_compatible_with_targets(self, rule: Concept):
        if self.target_left_branch is not None:
            left_branch_concepts = (
                StructureCollection({self.target_left_branch.parent_concept})
                if not isinstance(self.target_left_branch, Word)
                else StructureCollection(
                    {label.parent_concept for label in self.target_left_branch.labels}
                )
            )
        if self.target_right_branch is not None:
            right_branch_concepts = (
                StructureCollection({self.target_right_branch.parent_concept})
                if not isinstance(self.target_right_branch, Word)
                else StructureCollection(
                    {label.parent_concept for label in self.target_right_branch.labels}
                )
            )
        return (
            (self.target_root is None or self.target_root.parent_concept == rule.root)
            and (
                self.target_left_branch is None
                or rule.left_branch in left_branch_concepts
            )
            and (
                self.target_right_branch is None
                or rule.right_branch in right_branch_concepts
            )
        )
