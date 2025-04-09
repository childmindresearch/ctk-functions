"""Tests the utility functions for the WISC tables."""

import fastapi
import pytest
from fastapi import status

from ctk_functions.routers.pyrite.tables import wisc_subtest


@pytest.mark.parametrize(
    ("scaled_score", "expected_qualifier"),
    [
        (0, "extremely low"),
        (1, "extremely low"),
        (2, "very low"),
        (3, "very low"),
        (4, "low"),
        (5, "low"),
        (6, "low average"),
        (7, "low average"),
        (8, "average"),
        (9, "average"),
        (10, "average"),
        (11, "average"),
        (12, "high average"),
        (13, "high average"),
        (14, "high"),
        (15, "high"),
        (16, "very high"),
        (17, "very high"),
        (18, "extremely high"),
        (19, "extremely high"),
        (100, "extremely high"),
    ],
)
def test_wisc_subtest_scaled_score_to_qualifier(
    scaled_score: int, expected_qualifier: str
) -> None:
    """Test that valid scores return the expected qualifiers."""
    result = wisc_subtest._wisc_subtest_scaled_score_to_qualifier(scaled_score)
    assert result == expected_qualifier


@pytest.mark.parametrize(
    ("scale_score", "expected_percentile"),
    [
        (1, 1),
        (2, 1),
        (3, 1),
        (4, 2),
        (5, 5),
        (6, 9),
        (7, 16),
        (8, 25),
        (9, 37),
        (10, 50),
        (11, 63),
        (12, 75),
        (13, 84),
        (14, 91),
        (15, 95),
        (16, 98),
        (17, 99),
        (18, 99),
        (19, 99),
        (20, 99),
    ],
)
def test_wisc_subtest_scaled_score_to_percentile_valid(
    scale_score: int, expected_percentile: int
) -> None:
    """Test that valid scores return the expected percentiles."""
    result = wisc_subtest._wisc_subtest_scaled_score_to_percentile(scale_score)
    assert result == expected_percentile


def test_wisc_subtest_scaled_score_to_percentile_invalid() -> None:
    """Test that an invalid score raises an HTTPException."""
    with pytest.raises(fastapi.HTTPException) as exc_info:
        wisc_subtest._wisc_subtest_scaled_score_to_percentile(0)

    assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert exc_info.value.detail == "Unknown WISC subtest score."
