"""Tests for the CBCL/YSR helper functions."""

import cmi_docx
import pytest

from ctk_functions.routers.pyrite.tables import cbcl_ysr


def test_clinical_relevance_init_with_valid_parameters() -> None:
    """Test initialization with valid parameters."""
    low = 10
    high = 20
    label = "Normal"

    actual = cbcl_ysr.ClinicalRelevance(
        low=low,
        high=high,
        label=label,
        style=cmi_docx.TableStyle(),
    )

    assert actual.low == low
    assert actual.high == high
    assert actual.label == "Normal"


def test_clinical_relevance_init_with_missing_low_high() -> None:
    """Test initialization without low/high parameters."""
    with pytest.raises(
        ValueError,
        match="At least one of low or high must not be None.",
    ):
        cbcl_ysr.ClinicalRelevance(
            low=None,
            high=None,
            label="",
            style=cmi_docx.TableStyle(),
        )


def test_clinical_relevance_init_with_invalid_low_high() -> None:
    """Test initialization without low/high parameters."""
    with pytest.raises(ValueError, match="Low must be lower than high."):
        cbcl_ysr.ClinicalRelevance(low=1, high=0, label="", style=cmi_docx.TableStyle())


@pytest.mark.parametrize(
    ("low", "high", "expected"),
    [
        (10, 20, "10-20 = LABEL"),
        (10, None, ">10 = LABEL"),
        (None, 10, "<10 = LABEL"),
    ],
)
def test_clinical_relevance_strings(low: int, high: int, expected: str) -> None:
    """Tests the string representation of ClinicalRelevance."""
    cr = cbcl_ysr.ClinicalRelevance(
        low=low,
        high=high,
        label="LABEL",
        style=cmi_docx.TableStyle(),
    )

    assert str(cr) == expected


@pytest.mark.parametrize(
    ("low", "high", "value", "expected"),
    [
        (1, 10, 5, True),
        (1, 10, 11, False),
        (1, 10, -1, False),
        (None, 10, 9, True),
        (None, 10, 10, True),
        (None, 10, 11, False),
        (1, None, 1, False),
        (1, None, -1, False),
        (1, None, 2, True),
    ],
)
def test_clinical_relevance_in_range(
    low: int | None,
    high: int | None,
    value: int,
    expected: bool,  # noqa: FBT001
) -> None:
    """Tests that the in_range function evaluates correctly."""
    cr = cbcl_ysr.ClinicalRelevance(
        low=low,
        high=high,
        label="",
        style=cmi_docx.TableStyle(),
    )

    assert cr.in_range(value) == expected
