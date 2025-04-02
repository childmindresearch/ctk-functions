"""Tests for Pyrite utilities."""

from collections.abc import Callable

import pytest

from ctk_functions.routers.pyrite.tables import utils


@pytest.mark.parametrize(
    ("score", "expected_qualifier"),
    [
        (59, "extremely low"),
        (65, "very low"),
        (75, "low"),
        (85, "low average"),
        (100, "average"),
        (115, "high average"),
        (125, "high"),
        (135, "very high"),
        (145, "extremely high"),
    ],
)
def test_score_to_qualifier(score: float, expected_qualifier: str) -> None:
    """Test converting standard scores to qualifiers."""
    result = utils.standard_score_to_qualifier(score)
    assert result == expected_qualifier


@pytest.mark.parametrize(
    ("score", "mean", "std", "expected_range"),
    [
        (100, 100, 15, lambda x: round(x) == 50),  # noqa: PLR2004
        # 1-SD is approximately 15.9 percentile
        (85, 100, 15, lambda x: 15.8 < x < 16),  # noqa: PLR2004
    ],
)
def test_normal_score_to_percentile(
    score: float,
    mean: float,
    std: float,
    expected_range: Callable[[float], bool],
) -> None:
    """Test normal score to percentile conversion."""
    result = utils.normal_score_to_percentile(score, mean, std)
    assert expected_range(result)
