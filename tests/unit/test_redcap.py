"""Tests for REDCap intake data retrieval."""

import polars as pl
import pytest
import pytest_mock

from ctk_functions.intake import redcap


def test_redcap_error(mocker: pytest_mock.MockFixture) -> None:
    """Tests the REDcap error handling."""
    mocker.patch("requests.post", side_effect=Exception("Test exception"))

    with pytest.raises(Exception):
        redcap.get_intake_data("test_survey_id")


def test_redcap_success(mocker: pytest_mock.MockFixture) -> None:
    """Tests the REDcap success handling."""
    response = mocker.MagicMock()
    response.text = "data\ntest_data\n"
    mocker.patch("requests.post", return_value=response)
    expected = pl.DataFrame({"data": "test_data"})

    actual = redcap.get_intake_data("test_survey_id")

    assert actual.equals(expected)
