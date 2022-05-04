from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelet import Codelet
from linguoplotter.codelet_result import CodeletResult
from linguoplotter.errors import MissingStructureError
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.id import ID
from linguoplotter.hyper_parameters import HyperParameters


class Recycler(Codelet):

    MINIMUM_URGENCY = HyperParameters.MINIMUM_CODELET_URGENCY

    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        coderack: "Coderack",
        urgency: FloatBetweenOneAndZero,
    ):
        Codelet.__init__(self, codelet_id, parent_id, urgency)
        self.bubble_chamber = bubble_chamber
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
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            coderack,
            urgency,
        )

    def run(self) -> CodeletResult:
        try:
            target_view = self.bubble_chamber.views.filter(
                lambda x: x.activation == 0.0
                and x not in self.bubble_chamber.recycle_bin
            ).get()
            self.bubble_chamber.loggers["activity"].log(
                self, f"Found target view: {target_view}"
            )
            self.bubble_chamber.recycle_bin.add(target_view)
            self.result = CodeletResult.FINISH
        except MissingStructureError:
            self.bubble_chamber.loggers["activity"].log(self, f"No target view")
            self.result = CodeletResult.FIZZLE
        self._engender_follow_up()
        self.bubble_chamber.loggers["activity"].log_result(self)
        return self.result

    def _engender_follow_up(self):
        urgency = max(
            min(1, self.MINIMUM_URGENCY * len(self.bubble_chamber.views)),
            self.MINIMUM_URGENCY,
        )
        self.child_codelets.append(
            self.spawn(self.codelet_id, self.bubble_chamber, self.coderack, urgency)
        )
