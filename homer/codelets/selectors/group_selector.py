from __future__ import annotations
import statistics
from typing import Optional

from homer.bubble_chamber import BubbleChamber
from homer.bubbles.concepts.perceptlet_type import PerceptletType
from homer.bubbles.perceptlets import Group
from homer.codelets.selector import Selector
from homer.codelets.group_builder import GroupBuilder
from homer.hyper_parameters import HyperParameters
from homer.perceptlet_collection import PerceptletCollection


class GroupSelector(Selector):

    PROPORTION_THRESHOLD = HyperParameters.CONFIDENCE_THRESHOLD

    def __init__(
        self,
        bubble_chamber: BubbleChamber,
        perceptlet_type: PerceptletType,
        target_type: PerceptletType,
        champion: Group,
        urgency: float,
        parent_id: str,
        challenger: Optional[Group] = None,
    ):
        Selector.__init__(
            self,
            bubble_chamber,
            perceptlet_type,
            target_type,
            champion,
            urgency,
            parent_id,
        )
        self.challenger = challenger

    def _passes_preliminary_checks(self) -> bool:
        if self.challenger is None:
            self.challenger = self.bubble_chamber.workspace.groups.at(
                self.location
            ).get_random()
        if self.challenger == self.champion:
            return False
        shared_members = PerceptletCollection.union(
            self.champion.members, self.challenger.members
        )
        shared_champion_ratio = len(shared_members) / len(self.champion.members)
        shared_challenger_ratio = len(shared_members) / len(self.challenger.members)
        return (
            shared_champion_ratio > self.PROPORTION_THRESHOLD
            and shared_challenger_ratio > self.PROPORTION_THRESHOLD
        )

    def _fizzle(self) -> GroupBuilder:
        self.perceptlet_type.activation.decay(self.location)
        return GroupBuilder(
            self.bubble_chamber,
            self.target_type,
            self.bubble_chamber.workspace.raw_perceptlets.at(
                self.location
            ).get_random(),
            self.urgency,
            self.codelet_id,
        )

    def _run_competition(self) -> float:
        size_difference = self.champion.size - self.challenger.size
        connection_activations_difference = (
            self.champion.total_connection_activations()
            - self.challenger.total_connection_activations()
        )
        return statistics.fmean(
            [
                self._difference_score(size_difference),
                self._difference_score(connection_activations_difference),
            ]
        )

    def _engender_follow_up(self) -> GroupSelector:
        winner, loser = (
            (self.champion, self.challenger)
            if self.champion.activation.as_scalar()
            > self.challenger.activation.as_scalar()
            else (self.challenger, self.champion)
        )
        return GroupSelector(
            self.bubble_chamber,
            self.perceptlet_type,
            self.target_type,
            winner,
            loser.exigency,
            self.codelet_id,
            challenger=loser,
        )