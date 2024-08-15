"""Configuration for pytest."""

import pathlib

import pytest

from ctk_functions.microservices import redcap


@pytest.fixture(scope="session")
def test_redcap_data() -> redcap.RedCapData:
    """Returns a dictionary of test data."""
    data_file = pathlib.Path(__file__).parent / "data" / "test_redcap_data.csv"
    contents = data_file.read_text().strip()
    return redcap.RedCapData.from_csv(contents)
