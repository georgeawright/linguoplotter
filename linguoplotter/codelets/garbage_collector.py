from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelet import Codelet
from linguoplotter.codelet_result import CodeletResult
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.id import ID
from linguoplotter.hyper_parameters import HyperParameters
from linguoplotter.structure_collections import StructureDict


class GarbageCollector(Codelet):

    MINIMUM_URGENCY = HyperParameters.MINIMUM_CODELET_URGENCY

    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        coderack: "Coderack",
        targets: StructureDict,
        urgency: FloatBetweenOneAndZero,
    ):
        Codelet.__init__(self, codelet_id, parent_id, bubble_chamber, targets, urgency)
        self.coderack = coderack

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        coderack: "Coderack",
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        targets = bubble_chamber.new_dict(name="targets")
        return cls(codelet_id, parent_id, bubble_chamber, coderack, targets, urgency)

    def run(self) -> CodeletResult:
        if self.bubble_chamber.recycle_bin.is_empty:
            self.result = CodeletResult.FIZZLE
        else:
            self._remove_items()
            self.result = CodeletResult.FINISH
        self._engender_follow_up()
        return self.result

    def _remove_items(self):
        # TODO: don't delete interspatial relations
        for structure in self.bubble_chamber.recycle_bin:
            if not structure.is_recyclable:
                self.bubble_chamber.recycle_bin.remove(structure)
                continue
            if structure is self.bubble_chamber.focus.view:
                self.bubble_chamber.recycle_bin.remove(structure)
                continue
            if any(
                [
                    structure in codelet.targets.values()
                    or any(
                        [link in codelet.targets.values() for link in structure.links]
                    )
                    or (
                        isinstance(codelet.targets, StructureDict)
                        and codelet.targets["view"] is not None
                        and (
                            structure in codelet.targets["view"].structures
                            or structure in codelet.targets["view"].sub_views
                        )
                    )
                    for codelet in self.coderack._codelets
                ]
            ):
                self.bubble_chamber.recycle_bin.remove(structure)
                continue
            if self.bubble_chamber.worldview.views.not_empty and (
                any(
                    structure in view.grouped_nodes
                    for view in self.bubble_chamber.worldview.views
                )
                or any(
                    structure in view.members
                    for view in self.bubble_chamber.worldview.views
                )
            ):
                self.bubble_chamber.recycle_bin.remove(structure)
                continue
            probability_of_removal = (
                self.bubble_chamber.random_machine.generate_number()
            )
            if probability_of_removal > self.bubble_chamber.general_satisfaction:
                self.bubble_chamber.loggers["activity"].log(f"Removing {structure}")
                self.bubble_chamber.recycle_bin.remove(structure)
                self.bubble_chamber.remove(structure)

    def _engender_follow_up(self):
        urgency = max(
            min(1, self.MINIMUM_URGENCY * len(self.bubble_chamber.recycle_bin)),
            self.MINIMUM_URGENCY,
        )
        self.child_codelets.append(
            self.spawn(self.codelet_id, self.bubble_chamber, self.coderack, urgency)
        )
