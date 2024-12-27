"""Configuration for pytest."""

import pytest

from ctk_functions.microservices import redcap


@pytest.fixture(scope="session")
def test_redcap_data() -> redcap.RedCapData:
    """Returns a dictionary of test data."""
    return redcap.get_intake_data("mock")
