import pytest
from unittest.mock import Mock

from linguoplotter.structure_collection import StructureCollection
from linguoplotter.structures.spaces import ContextualSpace


@pytest.mark.parametrize(
    "activation_1, activation_2, activation_3, expected_activation",
    [
        (1.0, 1.0, 1.0, 1.0),
        (0.5, 0.2, 0.0, 0.2),
        (1.0, 0.0, 0.0, 0.0),
        (1.0, 1.0, 0.0, 1.0),
    ],
)
def test_update_activation(
    activation_1, activation_2, activation_3, expected_activation
):
    structure_1 = Mock()
    structure_1.activation = activation_1
    structure_2 = Mock()
    structure_2.activation = activation_2
    structure_3 = Mock()
    structure_3.activation = activation_3
    contextual_space = ContextualSpace(
        Mock(),
        Mock(),
        "name",
        Mock(),
        StructureCollection(Mock(), [structure_1, structure_2, structure_3]),
        Mock(),
        Mock(),
        Mock(),
        Mock(),
    )
    contextual_space.update_activation()
    assert expected_activation == contextual_space.activation
