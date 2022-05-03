from typing import List

from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.location import Location
from linguoplotter.structure import Structure
from linguoplotter.structure_collection import StructureCollection
from linguoplotter.structures import Node
from linguoplotter.tools import arrange_text_fragments

from .concept import Concept


class Rule(Node):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        name: str,
        location: Location,
        root_concept: Concept,
        left_concept: Concept,
        right_concept: Concept,
        links_in: StructureCollection,
        links_out: StructureCollection,
        parent_spaces: StructureCollection,
        stable_activation: FloatBetweenOneAndZero = None,
    ):
        quality = None
        Node.__init__(
            self,
            structure_id,
            parent_id,
            locations=[location],
            parent_space=location.space,
            quality=quality,
            links_in=links_in,
            links_out=links_out,
            parent_spaces=parent_spaces,
            stable_activation=stable_activation,
        )
        self.name = name
        self._value = name
        self.root_concept = root_concept
        self.left_concept = left_concept
        self.right_concept = right_concept
        self.is_rule = True

    def __dict__(self) -> dict:
        return {}

    @property
    def instance_type(self) -> type:
        return self.left_concept.instance_type

    @property
    def friends(self) -> StructureCollection:
        linked_node_links = StructureCollection.union(
            *[linked_node.relations for linked_node in self.relatives]
        )
        linked_rules = StructureCollection.union(
            *[linked_node_link.arguments for linked_node_link in linked_node_links]
        ).filter(
            lambda x: x != self and x.is_rule and x.parent_space == self.parent_space
        )
        if linked_rules.is_empty():
            linked_rules.add(self)
        return linked_rules

    def compatibility_with(
        self,
        root: Node = None,
        collection: StructureCollection = None,
        branch: str = "left",
    ) -> FloatBetweenOneAndZero:
        if root is None:
            if branch == "left":
                return self.left_concept.classifier.classify(
                    collection=collection, concept=self.left_concept
                )
            if branch == "right" and self.right_concept is not None:
                return self.right_concept.classifier.classify(
                    collection=collection, concept=self.right_concept
                )
            return 0.0
        if branch == "left":
            if self.left_branch_is_free(root):
                return self.left_concept.classifier.classify(
                    collection=collection, concept=self.left_concept
                )
            return 0.0
        if self.right_branch_is_free(root):
            return self.right_concept.classifier.classify(
                collection=collection, concept=self.right_concept
            )
        return 0.0

    def left_branch_is_free(self, root: Node) -> bool:
        return (
            self.left_concept is not None
            and not root.left_branch.where(is_slot=True).is_empty()
        )

    def right_branch_is_free(self, root: Node) -> bool:
        return (
            self.right_concept is not None
            and not root.right_branch.where(is_slot=True).is_empty()
        )

    def is_compatible_with(self, *fragments: List[Structure]) -> bool:
        # TODO: update for chunks
        return True
        if len(fragments) == 1:
            fragment = fragments[0]
            return (
                fragment.parent_concept == self.root
                or fragment.parent_concept == self.left_branch
                or fragment.parent_concept == self.right_branch
                or fragment.has_label(self.left_branch)
                or fragment.has_label(self.right_branch)
            )
        try:
            arranged_fragments = arrange_text_fragments(fragments)
        except Exception:
            return False
        return (
            (
                arranged_fragments["root"] is None
                or arranged_fragments["root"].parent_concept == self.root
            )
            and (
                arranged_fragments["left"] is None
                or arranged_fragments["left"].parent_concept == self.left_branch
                or arranged_fragments["left"].has_label(self.left_branch)
            )
            and (
                arranged_fragments["right"] is None
                or arranged_fragments["right"].parent_concept == self.right_branch
                or arranged_fragments["right"].has_label(self.right_branch)
            )
        )

    def __repr__(self) -> str:
        return f'<{self.structure_id} "{self.name}" in {self.parent_space.name}>'