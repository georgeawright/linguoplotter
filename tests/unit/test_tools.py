import math
import pytest
from unittest.mock import Mock

from linguoplotter.tools import *


@pytest.mark.parametrize(
    "a, b, result",
    [
        ([[24]], [[24]], 0.0),
        ([[24], [24]], [[24]], 0.0),
        ([[math.nan]], [[24]], 0.0),
    ],
)
def test_boolean_distance(a, b, result):
    assert boolean_distance(a, b) == result


@pytest.mark.parametrize(
    "vectors, expected_average",
    [([[1, 1, 1], [2, 2, 2], [3, 3, 3]], [2, 2, 2]), ([[1], [2]], [1.5])],
)
def test_average_vector(vectors, expected_average):
    assert average_vector(vectors) == expected_average


@pytest.mark.parametrize(
    "a, b, result",
    [
        ([[10]], [[10]], [[20]]),
        ([[0], [1]], [[2], [3]], [[2], [4]]),
        ([[0, 1]], [[2, 2]], [[2, 3]]),
    ],
)
def test_add_vectors(a, b, result):
    assert add_vectors(a, b) == result


def test_has_instance():
    list_with_int = [1, "a", "b"]
    assert hasinstance(list_with_int, int)
    list_without_int = ["1", "a", "b"]
    assert not hasinstance(list_without_int, int)


def test_are_instances():
    list_of_ints = [1, 2, 3]
    assert areinstances(list_of_ints, int)
    assert not areinstances(list_of_ints, str)


def test_arrange_text_fragments_arranges_three():
    root = Mock()
    left = Mock()
    right = Mock()
    root.left_branch = left
    root.right_branch = right
    result = arrange_text_fragments([root, left, right])
    assert result["root"] == root
    assert result["left"] == left
    assert result["right"] == right


def test_arrange_text_fragments_arranges_root_and_branch():
    root = Mock()
    branch = Mock()
    root.left_branch = branch
    result = arrange_text_fragments([root, branch])
    assert result["root"] == root
    assert result["left"] == branch


def test_arrange_text_fragments_arranges_branches():
    left = Mock()
    left.location.coordinates = [[0]]
    right = Mock()
    right.location.coordinates = [[1]]
    result = arrange_text_fragments([left, right])
    assert result["left"] == left
    assert result["right"] == right
