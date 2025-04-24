"""Tests for the table implementations."""

from typing import TYPE_CHECKING, Any

import pytest

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import (
    academic_achievement,
    base,
    celf5,
    ctopp2,
    grooved_pegboard,
    language,
    mfq,
    scared,
    scq,
    swan,
    wisc_composite,
    wisc_subtest,
)
from ctk_functions.routers.pyrite.tables.generic import tscore

if TYPE_CHECKING:
    from ctk_functions.routers.pyrite import types


@pytest.mark.parametrize(
    ("data_source", "headers", "labels"),
    [
        (
            academic_achievement._AcademicAchievementDataSource,
            ("Domain", "Subtest", "Standard Score", "Percentile", "Range"),
            academic_achievement.ACADEMIC_ROW_LABELS,
        ),
        (
            celf5._Celf5DataSource,
            ("Test", "Total Score", "Age Based Cutoff", "Range"),
            ["Has one row, no row labels defined."],
        ),
        (
            ctopp2._Ctopp2DataSource,
            ("CTOPP - 2 Rapid Naming", "Number of Errors"),
            ctopp2.CTOPP2_ROW_LABELS,
        ),
        (
            grooved_pegboard._GroovedPegboardDataSource,
            ("Hand", "Z-Score", "Percentile", "Range"),
            grooved_pegboard.PEGBOARD_ROW_LABELS,
        ),
        (
            language._LanguageDataSource,
            ("Test", "Subtest", "Standard Score", "Percentile", "Range"),
            language.LANGUAGE_ROW_LABELS,
        ),
        (
            mfq._MfqDataSource,
            ("Subscales", "Parent", "Child", "Clinical Relevance"),
            mfq.MFQ_ROW_LABELS,
        ),
        (
            scared._ScaredDataSource,
            ("Subscales", "Parent", "Child", "Clinical Relevance"),
            scared.SCARED_ROW_LABELS,
        ),
        (
            scq._ScqDataSource,
            ("Scale", "Score", "Clinical Relevance"),
            ["Has one row, no row labels defined."],
        ),
        (
            swan._SwanDataSource,
            ("Subscale", "Score", "Clinical Relevance"),
            swan.SWAN_ROW_LABELS,
        ),
        (
            wisc_composite._WiscCompositeDataSource,
            ("Composite", "Standard Score", "Percentile", "Range"),
            wisc_composite.WISC_COMPOSITE_ROW_LABELS,
        ),
        (
            wisc_subtest._WiscSubtestDataSource,
            ("Index", "Subtest", "Scaled Score", "Percentile", "Range"),
            wisc_subtest.WISC_SUBTEST_ROW_LABELS,
        ),
    ],
)
def test_data_sources(
    mock_sql_calls: None,
    data_source: type[base.DataProducer],
    headers: tuple[str, ...],
    labels: Any,  # noqa: ANN401
) -> None:
    """Tests whether the data sources all output the correct format."""
    actual = data_source().fetch("")

    assert isinstance(actual, tuple)
    assert headers == actual[0]
    assert len(actual) == len(labels) + 1


def test_t_score_data_producer(mock_sql_calls: None) -> None:
    """Tests the t-score data producer factory."""
    model = models.Cbcl
    test_ids: tuple[types.TestId] = ("cbcl",)
    labels = [
        tscore.TScoreRowLabel(subscale="CBCL", score_column="CBCL_AD_T", relevance=[])
    ]

    producer = tscore.create_data_producer(test_ids, model, labels)
    data = producer.fetch("")

    assert producer.test_ids("") == test_ids
    assert len(data) == len(labels) + 1
