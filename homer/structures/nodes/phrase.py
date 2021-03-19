from __future__ import annotations
from typing import Union

from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import Node
from homer.structures import Space

from .rule import Rule


class Phrase(Node):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        chunk: "Chunk",
        label: "Label",
        quality: FloatBetweenOneAndZero,
        left_branch: Union[Phrase, "Word"] = None,
        right_branch: Union[Phrase, "Word"] = None,
        rule: Rule = None,
        links_in: StructureCollection = None,
        links_out: StructureCollection = None,
    ):
        Node.__init__(
            self,
            structure_id,
            parent_id,
            value=label.value,
            locations=chunk.locations,
            parent_space=chunk.parent_space,
            quality=quality,
            links_in=links_in,
            links_out=links_out,
        )
        self.chunk = chunk
        self.label = label
        self.left_branch = left_branch
        self.right_branch = right_branch
        self.rule = rule

    @classmethod
    def get_builder_class(cls):
        from homer.codelets.builders import PhraseBuilder

        return PhraseBuilder

    @classmethod
    def get_evaluator_class(cls):
        from homer.codelets.evaluators import PhraseEvaluator

        return PhraseEvaluator

    @classmethod
    def get_selector_class(cls):
        from homer.codelets.selectors import PhraseSelector

        return PhraseSelector

    @property
    def value(self):
        return self.label.value

    @property
    def locations(self):
        return self.chunk.locations

    @property
    def parent_concept(self):
        return self.label.parent_concept

    @property
    def parent_space(self):
        return self.chunk.parent_space

    @property
    def members(self):
        return self.chunk.members

    @property
    def is_slot(self):
        return self.chunk.is_slot

    @property
    def size(self):
        return self.chunk.size

    @property
    def unchunkedness(self):
        return self.chunk.unchunkedness

    @property
    def potential_rule_mates(self) -> StructureCollection:
        return StructureCollection.union(
            self.adjacent, self.super_phrases, self.sub_phrases
        )

    @property
    def adjacent(self) -> StructureCollection:
        """return non-overlapping but touching phrases"""
        from .word import Word

        left = Location([self.location.coordinates[0]], self.parent_space)
        right = Location([self.location.coordinates[-1]], self.parent_space)
        return StructureCollection.union(
            self.parent_space.contents.at(left).of_type(Phrase),
            self.parent_space.contents.at(left).of_type(Word),
            self.parent_space.contents.at(right).of_type(Phrase),
            self.parent_space.contents.at(right).of_type(Word),
        ).of_type(Phrase)

    @property
    def super_phrases(self) -> StructureCollection:
        """return phrases that contain this phrase"""
        return StructureCollection(
            {
                phrase
                for phrase in self.parent_space.contents.of_type(Phrase)
                if self in phrase.members
            }
        )

    @property
    def sub_phrases(self) -> StructureCollection:
        return self.members

    def nearby(self, space: Space = None) -> StructureCollection:
        """return overlapping phrases for selectors to choose between"""
        return StructureCollection(
            {
                phrase
                for phrase in self.parent_space.contents.of_type(Phrase)
                if self.left_branch == phrase.right_branch
                or self.right_branch == phrase.left_branch
            }
        )
