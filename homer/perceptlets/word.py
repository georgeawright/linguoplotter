import statistics

from homer.concept import Concept
from homer.perceptlet import Perceptlet
from homer.perceptlets.relation import Relation


class Word(Perceptlet):
    """A word for use in text."""

    def __init__(self, text: str, parent_concept: Concept, strength: float):
        location = None
        neighbours = set()
        Perceptlet.__init__(self, text, location, neighbours)
        self.parent_concept = parent_concept
        self.strength = strength
        self.relations = set()

    @property
    def importance(self) -> float:
        return statistics.fmean([self.strength, self.parent_concept.activation])

    @property
    def unhappiness(self) -> float:
        return self._unhappiness_based_on_connections(self.relations)

    def add_relation(self, relation: Relation):
        self.relations.add(relation)
