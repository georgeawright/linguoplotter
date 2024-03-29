import pytest
import statistics
from unittest.mock import Mock

from linguoplotter.location import Location
from linguoplotter.structure_collection import StructureCollection
from linguoplotter.structures.nodes import Chunk
from linguoplotter.structures.spaces import ConceptualSpace


@pytest.mark.parametrize(
    "coordinates, n_s_coordinates, w_e_coordinates, nw_se_coordinates, ne_sw_coordinates",
    [([[0, 0]], [[0]], [[0]], [[0]], [[2]])],
)
def test_add(
    coordinates, n_s_coordinates, w_e_coordinates, nw_se_coordinates, ne_sw_coordinates
):

    north_south_space = ConceptualSpace(
        "",
        "",
        "north-south",
        Mock(),
        StructureCollection(Mock(), []),
        1,
        [],
        [],
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        super_space_to_coordinate_function_map={
            "location": lambda location: [[c[0]] for c in location.coordinates]
        },
    )
    west_east_space = ConceptualSpace(
        "",
        "",
        "west-east",
        Mock(),
        StructureCollection(Mock(), []),
        1,
        [],
        [],
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        super_space_to_coordinate_function_map={
            "location": lambda location: [[c[1]] for c in location.coordinates]
        },
    )
    nw_se_space = ConceptualSpace(
        "",
        "",
        "nw-se",
        Mock(),
        StructureCollection(Mock(), []),
        1,
        [],
        [],
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        super_space_to_coordinate_function_map={
            "location": lambda location: [
                [statistics.fmean(c)] for c in location.coordinates
            ]
        },
    )
    ne_sw_space = ConceptualSpace(
        "",
        "",
        "ne-sw",
        Mock(),
        StructureCollection(Mock(), []),
        1,
        [],
        [],
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        super_space_to_coordinate_function_map={
            "location": lambda location: [
                [statistics.fmean([c[0], 4 - c[1]])] for c in location.coordinates
            ]
        },
    )
    location_concept = Mock()
    location_concept.name = "location"
    location_space = ConceptualSpace(
        "",
        "",
        "location",
        location_concept,
        StructureCollection(Mock(), []),
        2,
        [north_south_space, west_east_space],
        [north_south_space, west_east_space, nw_se_space, ne_sw_space],
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        is_basic_level=True,
    )
    location = Location(coordinates, location_space)
    chunk = Chunk(
        "",
        "",
        [location],
        [],
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    location_space.add(chunk)

    assert chunk in location_space.contents
    assert chunk.location_in_space(location_space) == Location(
        coordinates, location_space
    )
    assert chunk in north_south_space.contents
    assert chunk.location_in_space(north_south_space) == Location(
        n_s_coordinates, north_south_space
    )
    assert chunk in west_east_space.contents
    assert chunk.location_in_space(west_east_space) == Location(
        w_e_coordinates, west_east_space
    )
    assert chunk in nw_se_space.contents
    assert chunk.location_in_space(nw_se_space) == Location(
        nw_se_coordinates, nw_se_space
    )
    assert chunk in ne_sw_space.contents
    assert chunk.location_in_space(ne_sw_space) == Location(
        ne_sw_coordinates, ne_sw_space
    )
