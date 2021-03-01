from homer.bubble_chamber import BubbleChamber
from homer.codelets.builders import ViewBuilder
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.spaces import WorkingSpace
from homer.structures.views import SimplexView


class SimplexViewBuilder(ViewBuilder):
    @classmethod
    def get_target_class(cls):
        return SimplexView

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber, urgency: float = None):
        target_one = bubble_chamber.spaces["input"]
        target_two = bubble_chamber.frames.get_active()
        urgency = urgency if urgency is not None else target_two.activation
        return cls.spawn(
            parent_id,
            bubble_chamber,
            StructureCollection({target_one, target_two}),
            urgency,
        )

    def _process_structure(self):
        view_id = ID.new(SimplexView)
        view_location = Location([], self.bubble_chamber.spaces["top level working"])
        view_output = WorkingSpace(
            structure_id=ID.new(WorkingSpace),
            parent_id=self.codelet_id,
            name=f"output for {view_id}",
            parent_concept=self.frame.parent_concept,
            conceptual_space=self.frame.conceptual_space,
            locations=[view_location],
            contents=StructureCollection(),
            no_of_dimensions=1,
            dimensions=[],
            sub_spaces=[],
        )
        view = SimplexView(
            structure_id=view_id,
            parent_id=self.codelet_id,
            location=view_location,
            members=StructureCollection(),
            input_spaces=self.target_spaces,
            output_space=view_output,
            quality=0,
        )
        self.bubble_chamber.logger.log(view_output)
        self.bubble_chamber.logger.log(view)
        self.bubble_chamber.views.add(view)
        self.child_structure = view