"""Configuration for pytest."""

import dataclasses
from typing import Any, Literal

import pytest
import pytest_mock
from fastapi import testclient

from ctk_functions import app
from ctk_functions.microservices import redcap
from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import (
    academic_achievement,
    cbcl_ysr,
    conners3,
    ctopp2,
    grooved_pegboard,
    language,
    mfq,
    scared,
    srs,
)


@pytest.fixture(scope="session")
def test_redcap_data() -> redcap.RedCapData:
    """Returns a dictionary of test data compliant with RedCAP."""
    return redcap.get_intake_data("mock")


@pytest.fixture(scope="session")
def client() -> testclient.TestClient:
    """Returns a test client for the FastAPI server."""
    return testclient.TestClient(app.app)


def _mock_from_column_names(column_names: list[str], default_value: Any) -> object:  # noqa: ANN401
    """Creates a mock data class from the column names."""
    attributes = [(column, Any) for column in column_names]
    obj = dataclasses.make_dataclass("obj", attributes)
    args = {attr[0]: default_value for attr in attributes}
    return obj(**args)


def _mock_fetch_participant_row(  # noqa: C901, PLR0912
    id_property: Literal["person_id", "EID", "mrn"],
    mrn: str,
    table: Any,  # noqa: ANN401
) -> object:
    """Redirects requests of fetch_participant_row to the correct mock."""
    default_value: str | int
    if table == models.Cbcl:
        columns = [label.score_column for label in cbcl_ysr.CBCL_YSR_ROW_LABELS["CBCL"]]
        default_value = 100
    elif table == models.Celf5:
        columns = ["CELF_Total", "CELF_CriterionScore", "CELF_ExceedCutoff"]
        default_value = 100
    elif table == models.Conners3:
        columns = [label.score_column for label in conners3.CONNERS3_ROW_LABELS]
        default_value = 100
    elif table == models.CmiHbnIdTrack:
        columns = ["first_name", "last_name", "GUID", "MRN", "person_id"]
        default_value = "abc"
    elif table == models.Gars:
        columns = ["GARS_AI", "GARS_AI_Perc"]
        default_value = 100
    elif table == models.GroovedPegboard:
        columns = [label.score_column for label in grooved_pegboard.PEGBOARD_ROW_LABELS]
        default_value = 100
    elif table == models.Scq:
        columns = ["SCQ_Total"]
        default_value = 100
    elif table == models.Srs:
        columns = [label.score_column for label in srs.SRS_ROW_LABELS]
        default_value = 100
    elif table == models.SummaryScores:
        columns = [
            label.score_column  # type: ignore[attr-defined]
            for label in [
                *academic_achievement.ACADEMIC_ROW_LABELS,
                *language.LANGUAGE_ROW_LABELS,
                *ctopp2.CTOPP2_ROW_LABELS,
            ]
            if label.score_column is not None  # type: ignore[attr-defined]
        ]
        default_value = 100
    elif table == models.Swan:
        columns = ["SWAN_IN", "SWAN_HY"]
        default_value = 100
    elif table == models.Wisc5:
        columns = [
            "WISC_VCI",
            "WISC_VSI",
            "WISC_FRI",
            "WISC_WMI",
            "WISC_PSI",
            "WISC_FSIQ",
            "WISC_Similarities_Scaled",
            "WISC_Vocab_Scaled",
            "WISC_BD_Scaled",
            "WISC_VP_Scaled",
            "WISC_MR_Scaled",
            "WISC_FW_Scaled",
            "WISC_DS_Scaled",
            "WISC_PS_Scaled",
            "WISC_Coding_Scaled",
            "WISC_SS_Scaled",
        ]
        default_value = 100
    elif table == models.Ysr:
        columns = [label.score_column for label in cbcl_ysr.CBCL_YSR_ROW_LABELS["YSR"]]
        default_value = 100
    else:
        msg = "Did not implemented this table's mock yet."
        raise NotImplementedError(msg)
    return _mock_from_column_names(columns, default_value)


def _mock_parent_child_sql_request(
    mrn: str, parent_table: type[models.Base], child_table: type[models.Base]
) -> tuple[object, object]:
    if parent_table == models.MfqParent:
        parent_columns = [label.parent_column for label in mfq.MFQ_ROW_LABELS]
        child_columns = [label.child_column for label in mfq.MFQ_ROW_LABELS]
    elif parent_table == models.ScaredParent:
        parent_columns = [label.parent_column for label in scared.SCARED_ROW_LABELS]
        child_columns = [label.child_column for label in scared.SCARED_ROW_LABELS]
    else:
        msg = "Did not implemented this table's mock yet."
        raise NotImplementedError(msg)
    return (
        _mock_from_column_names(parent_columns, 100),
        _mock_from_column_names(child_columns, 100),
    )


@pytest.fixture
def mock_sql_calls(mocker: pytest_mock.MockerFixture) -> None:
    """Mocks requests to the SQL database."""
    mocker.patch(
        "ctk_functions.routers.pyrite.tables.utils.fetch_participant_row",
        side_effect=_mock_fetch_participant_row,
    )
    mocker.patch(
        "ctk_functions.routers.pyrite.tables.generic.parent_child._parent_child_sql_request",
        side_effect=_mock_parent_child_sql_request,
    )
