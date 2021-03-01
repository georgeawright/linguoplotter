from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures import View
from homer.structures.spaces import WorkingSpace


class SimplexView(View):
    @classmethod
    def get_builder_class(cls):
        from homer.codelets.builders.view_builders import SimplexViewBuilder

        return SimplexViewBuilder

    @classmethod
    def get_evaluator_class(cls):
        from homer.codelets.evaluators.view_evaluators import SimplexViewEvaluator

        return SimplexViewEvaluator

    @classmethod
    def get_selector_class(cls):
        from homer.codelets.selectors.view_selectors import SimplexViewSelector

        return SimplexViewSelector