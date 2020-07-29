from typing import List

from homer.perceptlet import Perceptlet
from homer.perceptlets.raw_perceptlet_field import RawPerceptletField


class RawPerceptletFieldSequence(Perceptlet):
    """A sequence of raw temporal data."""

    def __init__(self, value: List[RawPerceptletField]):
        location = None
        time = None
        neighbours = set()
        Perceptlet.__init__(self, value, location, time, neighbours)
