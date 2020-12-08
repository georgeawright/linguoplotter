from homer.bubble_chamber import BubbleChamber
from homer.codelets.builders import ViewBuilder
from homer.codelets.selector import Selector
from homer.errors import MissingStructureError
from homer.float_between_one_and_zero import FloatBetweenOneAndZero
from homer.id import ID
from homer.structure_collection import StructureCollection
from homer.structures import Space
from homer.structures.chunks import View


class ViewSelector(Selector):
    def __init__(
        self,
        codelet_id: str,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        champion: View,
        urgency: FloatBetweenOneAndZero,
        challenger: View = None,
    ):
        Selector.__init__(self, codelet_id, parent_id, bubble_chamber, urgency)
        self.champion = champion
        self.challenger = challenger

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        champion: View,
        urgency: FloatBetweenOneAndZero,
        challenger: View = None,
    ):
        codelet_id = ID.new(cls)
        return cls(
            codelet_id,
            parent_id,
            bubble_chamber,
            champion,
            urgency,
            challenger=challenger,
        )

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["view"]

    def _passes_preliminary_checks(self):
        if self.challenger is not None:
            return True
        self.challenger = self.bubble_chamber.views.get_random(exclude=[self.champion])
        members_intersection = StructureCollection.intersection(
            self.champion.members, self.challenger.members
        )
        return len(members_intersection) > 0.5 * len(self.champion.members) and len(
            members_intersection
        ) > 0.5 * len(self.challenger.members)

    def _fizzle(self):
        new_target = self.bubble_chamber.correspondences.get_unhappy()
        self.child_codelets.append(
            ViewBuilder.spawn(
                self.codelet_id,
                self.bubble_chamber,
                new_target,
                new_target.unhappiness,
            )
        )

    def _engender_follow_up(self):
        self.child_codelets.append(
            self.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.champion,
                1 - abs(self.winner.activation - self.loser.activation),
                challenger=self.challenger,
            )
        )
