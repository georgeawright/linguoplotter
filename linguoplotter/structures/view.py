from __future__ import annotations
import statistics
from typing import List

from linguoplotter import fuzzy
from linguoplotter.errors import MissingStructureError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.hyper_parameters import HyperParameters
from linguoplotter.location import Location
from linguoplotter.structure import Structure
from linguoplotter.structure_collection import StructureCollection
from linguoplotter.structures import Frame
from linguoplotter.structures.nodes import Concept
from linguoplotter.structures.space import Space
from linguoplotter.structures.spaces import ContextualSpace


class View(Structure):
    """A collection of spaces and self-consistent correspondences between them."""

    FLOATING_POINT_TOLERANCE = HyperParameters.FLOATING_POINT_TOLERANCE

    CORRESPONDENCE_WEIGHT = HyperParameters.VIEW_QUALITY_CORRESPONDENCE_WEIGHT
    INPUT_WEIGHT = HyperParameters.VIEW_QUALITY_INPUT_WEIGHT

    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        parent_frame: Frame,
        locations: List[Location],
        members: StructureCollection,
        frames: StructureCollection,
        input_spaces: StructureCollection,
        output_space: ContextualSpace,
        quality: FloatBetweenOneAndZero,
        links_in: StructureCollection,
        links_out: StructureCollection,
        parent_spaces: StructureCollection,
        sub_views: StructureCollection,
        super_views: StructureCollection,
        champion_labels: StructureCollection,
        champion_relations: StructureCollection,
    ):
        Structure.__init__(
            self,
            structure_id,
            parent_id,
            locations=locations,
            quality=quality,
            links_in=links_in,
            links_out=links_out,
            parent_spaces=parent_spaces,
            champion_labels=champion_labels,
            champion_relations=champion_relations,
        )
        self.parent_frame = parent_frame
        self.value = None
        self.frames = frames
        self.input_spaces = input_spaces
        self.output_space = output_space
        self.members = members
        self.sub_views = sub_views
        self.super_views = super_views
        self._node_groups = []
        self._grouped_nodes = {}
        self.matched_sub_frames = {}
        self.slot_values = {}
        self.is_view = True

    def __dict__(self) -> dict:
        return {
            "structure_id": self.structure_id,
            "parent_id": self.parent_id,
            "parent_frame": self.parent_frame.structure_id,
            "parent_frame_name": self.parent_frame.name,
            "frames": [frame.structure_id for frame in self.frames],
            "super_views": [view.structure_id for view in self.super_views],
            "sub_views": [view.structure_id for view in self.sub_views],
            "input_spaces": [space.structure_id for space in self.input_spaces],
            "output_space": self.output_space.structure_id,
            "members": [correspondence.structure_id for correspondence in self.members],
            "members_repr": [str(correspondence) for correspondence in self.members],
            "node_groups": [
                {space.structure_id: node.structure_id for space, node in group.items()}
                for group in self._node_groups
            ],
            "grouped_nodes": [node.structure_id for node in self._grouped_nodes],
            "matched_sub_frames": {
                frame_1.structure_id: frame_2.structure_id
                for frame_1, frame_2 in self.matched_sub_frames.items()
            },
            "quality": self.quality,
            "activation": self.activation,
            "unhappiness": self.unhappiness,
        }

    @classmethod
    def get_builder_class(cls):
        from linguoplotter.codelets.builders import ViewBuilder

        return ViewBuilder

    @classmethod
    def get_evaluator_class(cls):
        from linguoplotter.codelets.evaluators import ViewEvaluator

        return ViewEvaluator

    @classmethod
    def get_selector_class(cls):
        from linguoplotter.codelets.selectors import ViewSelector

        return ViewSelector

    @property
    def raw_input_space(self) -> Space:
        return self.input_spaces.filter(
            lambda x: x.parent_concept.name == "input"
        ).get()

    # TODO: this should be a property
    def raw_input_nodes(self):
        return StructureCollection.union(
            *[
                node.raw_members
                for node in self.grouped_nodes
                if node.parent_space in self.input_spaces
            ]
        )

    @property
    def input_contextual_spaces(self):
        return self.input_spaces.where(is_contextual_space=True)

    @property
    def input_slots(self):
        return self.parent_frame.input_space.contents.where(is_slot=True)

    @property
    def output_sub_frame_slots(self):
        return self.parent_frame.output_space.contents.filter(
            lambda x: x.is_slot
            and len(x.parent_spaces.where(is_contextual_space=True)) > 1
        )

    @property
    def size(self):
        return len(self.members)

    @property
    def structures(self):
        return [
            correspondence.start
            for correspondence in self.members
            if correspondence.start.parent_space in self.input_spaces
        ] + [
            node
            for node in self.grouped_nodes
            if node.parent_space in self.input_spaces
        ]

    @property
    def slots(self):
        return self.parent_frame.slots

    @property
    def is_recyclable(self) -> bool:
        return self.activation < self.FLOATING_POINT_TOLERANCE

    @property
    def unfilled_sub_frame_input_structures(self):
        return self.parent_frame.input_space.contents.filter(
            lambda x: not x.is_correspondence
            and not x.is_chunk
            and (
                len(x.correspondences.where(end=x))
                < len(x.parent_spaces.where(is_contextual_space=True)) - 1
            )
        )

    @property
    def unfilled_input_structures(self):
        return self.parent_frame.input_space.contents.filter(
            lambda x: not x.is_correspondence
            and not x.is_chunk
            and x.correspondences.where(end=x).is_empty()
        )

    @property
    def unfilled_output_structures(self):
        return self.parent_frame.output_space.contents.filter(
            lambda x: not x.is_correspondence
            and x.parent_space != self.parent_frame.output_space
            and x.correspondences.where(end=x).is_empty()
        )

    @property
    def unfilled_projectable_structures(self):
        return self.parent_frame.output_space.contents.filter(
            lambda x: not x.is_correspondence
            and x.correspondences_to_space(self.output_space).is_empty()
        )

    @property
    def grouped_nodes(self):
        if self.super_views.is_empty():
            return self._grouped_nodes
        return self.super_views.get().grouped_nodes

    @property
    def node_groups(self):
        if self.super_views.is_empty():
            return self._node_groups
        return self.super_views.get().node_groups

    @property
    def output(self):
        return (
            self.output_space.contents.filter(
                lambda x: x.is_letter_chunk and x.super_chunks.is_empty()
            )
            .get()
            .name
        )

    @property
    def number_of_items_left_to_process(self):
        return sum(
            [
                len(self.unfilled_sub_frame_input_structures),
                len(self.unfilled_input_structures),
                len(self.unfilled_output_structures),
                len(self.unfilled_projectable_structures),
            ]
        )

    def recalculate_unhappiness(self):
        self.unhappiness = 1 - 0.5 ** self.number_of_items_left_to_process

    def recalculate_exigency(self):
        self.recalculate_unhappiness()
        self.exigency = fuzzy.AND(self.unhappiness, self.activation)

    def calculate_quality(self):
        for member in self.members:
            if (
                member.parent_concept.is_compound_concept
                and member.parent_concept.root.name == "not"
            ):
                return 0.0
        total_slots = len(self.members) + self.number_of_items_left_to_process
        correspondence_quality = (
            sum(correspondence.quality for correspondence in self.members) / total_slots
        )
        try:
            input_quality = min(
                correspondence.start.quality
                for correspondence in self.members
                if correspondence.start.parent_space.is_main_input
            )
        except ValueError:
            input_quality = 0
        return sum(
            [
                self.CORRESPONDENCE_WEIGHT * correspondence_quality,
                self.INPUT_WEIGHT * input_quality,
            ]
        )

    def is_equivalent_to(self, other: View):
        try:
            return self.structures == other.structures and self.output == other.output
        except MissingStructureError:
            return False

    def input_overlap_with(self, other: View):
        shared_raw_nodes = StructureCollection.intersection(
            self.raw_input_nodes, other.raw_input_nodes
        )
        proportion_in_self = len(shared_raw_nodes) / len(self.raw_input_nodes)
        proportion_in_other = len(shared_raw_nodes) / len(other.raw_input_nodes)
        return statistics.fmean([proportion_in_self, proportion_in_other])

    def nearby(self, space: Space = None) -> StructureCollection:
        space = space if space is not None else self.location.space
        return (
            space.contents.where(is_view=True)
            .filter(lambda x: self.input_overlap_with(x) > 0.5)
            .excluding(self)
        )

    def decay_activation(self, amount: float = None):
        if amount is None:
            amount = self.MINIMUM_ACTIVATION_UPDATE
        self._activation_buffer -= self._activation_update_coefficient * amount
        for member in self.members:
            member.decay_activation(amount)
        self.output_space.decay_activation(amount)

    def copy(self, **kwargs: dict):
        raise NotImplementedError

    def add(self, correspondence: "Correspondence"):
        self.members.add(correspondence)
        for node_pair in correspondence.node_pairs:
            for node_group in self._node_groups:
                if (
                    node_group.get(node_pair[0].parent_space) == node_pair[0]
                    or node_group.get(node_pair[1].parent_space) == node_pair[1]
                ):
                    node_group[node_pair[0].parent_space] = node_pair[0]
                    node_group[node_pair[1].parent_space] = node_pair[1]
                    self._grouped_nodes[node_pair[0]] = True
                    self._grouped_nodes[node_pair[1]] = True
            if (
                node_pair[0] not in self._grouped_nodes
                or node_pair[1] not in self._grouped_nodes
            ):
                self._node_groups.append(
                    {
                        node_pair[0].parent_space: node_pair[0],
                        node_pair[1].parent_space: node_pair[1],
                    }
                )
                self._grouped_nodes[node_pair[0]] = True
                self._grouped_nodes[node_pair[1]] = True
        if not self.super_views.is_empty():
            self.super_views.get().add(correspondence)

    def remove(self, correspondence: "Correspondence"):
        self.members.remove(correspondence)
        for sub_frame, matched_frame in self.matched_sub_frames.copy().items():
            if (
                correspondence in matched_frame.input_space.contents
                or correspondence in matched_frame.output_space.contents
            ):
                if self.members.filter(
                    lambda x: x in matched_frame.input_space.contents
                    or x in matched_frame.output_space.contents
                ).is_empty():
                    try:
                        sub_view = self.sub_views.where(
                            parent_frame=matched_frame
                        ).get()
                        sub_view.super_views.remove(self)
                        self.sub_views.remove(sub_view)
                    except MissingStructureError:
                        pass
                    self.frames.remove(sub_frame)
                    self.matched_sub_frames.pop(sub_frame)
        self._grouped_nodes = {}
        self._node_groups = []
        for member in self.members:
            self.add(member)
        if not self.super_views.is_empty():
            self.super_views.get().remove(correspondence)

    def has_member(
        self,
        parent_concept: Concept,
        conceptual_space: Space,
        start: Structure,
        end: Structure,
    ) -> bool:
        return not self.members.where(
            parent_concept=parent_concept,
            conceptual_space=conceptual_space,
            start=start,
            end=end,
        ).is_empty()

    def can_accept_member(
        self,
        parent_concept: Concept,
        conceptual_space: Space,
        start: Structure,
        end: Structure,
        sub_view: View = None,
    ) -> bool:
        if self.has_member(parent_concept, conceptual_space, start, end):
            return False
        if (
            start.is_link
            and end.is_link
            and (not start.parent_concept.is_slot or start.parent_concept.is_filled_in)
        ):
            start_concept = (
                start.parent_concept
                if not start.parent_concept.is_slot
                else start.parent_concept.non_slot_value
            )
            end_concept = end.parent_concept
            if end_concept.is_slot:
                for relative in end_concept.relatives.filter(
                    lambda x: x in self.parent_frame.concepts
                ):
                    relation_concept = (
                        end_concept.relations_with(relative).get().parent_concept
                    )
                    if relation_concept.name == "different":
                        continue
                    if relative.is_slot and relative.is_filled_in:
                        relative_concept = relative.non_slot_value
                        if not start_concept.has_relation_with(
                            relative_concept, relation_concept
                        ):
                            return False
                    if not relative.is_slot:
                        if not start_concept.has_relation_with(
                            end_concept, relation_concept
                        ):
                            return False
            different_concepts = end_concept.relatives.filter(
                lambda x: not x.relations_with(end_concept)
                .where(name="different")
                .is_empty()
            )
            if start_concept in different_concepts:
                return False
        if not end.correspondences.filter(
            lambda x: x.end == end
            and x in self.members
            and x.start in start.parent_space.contents
        ).is_empty():
            return False
        potential_node_groups = (
            [{start.parent_space: start, end.parent_space: end}]
            if start.is_node
            else [
                {
                    start.start.parent_space: start.start,
                    end.start.parent_space: end.start,
                }
            ]
            if start.is_label
            else [
                {
                    start.start.parent_space: start.start,
                    end.start.parent_space: end.start,
                },
                {
                    start.end.parent_space: start.end,
                    end.end.parent_space: end.end,
                },
            ]
        )
        if sub_view is not None:
            for potential_node_group in potential_node_groups:
                for sub_view_node_group in sub_view.node_groups:
                    if any(
                        [
                            node in sub_view_node_group.values()
                            for node in potential_node_group.values()
                        ]
                    ):
                        for space in sub_view_node_group:
                            potential_node_group[space] = sub_view_node_group[space]
        for existing_node_group in self.node_groups:
            for potential_group in potential_node_groups:
                shared_spaces = [
                    space for space in existing_node_group if space in potential_group
                ]
                if (
                    len(shared_spaces) > 1
                    and any(
                        existing_node_group[space] == potential_group[space]
                        for space in shared_spaces
                    )
                    and not all(
                        existing_node_group[space] == potential_group[space]
                        for space in shared_spaces
                    )
                ):
                    return False
        if self.super_views.is_empty():
            return True
        return self.super_views.get().can_accept_member(
            parent_concept,
            conceptual_space,
            start,
            end,
        )

    def spread_activation(self):
        if self.is_fully_active():
            self.parent_frame.parent_concept.boost_activation(self.quality)
            self.parent_frame.progenitor.boost_activation(self.quality)

    def __repr__(self) -> str:
        inputs = ", ".join([space.structure_id for space in self.input_spaces])
        return (
            f"<{self.structure_id} "
            + f"from {inputs} to {self.output_space.structure_id} "
            + f"with {self.parent_frame}>"
        )

    def to_long_string(self) -> str:
        def space_to_long_string(space):
            string = "-" * 120 + "\n"
            string += f"{space.structure_id}\n"
            string += "-" * 120 + "\n"
            for structure in space.contents.filter(
                lambda x: not x.correspondences.filter(
                    lambda y: y in self.members
                ).is_empty()
            ):
                string += f"{structure}\n"
            return string

        string = "-" * 120 + "\n"
        string += f"{self.structure_id}\n"
        string += "-" * 120 + "\n"
        string += "Inputs:\n"
        for input_space in self.input_spaces:
            string += space_to_long_string(input_space)
        string += "Frames:'n"
        for frame in self.frames:
            string += "-" * 120 + "\n"
            string += f"{frame.structure_id}\n"
            string += space_to_long_string(frame.input_space)
            string += space_to_long_string(frame.output_space)
        string += "-" * 120 + "\n"
        string += "Output:\n" + space_to_long_string(self.output_space)
        string += "-" * 120 + "\n"
        string += "Correspondences:\n"
        for correspondence in self.members:
            string += f"{correspondence}\n"
        return string

    def to_concise_dot_string(self) -> str:
        dot_string = """
digraph G {"""
        cluster_count = 0
        for space in self.input_spaces:
            dot_string += f"""
subgraph cluster_{cluster_count} {{
    style=filled;
    color=lightblue;
    node [style=filled, color=white];"""
            for node in space.contents.filter(
                lambda x: x.is_node and x in self.grouped_nodes
            ):
                node_label = (
                    node.name
                    if node.is_letter_chunk and node.name is not None
                    else node.structure_id
                )
                dot_string += f"""
    {node.structure_id} [label="{node_label}"];"""
            for letter_chunk in space.contents.filter(
                lambda x: x.is_letter_chunk and x.in_self.grouped_nodes
            ):
                for left_member in letter_chunk.left_branch:
                    dot_string += f"""
    {letter_chunk.structure_id} -> {left_member.structure_id} [label="left"];"""
                for right_member in letter_chunk.right_branch:
                    dot_string += f"""
    {letter_chunk.structure_id} -> {right_member.structure_id} [label="right"];"""
            for label in space.contents.filter(
                lambda x: x.is_label and x.has_correspondence_in_view(self)
            ):
                dot_string += f"""
    {label.structure_id} [label="{label.parent_concept.name}"];
    {label.structure_id} -> {label.start.structure_id} [label="start"];"""
            for relation in space.contents.filter(
                lambda x: x.is_relation and x.has_correspondence_in_view(self)
            ):
                concept_label = (
                    relation.parent_concept.name
                    if not relation.parent_concept.is_slot
                    else relation.structure_id
                )
                dot_string += f"""
    {relation.structure_id} [label="{relation.parent_concept.name}"];
    {relation.structure_id} -> {relation.start.structure_id} [label="start"];
    {relation.structure_id} -> {relation.end.structure_id} [label="end"];"""
            dot_string += f"""
    label = "{space.structure_id}";
}}"""
            cluster_count += 1
        dot_string += f"""
subgraph cluster_{cluster_count} {{
    style=filled;
    color=palegreen;
    node [style=filled, color=white];"""
        for node in self.output_space.contents.where(is_node=True):
            node_label = (
                node.name
                if node.is_letter_chunk and node.name is not None
                else node.structure_id
            )
            dot_string += f"""
    {node.structure_id} [label="{node_label}"];"""
        for letter_chunk in self.output_space.contents.where(is_letter_chunk=True):
            for left_member in letter_chunk.left_branch:
                dot_string += f"""
    {letter_chunk.structure_id} -> {left_member.structure_id} [label="left"];"""
            for right_member in letter_chunk.right_branch:
                dot_string += f"""
    {letter_chunk.structure_id} -> {right_member.structure_id} [label="right"];"""
        for label in self.output_space.contents.where(is_label=True):
            dot_string += f"""
    {label.structure_id} [label="{label.parent_concept.name}"];
    {label.structure_id} -> {label.start.structure_id} [label="start"];"""
        for relation in self.output_space.contents.where(is_relation=True):
            dot_string += f"""
    {relation.structure_id} [label="{relation.parent_concept.name}"];
    {relation.structure_id} -> {relation.start.structure_id} [label="start"];
    {relation.structure_id} -> {relation.end.structure_id} [label="end"];"""
        dot_string += f"""
    label = "{self.output_space.structure_id}";
}}"""
        cluster_count += 1
        dot_string += f"""
subgraph cluster_{cluster_count} {{
    style=filled;
    color=lightgray;
    node [style=filled, color=white];"""
        cluster_count += 1
        dot_string += f"""
    subgraph cluster_{cluster_count} {{
        style=filled;
        color=pink;
        node [style=filled, color=white];"""
        for concept in self.parent_frame.concepts.where(is_concept=True):
            dot_string += f"""
        {concept.structure_id};"""
        for concept in self.parent_frame.concepts.where(is_concept=True):
            for relation in concept.links_out.filter(
                lambda x: x.is_relation and x.end in self.parent_frame.concepts
            ):
                dot_string += f"""
        {relation.structure_id} [label={relation.parent_concept.name}];
        {relation.structure_id} -> {relation.start.structure_id} [label="start"];
        {relation.structure_id} -> {relation.end.structure_id} [label="end"];"""
        dot_string += f"""
        label = "Concepts";
    }}"""
        cluster_count += 1
        dot_string += f"""
    subgraph cluster_{cluster_count} {{
        style=filled;
        color=lightblue;
        node [style=filled, color=white];"""
        for node in self.parent_frame.input_space.contents.where(is_node=True):
            node_label = (
                node.name
                if node.is_letter_chunk and node.name is not None
                else node.structure_id
            )
            dot_string += f"""
        {node.structure_id} [label="{node_label}"];"""
        for letter_chunk in self.parent_frame.input_space.contents.where(
            is_letter_chunk=True
        ):
            for left_member in letter_chunk.left_branch:
                dot_string += f"""
        {letter_chunk.structure_id} -> {left_member.structure_id} [label="left"];"""
            for right_member in letter_chunk.right_branch:
                dot_string += f"""
        {letter_chunk.structure_id} -> {right_member.structure_id} [label="right"];"""
        for label in self.parent_frame.input_space.contents.where(is_label=True):
            concept_label = (
                label.parent_concept.name
                if not label.parent_concept.is_slot
                else label.structure_id
            )
            dot_string += f"""
        {label.structure_id} [label="{concept_label}"];
        {label.structure_id} -> {label.start.structure_id} [label="start"];"""
        for relation in self.parent_frame.input_space.contents.where(is_relation=True):
            concept_label = (
                relation.parent_concept.name
                if not relation.parent_concept.is_slot
                else relation.structure_id
            )
            dot_string += f"""
        {relation.structure_id} [label="{concept_label}"];
        {relation.structure_id} -> {relation.start.structure_id} [label="start"];
        {relation.structure_id} -> {relation.end.structure_id} [label="end"];"""
        dot_string += f"""
        label = "{self.parent_frame.input_space.structure_id}";
    }}"""
        cluster_count += 1
        dot_string += f"""
    subgraph cluster_{cluster_count} {{
        style=filled;
        color=palegreen;
        node [style=filled, color=white];"""
        for node in self.parent_frame.output_space.contents.where(is_node=True):
            node_label = (
                node.name
                if node.is_letter_chunk and node.name is not None
                else node.structure_id
            )
            dot_string += f"""
        {node.structure_id} [label="{node_label}"];"""
        for letter_chunk in self.parent_frame.output_space.contents.where(
            is_letter_chunk=True
        ):
            for left_member in letter_chunk.left_branch:
                dot_string += f"""
        {letter_chunk.structure_id} -> {left_member.structure_id} [label="left"];"""
            for right_member in letter_chunk.right_branch:
                dot_string += f"""
        {letter_chunk.structure_id} -> {right_member.structure_id} [label="right"];"""
        for label in self.parent_frame.output_space.contents.where(is_label=True):
            concept_label = (
                label.parent_concept.name
                if not label.parent_concept.is_slot
                else label.structure_id
            )
            dot_string += f"""
        {label.structure_id} [label="{concept_label}"];
        {label.structure_id} -> {label.start.structure_id} [label="start"];"""
        for relation in self.parent_frame.output_space.contents.where(is_relation=True):
            concept_label = (
                relation.parent_concept.name
                if not relation.parent_concept.is_slot
                else relation.structure_id
            )
            dot_string += f"""
        {relation.structure_id} [label="{concept_label}"];
        {relation.structure_id} -> {relation.start.structure_id} [label="start"];
        {relation.structure_id} -> {relation.end.structure_id} [label="end"];"""
        dot_string += f"""
        label = "{self.parent_frame.output_space.structure_id}";
    }}"""
        for label in self.parent_frame.input_space.contents.where(is_label=True):
            if label.parent_concept in self.parent_frame.concepts:
                dot_string += f"""
    {label.structure_id} -> {label.parent_concept.structure_id} [label="parent_concept"];"""
        for relation in self.parent_frame.input_space.contents.where(is_relation=True):
            if relation.parent_concept in self.parent_frame.concepts:
                dot_string += f"""
    {relation.structure_id} -> {relation.parent_concept.structure_id} [label="parent_concept"];"""
        for label in self.parent_frame.output_space.contents.where(is_label=True):
            if label.parent_concept in self.parent_frame.concepts:
                dot_string += f"""
    {label.structure_id} -> {label.parent_concept.structure_id} [label="parent_concept"];"""
        for relation in self.parent_frame.output_space.contents.where(is_relation=True):
            if relation.parent_concept in self.parent_frame.concepts:
                dot_string += f"""
    {relation.structure_id} -> {relation.parent_concept.structure_id} [label="parent_concept"];"""
        dot_string += f"""
    label = "{self.parent_frame.structure_id}";
}}"""
        for correspondence in self.members:
            if (
                correspondence.start.parent_space in self.input_spaces
                or correspondence.start in self.parent_frame.output_space.contents
            ) and (
                correspondence.end in self.parent_frame.input_space.contents
                or correspondence.end in self.output_space.contents
            ):
                dot_string += f"""
    {correspondence.structure_id} [label="{correspondence.parent_concept.name}"];
    {correspondence.structure_id} -> {correspondence.start.structure_id};
    {correspondence.structure_id} -> {correspondence.end.structure_id};"""
        dot_string += """
}"""
        return dot_string

    def to_long_dot_string(self) -> str:
        # TODO: should show sub_view output spaces and letter chunk names
        # TODO: check why frame elements have the wrong parent concept
        dot_string = """
digraph G {"""
        cluster_count = 0
        for space in self.input_spaces:
            dot_string += f"""
subgraph cluster_{cluster_count} {{
    style=filled;
    color=lightblue;
    node [style=filled, color=white];"""
            for node in space.contents.filter(
                lambda x: x.is_node and x in self.grouped_nodes
            ):
                dot_string += f"""
    {node.structure_id};"""
            for letter_chunk in space.contents.filter(
                lambda x: x.is_letter_chunk and x.in_self.grouped_nodes
            ):
                for left_member in letter_chunk.left_branch:
                    dot_string += f"""
    {letter_chunk.structure_id} -> {left_member.structure_id} [label="left"];"""
                for right_member in letter_chunk.right_branch:
                    dot_string += f"""
    {letter_chunk.structure_id} -> {right_member.structure_id} [label="right"];"""
            for label in space.contents.filter(
                lambda x: x.is_label and x.has_correspondence_in_view(self)
            ):
                dot_string += f"""
    {label.structure_id} [label="{label.parent_concept.name}"];
    {label.structure_id} -> {label.start.structure_id} [label="start"];"""
            for relation in space.contents.filter(
                lambda x: x.is_relation and x.has_correspondence_in_view(self)
            ):
                concept_label = (
                    relation.parent_concept.name
                    if not relation.parent_concept.is_slot
                    else relation.structure_id
                )
                dot_string += f"""
    {relation.structure_id} [label="{relation.parent_concept.name}"];
    {relation.structure_id} -> {relation.start.structure_id} [label="start"];
    {relation.structure_id} -> {relation.end.structure_id} [label="end"];"""
            dot_string += f"""
    label = "{space.structure_id}";
}}"""
            cluster_count += 1
        dot_string += f"""
subgraph cluster_{cluster_count} {{
    style=filled;
    color=palegreen;
    node [style=filled, color=white];"""
        for node in self.output_space.contents.where(is_node=True):
            dot_string += f"""
    {node.structure_id};"""
        for letter_chunk in self.output_space.contents.where(is_letter_chunk=True):
            for left_member in letter_chunk.left_branch:
                dot_string += f"""
    {letter_chunk.structure_id} -> {left_member.structure_id} [label="left"];"""
            for right_member in letter_chunk.right_branch:
                dot_string += f"""
    {letter_chunk.structure_id} -> {right_member.structure_id} [label="right"];"""
        for label in self.output_space.contents.where(is_label=True):
            dot_string += f"""
    {label.structure_id} [label="{label.parent_concept.name}"];
    {label.structure_id} -> {label.start.structure_id} [label="start"];"""
        for relation in self.output_space.contents.where(is_relation=True):
            dot_string += f"""
    {relation.structure_id} [label="{relation.parent_concept.name}"];
    {relation.structure_id} -> {relation.start.structure_id} [label="start"];
    {relation.structure_id} -> {relation.end.structure_id} [label="end"];"""
        dot_string += f"""
    label = "{self.output_space.structure_id}";
}}"""
        cluster_count += 1
        for frame in self.frames:
            dot_string += f"""
subgraph cluster_{cluster_count} {{
    style=filled;
    color=lightgray;
    node [style=filled, color=white];"""
            cluster_count += 1
            dot_string += f"""
    subgraph cluster_{cluster_count} {{
        style=filled;
        color=pink;
        node [style=filled, color=white];"""
            for concept in frame.concepts.where(is_concept=True):
                dot_string += f"""
        {concept.structure_id};"""
            for concept in frame.concepts.where(is_concept=True):
                for relation in concept.links_out.filter(
                    lambda x: x.is_relation and x.end in frame.concepts
                ):
                    dot_string += f"""
        {relation.structure_id} [label={relation.parent_concept.name}];
        {relation.structure_id} -> {relation.start.structure_id} [label="start"];
        {relation.structure_id} -> {relation.end.structure_id} [label="end"];"""
            dot_string += f"""
        label = "Concepts";
    }}"""
            cluster_count += 1
            dot_string += f"""
    subgraph cluster_{cluster_count} {{
        style=filled;
        color=lightblue;
        node [style=filled, color=white];"""
            for node in frame.input_space.contents.where(is_node=True):
                dot_string += f"""
        {node.structure_id};"""
            for letter_chunk in frame.input_space.contents.where(is_letter_chunk=True):
                for left_member in letter_chunk.left_branch:
                    dot_string += f"""
        {letter_chunk.structure_id} -> {left_member.structure_id} [label="left"];"""
                for right_member in letter_chunk.right_branch:
                    dot_string += f"""
        {letter_chunk.structure_id} -> {right_member.structure_id} [label="right"];"""
            for label in frame.input_space.contents.where(is_label=True):
                concept_label = (
                    label.parent_concept.name
                    if not label.parent_concept.is_slot
                    else label.structure_id
                )
                dot_string += f"""
        {label.structure_id} [label="{concept_label}"];
        {label.structure_id} -> {label.start.structure_id} [label="start"];"""
            for relation in frame.input_space.contents.where(is_relation=True):
                concept_label = (
                    relation.parent_concept.name
                    if not relation.parent_concept.is_slot
                    else relation.structure_id
                )
                dot_string += f"""
        {relation.structure_id} [label="{concept_label}"];
        {relation.structure_id} -> {relation.start.structure_id} [label="start"];
        {relation.structure_id} -> {relation.end.structure_id} [label="end"];"""
            dot_string += f"""
        label = "{frame.input_space.structure_id}";
    }}"""
            cluster_count += 1
            dot_string += f"""
    subgraph cluster_{cluster_count} {{
        style=filled;
        color=palegreen;
        node [style=filled, color=white];"""
            for node in frame.output_space.contents.where(is_node=True):
                dot_string += f"""
        {node.structure_id};"""
            for letter_chunk in frame.output_space.contents.where(is_letter_chunk=True):
                for left_member in letter_chunk.left_branch:
                    dot_string += f"""
        {letter_chunk.structure_id} -> {left_member.structure_id} [label="left"];"""
                for right_member in letter_chunk.right_branch:
                    dot_string += f"""
        {letter_chunk.structure_id} -> {right_member.structure_id} [label="right"];"""
            for label in frame.output_space.contents.where(is_label=True):
                concept_label = (
                    label.parent_concept.name
                    if not label.parent_concept.is_slot
                    else label.structure_id
                )
                dot_string += f"""
        {label.structure_id} [label="{concept_label}"];
        {label.structure_id} -> {label.start.structure_id} [label="start"];"""
            for relation in frame.output_space.contents.where(is_relation=True):
                concept_label = (
                    relation.parent_concept.name
                    if not relation.parent_concept.is_slot
                    else relation.structure_id
                )
                dot_string += f"""
        {relation.structure_id} [label="{concept_label}"];
        {relation.structure_id} -> {relation.start.structure_id} [label="start"];
        {relation.structure_id} -> {relation.end.structure_id} [label="end"];"""
            dot_string += f"""
        label = "{frame.output_space.structure_id}";
    }}"""
            for label in frame.input_space.contents.where(is_label=True):
                if label.parent_concept in frame.concepts:
                    dot_string += f"""
    {label.structure_id} -> {label.parent_concept.structure_id} [label="parent_concept"];"""
            for relation in frame.input_space.contents.where(is_relation=True):
                if relation.parent_concept in frame.concepts:
                    dot_string += f"""
    {relation.structure_id} -> {relation.parent_concept.structure_id} [label="parent_concept"];"""
            for label in frame.output_space.contents.where(is_label=True):
                if label.parent_concept in frame.concepts:
                    dot_string += f"""
    {label.structure_id} -> {label.parent_concept.structure_id} [label="parent_concept"];"""
            for relation in frame.output_space.contents.where(is_relation=True):
                if relation.parent_concept in frame.concepts:
                    dot_string += f"""
    {relation.structure_id} -> {relation.parent_concept.structure_id} [label="parent_concept"];"""
            dot_string += f"""
    label = "{frame.structure_id}";
}}"""
        for correspondence in self.members:
            #            dot_string += f"""
            #    {correspondence.structure_id} [label="{correspondence.parent_concept.name}"];
            #    {correspondence.structure_id} -> {correspondence.start.structure_id};
            #    {correspondence.structure_id} -> {correspondence.end.structure_id};"""
            dot_string += f"""
    {correspondence.start.structure_id} -> {correspondence.end.structure_id};"""
        dot_string += """
}"""
        return dot_string
