import pytest
from unittest.mock import Mock

from homer.codelets.evaluators import GroupEvaluator


@pytest.mark.parametrize(
    "champion_size, challenger_size, "
    + "champion_connections, challenger_connections, expected",
    [(10, 5, 5, 3, 0.65), (5, 10, 3, 5, -0.65)],
)
def test_run_competition(
    champion_size,
    challenger_size,
    champion_connections,
    challenger_connections,
    expected,
):
    champion = Mock()
    champion.location = [0, 0, 0]
    champion.size = champion_size
    champion.total_connection_activations.side_effect = [champion_connections]
    challenger = Mock()
    challenger.size = challenger_size
    challenger.total_connection_activations.side_effect = [challenger_connections]
    evaluator = GroupEvaluator(
        Mock(), Mock(), Mock(), champion, challenger, Mock(), Mock()
    )
    assert expected == evaluator._run_competition()
