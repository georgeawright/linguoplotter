from linguoplotter.codelets.selector import Selector
from linguoplotter.errors import MissingStructureError
from linguoplotter.hyper_parameters import HyperParameters
from linguoplotter.structure_collection_keys import activation, salience
from linguoplotter.structure_collections import StructureSet
from linguoplotter.structures import View


class ViewSelector(Selector):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.suggesters import ViewSuggester

        return ViewSuggester

    @classmethod
    def get_target_class(cls):
        return View

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["view"]

    def _passes_preliminary_checks(self):
        if self.challengers.not_empty:
            return True
        try:
            self._get_challenger()
        except MissingStructureError:
            return True
        return True

    def _engender_follow_up(self):
        try:
            winning_view = self.winners.get()
            if winning_view.unhappiness < HyperParameters.FLOATING_POINT_TOLERANCE:
                target_frame = (
                    StructureSet.union(
                        self.bubble_chamber.new_set(winning_view.parent_frame),
                        winning_view.parent_frame.parent_concept.relatives.where(
                            is_frame=True, is_sub_frame=False
                        ),
                    )
                    .filter(
                        lambda f: self.bubble_chamber.views.filter(
                            lambda v: v.parent_frame.parent_concept == f.parent_concept
                            and v.members.is_empty
                        ).is_empty
                        and not f.is_merged_frame
                    )
                    .get(key=salience)
                )
                self.child_codelets.append(
                    self.get_follow_up_class().make(
                        self.codelet_id,
                        self.bubble_chamber,
                        frame=target_frame,
                        urgency=target_frame.activation,
                    )
                )
        except MissingStructureError:
            pass

    def _get_challenger(self):
        champion = self.champions.get()
        if champion.super_views.not_empty:
            raise MissingStructureError
        self.challengers.add(
            self.bubble_chamber.views.filter(
                lambda x: x.is_fully_active() and x.is_competing_with(champion)
            ).get(key=activation)
        )

    def _fizzle(self):
        pass
