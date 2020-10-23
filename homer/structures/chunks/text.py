from typing import List

from homer.location import Location
from homer.structures.chunk import Chunk
from homer.structures.link import Link


class Text(Chunk):
    def __init__(
        self,
        location: Location,
        members: List[Structure],
        links_in: List[Link],
        links_out: List[Link],
    ):
        value = " ".join(member.value for member in members)
        location = None
        neighbours = []
        links_in = [] if links_in is None else links_in
        links_out = [] if links_out is None else links_out
        Chunk.__init__(value, location, members, neighbours, links_in, links_out)
