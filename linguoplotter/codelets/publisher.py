import statistics

from linguoplotter import fuzzy
from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelet import Codelet
from linguoplotter.codelet_result import CodeletResult
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.hyper_parameters import HyperParameters
from linguoplotter.id import ID
from linguoplotter.structure_collections import StructureDict


class Publisher(Codelet):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        coderack: "Coderack",
        targets: StructureDict,
        last_satisfaction: FloatBetweenOneAndZero,
        last_time: int,
        urgency: FloatBetweenOneAndZero,
    ):
        Codelet.__init__(self, codelet_id, parent_id, bubble_chamber, targets, urgency)
        self.coderack = coderack
        self.last_satisfaction = last_satisfaction
        self.last_time = last_time

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        coderack: "Coderack",
        last_satisfaction: FloatBetweenOneAndZero,
        last_time: int,
        urgency: FloatBetweenOneAndZero,
    ):
        MINIMUM_CODELET_URGENCY = (
            bubble_chamber.hyper_parameters.MINIMUM_CODELET_URGENCY
        )
        targets = bubble_chamber.new_dict(name="targets")
        urgency = max(urgency, MINIMUM_CODELET_URGENCY)
        return cls(
            ID.new(cls),
            parent_id,
            bubble_chamber,
            coderack,
            targets,
            last_satisfaction,
            last_time,
            urgency,
        )

    def run(self) -> CodeletResult:
        if self.bubble_chamber.worldview.view is None:
            self.bubble_chamber.loggers["activity"].log("Worldview is empty.")
            self._update_bottom_up_factories_urgencies()
            self._fizzle()
            self.result = CodeletResult.FIZZLE
            return
        self.bubble_chamber.loggers["activity"].log("Worldview is not empty.")
        if self.bubble_chamber.focus.view is not None:
            self.bubble_chamber.loggers["activity"].log("Focus is not empty.")
            self.bubble_chamber.concepts["publish"].decay_activation(
                self.bubble_chamber.focus.view.salience
            )
            self._update_focus_codelet_urgencies()
            self._fizzle()
            self.result = CodeletResult.FIZZLE
            return
        self.bubble_chamber.loggers["activity"].log("Focus is empty.")
        satisfaction_difference = (
            self.bubble_chamber.general_satisfaction - self.last_satisfaction
        )
        time_difference = self.coderack.codelets_run - self.last_time
        satisfaction_gradient = satisfaction_difference / time_difference
        self.bubble_chamber.loggers["activity"].log(
            f"Satisfaction gradient: {satisfaction_gradient}"
        )
        if satisfaction_gradient > 0 and self.bubble_chamber.random_machine.coin_flip():
            self.bubble_chamber.loggers["activity"].log(
                "Satisfaction is increasing too much."
            )
            self.bubble_chamber.concepts["publish"].decay_activation(
                satisfaction_gradient
            )
            self._fizzle()
            self.result = CodeletResult.FIZZLE
            return
        publish_concept = self.bubble_chamber.concepts["publish"]
        self.bubble_chamber.loggers["activity"].log(
            f"Publish concept activation: {publish_concept.activation}"
        )
        if not publish_concept.is_fully_active():
            self.bubble_chamber.loggers["activity"].log("Boosting publish concept")
            self.bubble_chamber.loggers["activity"].log(
                f"Worldview Satisfaction: {self.bubble_chamber.worldview.satisfaction}"
            )
            publish_concept.boost_activation(
                publish_concept.activation
                + HyperParameters.MINIMUM_ACTIVATION_UPDATE
                # fuzzy.OR(
                #    self.bubble_chamber.worldview.satisfaction,
                #    publish_concept.activation,
                # )
                # statistics.fmean(
                #    [self.bubble_chamber.worldview.satisfaction, self.urgency]
                # )
            )
            self._fizzle()
            self.result = CodeletResult.FIZZLE
            return
        self.bubble_chamber.loggers["activity"].log("Publishing")
        self.bubble_chamber.result = self.bubble_chamber.worldview.output
        self.result = CodeletResult.FINISH

    def _fizzle(self) -> CodeletResult:
        urgency = (
            fuzzy.OR(self.bubble_chamber.worldview.satisfaction, self.urgency)
            if self.last_satisfaction <= self.bubble_chamber.general_satisfaction
            and self.bubble_chamber.focus.view is None
            and self.bubble_chamber.worldview.view is not None
            else self.bubble_chamber.worldview.satisfaction
        )
        self.child_codelets.append(
            self.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.coderack,
                last_satisfaction=self.bubble_chamber.general_satisfaction,
                last_time=self.coderack.codelets_run,
                urgency=urgency,
            )
        )

    def _update_bottom_up_factories_urgencies(self):
        for codelet in self.coderack._codelets:
            if (
                "BottomUpSuggesterFactory" in codelet.codelet_id
                or "BottomUpEvaluatorFactory" in codelet.codelet_id
            ):
                codelet.adjust_urgency(1.0 - self.bubble_chamber.worldview.satisfaction)

    def _update_focus_codelet_urgencies(self):
        for codelet in self.coderack._codelets:
            if "Focus" in codelet.codelet_id:
                codelet.adjust_urgency(1.0 - self.bubble_chamber.worldview.satisfaction)
