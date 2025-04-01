"""Tests for the table implementations."""

from typing import Any

import fastapi
import pytest
from fastapi import status

from ctk_functions.routers.pyrite.tables import (
    academic_achievement,
    base,
    cbcl_ysr,
    celf5,
    conners3,
    ctopp2,
    gars,
    grooved_pegboard,
    language,
    mfq,
    scared,
    scq,
    srs,
    swan,
    wisc_composite,
    wisc_subtest,
)


@pytest.mark.parametrize(
    ("data_source", "headers", "labels"),
    [
        (
            academic_achievement._AcademicAchievementDataSource,
            ["Domain", "Subtest", "Standard Score", "Percentile", "Range"],
            academic_achievement.ACADEMIC_ROW_LABELS,
        ),
        (
            cbcl_ysr._CbclDataSource,
            ["Subscale", "T-Score", "Clinical Relevance"],
            cbcl_ysr.CBCL_YSR_ROW_LABELS["CBCL"],
        ),
        (
            celf5._Celf5DataSource,
            ["Test", "Total Score", "Age Based Cutoff", "Range"],
            ["Has one row, no row labels defined."],
        ),
        (
            conners3._Conners3DataSource,
            ["Subscale", "T-Score", "Clinical Relevance"],
            conners3.CONNERS3_ROW_LABELS,
        ),
        (
            ctopp2._Ctopp2DataSource,
            ["CTOPP - 2 Rapid Naming", "Number of Errors"],
            ctopp2.CTOPP2_ROW_LABELS,
        ),
        (
            gars._GarsDataSource,
            ["Autism Index Score", "Percentile Rank", "Autism Index Interpretation"],
            ["Has one row, no row labels defined."],
        ),
        (
            grooved_pegboard._GroovedPegboardDataSource,
            ["Grooved Pegboard", "Z-Score", "Percentile", "Range"],
            grooved_pegboard.PEGBOARD_ROW_LABELS,
        ),
        (
            language._LanguageDataSource,
            ["Test", "Subtest", "Standard Score", "Percentile", "Range"],
            language.LANGUAGE_ROW_LABELS,
        ),
        (
            mfq._MfqDataSource,
            ["Subscales", "Parent", "Child", "Clinical Relevance"],
            mfq.MFQ_ROW_LABELS,
        ),
        (
            scared._ScaredDataSource,
            ["Subscales", "Parent", "Child", "Clinical Relevance"],
            scared.SCARED_ROW_LABELS,
        ),
        (
            scq._ScqDataSource,
            ["Scale", "Score", "Clinical Relevance"],
            ["Has one row, no row labels defined."],
        ),
        (
            swan._SwanDataSource,
            ["Subscale", "Score", "Clinical Relevance"],
            swan.SWAN_ROW_LABELS,
        ),
        (
            srs._SrsDataSource,
            ["Subscale", "T-Score", "Clinical Relevance"],
            srs.SRS_ROW_LABELS,
        ),
        (
            wisc_composite._WiscCompositeDataSource,
            ["Composite", "Standard Score", "Percentile", "Range"],
            wisc_composite.WISC_COMPOSITE_ROW_LABELS,
        ),
        (
            wisc_subtest._WiscSubtestDataSource,
            ["Scale", "Subtest", "Scaled Score", "Percentile", "Range"],
            wisc_subtest.WISC_SUBTEST_ROW_LABELS,
        ),
        (
            cbcl_ysr._YsrDataSource,
            ["Subscale", "T-Score", "Clinical Relevance"],
            cbcl_ysr.CBCL_YSR_ROW_LABELS["YSR"],
        ),
    ],
)
def test_data_sources(
    mock_sql_calls: None,
    data_source: type[base.DataProducer],
    headers: list[str],
    labels: Any,  # noqa: ANN401
) -> None:
    """Tests whether the data sources all output the correct format."""
    actual = data_source().fetch("")

    assert isinstance(actual, base.WordTableMarkup)
    assert headers == [row.content for row in actual.rows[0]]
    assert len(actual.rows) == len(labels) + 1


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
