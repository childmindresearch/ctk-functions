"""Tests for REDCap intake data retrieval."""

import pytest
import pytest_mock

from ctk_functions.microservices import redcap


def test_redcap_error(mocker: pytest_mock.MockFixture) -> None:
    """Tests the REDcap error handling."""
    mocker.patch("requests.post", side_effect=Exception("Test exception"))

    with pytest.raises(Exception):
        redcap.get_intake_data("00000")


def test_redcap_success(mocker: pytest_mock.MockFixture) -> None:
    """Tests the REDcap success handling."""
    mocker.patch(
        "redcap.Project",
        return_value=mocker.MagicMock(
            export_records=mocker.MagicMock(
                return_value="record_id,redcap_survey_identifier,data\n0,00000,test_data\n"
            )
        ),
    )
    expected = {
        "record_id": "0",
        "redcap_survey_identifier": "00000",
        "data": "test_data",
    }

    actual = redcap.get_intake_data("00000")

    assert actual == expected
