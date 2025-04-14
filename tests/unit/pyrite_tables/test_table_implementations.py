"""Tests for the table implementations."""

from typing import Any

import pytest

from ctk_functions.routers.pyrite.tables import (
    academic_achievement,
    base,
    cbcl_ysr,
    celf5,
    conners3,
    ctopp2,
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
            grooved_pegboard._GroovedPegboardDataSource,
            ["Hand", "Z-Score", "Percentile", "Range"],
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
            ["Index", "Subtest", "Scaled Score", "Percentile", "Range"],
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
