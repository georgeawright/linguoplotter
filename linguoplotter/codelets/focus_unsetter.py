from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelet import Codelet
from linguoplotter.codelet_result import CodeletResult
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.id import ID
from linguoplotter.structure_collections import StructureDict


class FocusUnsetter(Codelet):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        coderack: "Coderack",
        targets: StructureDict,
        last_satisfaction_score: FloatBetweenOneAndZero,
        time_focus_set: FloatBetweenOneAndZero,
        urgency: FloatBetweenOneAndZero,
    ):
        Codelet.__init__(self, codelet_id, parent_id, bubble_chamber, targets, urgency)
        self.coderack = coderack
        self.last_satisfaction_score = last_satisfaction_score
        self.time_focus_set = time_focus_set
        self.target_view = self.bubble_chamber.focus.view

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        coderack: "Coderack",
        last_satisfaction_score: FloatBetweenOneAndZero,
        time_focus_set: FloatBetweenOneAndZero,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        targets = bubble_chamber.new_dict(name="targets")
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            coderack,
            targets,
            last_satisfaction_score,
            time_focus_set,
            urgency,
        )

    def run(self) -> CodeletResult:
        focus_length = self.coderack.codelets_run - self.time_focus_set
        self.bubble_chamber.focus.recalculate_satisfaction()
        self.bubble_chamber.loggers["activity"].log(
            f"Focus satisfaction: {self.bubble_chamber.focus.satisfaction}"
        )
        current_satisfaction_score = self.bubble_chamber.focus.satisfaction
        self.bubble_chamber.focus.view.quality = current_satisfaction_score
        change_in_satisfaction_score = (
            current_satisfaction_score - self.last_satisfaction_score
        )
        if self.bubble_chamber.focus.frame.number_of_items_left_to_process == 0:
            self.bubble_chamber.time_of_last_successful_focus_unset = (
                self.coderack.codelets_run
            )
            self.bubble_chamber.focus_setters_since_last_successful_focus_unset = 0
        transposed_change_in_satisfaction_score = (
            change_in_satisfaction_score * 0.5
        ) + 0.5
        self.bubble_chamber.loggers["activity"].log(
            f"Current focus satisfaction: {self.bubble_chamber.focus.satisfaction}",
        )
        self.bubble_chamber.loggers["activity"].log(
            f"Change in satisfaction: {change_in_satisfaction_score}",
        )
        self.bubble_chamber.loggers["activity"].log(
            f"Transposed change in satisfaction: {transposed_change_in_satisfaction_score}",
        )
        if (
            self.bubble_chamber.focus.view.unhappiness < self.FLOATING_POINT_TOLERANCE
            and self.bubble_chamber.focus.frame.number_of_items_left_to_process == 0
        ):
            probability_of_unsetting_focus = 1
            self._check_for_and_merge_with_equivalent_views()
            self._update_worldview_setter_urgency()
            self._update_bottom_up_factories_urgencies()
        elif self.bubble_chamber.focus.view.members.filter(
            lambda x: x.parent_concept.is_compound_concept
        ).not_empty:
            probability_of_unsetting_focus = 1
        else:
            probability_of_unsetting_focus = (
                1 - transposed_change_in_satisfaction_score - 1 / focus_length
            )
        self.bubble_chamber.loggers["activity"].log(
            f"Probability of unsetting focus: {probability_of_unsetting_focus}"
        )
        random_number = self.bubble_chamber.random_machine.generate_number()
        self.bubble_chamber.loggers["activity"].log(f"Random number: {random_number}")
        if random_number > probability_of_unsetting_focus:
            self._update_view_driven_factory_urgency()
            self.bubble_chamber.loggers["activity"].log("Focus left set.")
            if change_in_satisfaction_score > 0:
                self.bubble_chamber.focus.view.boost_activation(
                    transposed_change_in_satisfaction_score
                )
                for sub_view in self.bubble_chamber.focus.view.all_sub_views:
                    sub_view.boost_activation(transposed_change_in_satisfaction_score)
            self.result = CodeletResult.FIZZLE
            self._fizzle()
        else:
            if transposed_change_in_satisfaction_score <= 0.5:
                self._update_recycler_urgency()
                self._update_bottom_up_factories_urgencies()
            self.bubble_chamber.focus.view._activation *= (
                transposed_change_in_satisfaction_score
            )
            self.bubble_chamber.focus.view = None
            self.bubble_chamber.focus.frame = None
            self.bubble_chamber.loggers["activity"].log("Focus unset.")
            self._engender_follow_up()
            self.result = CodeletResult.FINISH
        return self.result

    def _update_worldview_setter_urgency(self):
        for codelet in self.coderack._codelets:
            if "WorldviewSetter" in codelet.codelet_id:
                codelet.urgency = self.bubble_chamber.focus.satisfaction
                return
        raise Exception

    def _update_recycler_urgency(self):
        for codelet in self.coderack._codelets:
            if "Recycler" in codelet.codelet_id:
                codelet.urgency = 1.0
                return
        raise Exception

    def _update_view_driven_factory_urgency(self):
        for codelet in self.coderack._codelets:
            if "ViewDrivenFactory" in codelet.codelet_id:
                codelet.urgency = 1.0
                return
        raise Exception

    def _update_bottom_up_factories_urgencies(self):
        for codelet in self.coderack._codelets:
            if (
                "BottomUpSuggesterFactory" in codelet.codelet_id
                or "BottomUpEvaluatorFactory" in codelet.codelet_id
            ):
                codelet.adjust_urgency(1.0 - self.bubble_chamber.worldview.satisfaction)

    def _check_for_and_merge_with_equivalent_views(self):
        # if not self.target_view.super_views.is_empty: return ?
        for view in self.bubble_chamber.views.excluding(self.target_view).filter(
            lambda x: x.super_views.is_empty
            and x.unhappiness < self.FLOATING_POINT_TOLERANCE
        ):
            if self.target_view.is_equivalent_to(view):
                view.quality = 0.0
                view.deactivate()
                self.bubble_chamber.remove(view)
                self.bubble_chamber.loggers["activity"].log(
                    f"Found and removed equivalent view: {view}"
                )

    def _fizzle(self):
        self.child_codelets.append(
            self.spawn(
                parent_id=self.codelet_id,
                bubble_chamber=self.bubble_chamber,
                coderack=self.coderack,
                last_satisfaction_score=self.bubble_chamber.focus.satisfaction,
                time_focus_set=self.time_focus_set,
                urgency=0.5,
            )
        )

    def _engender_follow_up(self):
        from linguoplotter.codelets import FocusSetter

        self.child_codelets.append(
            FocusSetter.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.coderack,
                0.5,
            )
        )
