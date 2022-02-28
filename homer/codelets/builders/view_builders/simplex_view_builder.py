from homer.codelets.builders import ViewBuilder
from homer.id import ID
from homer.location import Location
from homer.structures.spaces import ContextualSpace
from homer.structures.views import SimplexView


class SimplexViewBuilder(ViewBuilder):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.evaluators.view_evaluators import SimplexViewEvaluator

        return SimplexViewEvaluator

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["view-simplex"]

    def _process_structure(self):
        view_id = ID.new(SimplexView)
        input_space_concept = self.contextual_space.parent_concept
        frame_input_space = (
            self.frame.input_space
            if self.frame.input_space.parent_concept == input_space_concept
            else self.frame.output_space
        )
        frame_instance = self.frame.instantiate(
            input_space=frame_input_space,
            conceptual_spaces_map=self.conceptual_spaces_map,
            parent_id=self.codelet_id,
            bubble_chamber=self.bubble_chamber,
        )
        view_output = ContextualSpace(
            structure_id=ID.new(ContextualSpace),
            parent_id=self.codelet_id,
            name=f"output for {view_id}",
            parent_concept=frame_instance.output_space.parent_concept,
            contents=self.bubble_chamber.new_structure_collection(),
            conceptual_spaces=frame_instance.output_space.conceptual_spaces,
            links_in=self.bubble_chamber.new_structure_collection(),
            links_out=self.bubble_chamber.new_structure_collection(),
            parent_spaces=self.bubble_chamber.new_structure_collection(),
        )
        view = SimplexView(
            structure_id=view_id,
            parent_id=self.codelet_id,
            parent_frame=frame_instance,
            locations=[Location([], self.bubble_chamber.spaces["views"])],
            members=self.bubble_chamber.new_structure_collection(),
            frames=self.bubble_chamber.new_structure_collection(frame_instance),
            input_spaces=self.bubble_chamber.new_structure_collection(
                self.contextual_space
            ),
            output_space=view_output,
            quality=0,
            links_in=self.bubble_chamber.new_structure_collection(),
            links_out=self.bubble_chamber.new_structure_collection(),
            parent_spaces=self.bubble_chamber.new_structure_collection(),
        )
        self.bubble_chamber.loggers["structure"].log(view_output)
        self.bubble_chamber.contextual_spaces.add(view_output)
        self.bubble_chamber.loggers["structure"].log(view)
        self.bubble_chamber.views.add(view)
        self._structure_concept.instances.add(view)
        self.child_structures = self.bubble_chamber.new_structure_collection(view)
