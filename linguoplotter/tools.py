import math
import statistics
from typing import Iterable, List, Union


def generalized_mean(
    values: list, weights: list = None, exponent: float = 1.0, tolerance: float = 0.0
):
    weights = [1 for _ in values] if weights is None else weights
    if exponent == 0:
        return math.prod([(v + tolerance) ** w for w, v in zip(weights, values)]) ** (
            1 / sum(weights)
        )
    if exponent == math.inf:
        return max(values)
    if exponent == -math.inf:
        return min(values)
    return (
        sum([w * (v + tolerance) ** exponent for w, v in zip(weights, values)])
        / sum(weights)
    ) ** (1 / exponent)


def shortest_distance(a, b, return_nan: bool = False) -> float:
    nan_return_value = math.nan if return_nan else 0.0
    distance = min([math.dist(a_point, b_point) for a_point in a for b_point in b])
    return distance if not math.isnan(distance) else nan_return_value


def average_euclidean_distance(a, b, return_nan: bool = False) -> float:
    distances = []
    for a_coords in a:
        for b_coords in b:
            distance = math.dist(a_coords, b_coords)
            if math.isnan(distance):
                return math.nan if return_nan else 0.0
            distances.append(distance)
    return statistics.fmean(distances)


def centroid_euclidean_distance(a, b, return_nan: bool = False) -> float:
    nan_return_value = math.nan if return_nan else 0.0
    if len(a) == len(b) == 0:
        # TODO: possibly get rid of this if statment
        return 0.0
    distance = math.dist(average_vector(a), average_vector(b))
    return distance if not math.isnan(distance) else nan_return_value


def area_euclidean_distance(a, b, return_nan: bool = False) -> float:
    nan_return_value = math.nan if return_nan else 0.0
    if len(a) > 1 and len(b) > 1:
        return centroid_euclidean_distance(a, b, return_nan)
    distance = statistics.fmean(
        [shortest_distance(a, [b_point]) for b_point in b]
        + [shortest_distance(b, [a_point]) for a_point in a]
    )
    return distance if not math.isnan(distance) else nan_return_value


def size_euclidean_distance(a, b, return_nan: bool = False) -> float:
    return abs(len(a) - len(b))


def centroid_difference(a, b, return_nan: bool = False) -> float:
    if isinstance(a[0][0], str):
        return boolean_distance(a, b, return_nan=return_nan)
    nan_return_value = math.nan if return_nan else 0.0
    difference = average_vector(a)[0] - average_vector(b)[0]
    return difference if not math.isnan(difference) else nan_return_value


def boolean_distance(a, b, return_nan: bool = False) -> float:
    # TODO: this is not fully general
    if isinstance(a[0][0], str):
        if a[0][0] == b[0][0]:
            return 0.0
        return math.inf
    if (len(a) == 0 or len(b) == 0) and a != b:
        return math.inf
    if all([math.isnan(coord) for a_coords in a for coord in a_coords]):
        return 0.0
    if all([math.isnan(coord) for b_coords in b for coord in b_coords]):
        return 0.0
    for a_coords in a:
        if not a_coords in b:
            return math.inf
    for b_coords in b:
        if not b_coords in a:
            return math.inf
    return 0.0


def average_vector(vectors: List[List[Union[float, int]]]):
    return [
        statistics.fmean([vectors[j][i] for j in range(len(vectors))])
        for i in range(len(vectors[0]))
    ]


def add_vectors(a: list, b: list) -> list:
    """adds the corresponding numbers in two lists of lists"""
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def first_key_of_dict(dictionary: dict):
    try:
        return min(int(k) for k in dictionary.keys())
    except ValueError:
        return None


def last_value_of_dict(dictionary: dict):
    try:
        return dictionary[str(max(int(k) for k in dictionary.keys()))]
    except ValueError:
        return None


def hasinstance(items: Iterable, t: type) -> bool:
    for item in items:
        if isinstance(item, t):
            return True
    return False


def areinstances(items: Iterable, t: type) -> bool:
    for item in items:
        if not isinstance(item, t):
            return False
    return True


def project_item_into_space(item: "Structure", space: "Space"):
    from homer.location import Location

    item.locations.append(
        Location(getattr(item, space.parent_concept.relevant_value), space)
    )
    space.add(item)


def equivalent_space(structure, space):
    for location in structure.locations:
        if location is None:
            continue
        if location.space.parent_concept == space.parent_concept:
            return location.space
    raise Exception(
        f"{structure.structure_id} does not exist "
        + f"in any space equivalent to {space.structure_id}"
    )


def arrange_text_fragments(fragments) -> dict:
    """Takes 2-3 text fragments and works out which is root, left branch, and right branch"""
    for potential_root in fragments:
        if not hasattr(potential_root, "left_branch"):
            continue
        potential_arrangement = {"root": potential_root}
        potential_members = [f for f in fragments if f != potential_root]
        if potential_root.left_branch in potential_members:
            potential_arrangement["left"] = potential_root.left_branch
        if potential_root.right_branch in potential_members:
            potential_arrangement["right"] = potential_root.right_branch
        if len(potential_arrangement) == len(fragments):
            if "left" not in potential_arrangement:
                potential_arrangement["left"] = None
            if "right" not in potential_arrangement:
                potential_arrangement["right"] = None
            return potential_arrangement
    if len(fragments) == 2:
        if (
            fragments[0].location.coordinates[-1][0] + 1
            == fragments[1].location.coordinates[0][0]
        ):
            return {"root": None, "left": fragments[0], "right": fragments[1]}
        if (
            fragments[1].location.coordinates[-1][0] + 1
            == fragments[0].location.coordinates[0][0]
        ):
            return {"root": None, "left": fragments[1], "right": fragments[0]}
    raise Exception("No acceptable arrangement")
