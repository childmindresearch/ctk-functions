"""Tests for REDCap intake data retrieval."""

import pytest
import pytest_mock

from ctk_functions import exceptions
from ctk_functions.microservices import redcap


def test_redcap_error(mocker: pytest_mock.MockFixture) -> None:
    """Tests the REDcap error handling."""
    mocker.patch(
        "redcap.Project",
        return_value=mocker.MagicMock(
            export_records=mocker.MagicMock(
                return_value="record_id,redcap_survey_identifier,data\n",
            ),
        ),
    )

    with pytest.raises(exceptions.RedcapError):
        redcap.get_intake_data("00000")
