"""Unit tests for the intake form parser."""

import pytest

from ctk_functions.microservices import redcap
from ctk_functions.routers.intake.intake_processing import parser


def test_guardian_parser(
    test_redcap_data: redcap.RedCapData,
) -> None:
    """Tests the Guardian intake form parser."""
    guardian = parser.Guardian(test_redcap_data)

    assert guardian.first_name == test_redcap_data.guardian_first_name
    assert guardian.last_name == test_redcap_data.guardian_last_name
    assert guardian.title_name == f"Ms./Mrs. {guardian.last_name}"
    assert guardian.relationship == "biological mother"


def test_guardian_parser_other_relationship(
    test_redcap_data: redcap.RedCapData,
) -> None:
    """Tests the Guardian intake form parser with an 'other' relationship."""
    test_redcap_data = test_redcap_data.model_copy(
        update={
            "guardian_relationship___1": False,
            "guardian_relationship___12": True,
            "other_relation": "xkcd",
        },
    )

    guardian = parser.Guardian(test_redcap_data)

    assert guardian.relationship == test_redcap_data.other_relation


def test_guardian_parser_title(
    test_redcap_data: redcap.RedCapData,
) -> None:
    """Tests default title parsing."""
    test_redcap_data = test_redcap_data.model_copy(
        update={
            "title": redcap.GuardianTitle.Mr,
        },
    )

    guardian = parser.Guardian(test_redcap_data)

    assert guardian.title == "Mr."


def test_guardian_parser_title_other(
    test_redcap_data: redcap.RedCapData,
) -> None:
    """Tests other title parsing.."""
    test_redcap_data = test_redcap_data.model_copy(
        update={
            "title": redcap.GuardianTitle.Other,
            "title_other": "Jedi",
        },
    )

    guardian = parser.Guardian(test_redcap_data)

    assert guardian.title == "Jedi"


def test_household_parser(
    test_redcap_data: redcap.RedCapData,
) -> None:
    """Tests the Household intake form parser."""
    expected_marital_status = test_redcap_data.guardian_maritalstatus.name
    n_household_members = test_redcap_data.residing_number
    max_languages = 25
    n_languages = sum(
        [
            getattr(test_redcap_data, f"language___{index}")
            for index in range(1, max_languages + 1)
        ],
    )

    household = parser.Household(test_redcap_data)

    assert household.city == test_redcap_data.city.replace("_", " ")
    assert household.state == test_redcap_data.state.name.replace("_", " ")
    assert household.guardian_marital_status == expected_marital_status
    assert len(household.members) == n_household_members
    assert len(household.languages) == n_languages


def test_language_parser(
    test_redcap_data: redcap.RedCapData,
) -> None:
    """Tests the Language intake form parser."""
    expected_fluency = test_redcap_data.child_language1_fluency
    if not expected_fluency:
        msg = "Fluency is required. Something is wrong in the test data"
        raise ValueError(msg)

    language = parser.Language(test_redcap_data, 1)

    assert language.name == test_redcap_data.child_language1
    assert language.spoken_whole_life == test_redcap_data.child_language1_spoken
    assert language.spoken_since_age == test_redcap_data.child_language1_age
    assert language.setting == test_redcap_data.child_language1_setting
    assert language.fluency == expected_fluency.name


@pytest.mark.parametrize(
    ("test_input", "expected"),
    [
        ("ALL CAPS-", "All Caps-"),
        ("Not all caps", "Not all caps"),
    ],
)
def test_all_caps_to_title(test_input: str, expected: str) -> None:
    """Tests the conversion of all caps to title case."""
    actual = parser.all_caps_to_title(test_input)
    assert actual == expected


@pytest.mark.parametrize(
    ("test_input", "expected"),
    [
        ("PS40", "P.S. 40"),
        ("PS 40", "P.S. 40"),
        ("P.S. 40", "P.S. 40"),
        ("ELEMENTARY SCHOOL", "Elementary School"),
    ],
)
def test_process_school_name(test_input: str, expected: str) -> None:
    """Tests the processing of school name."""
    actual = parser.process_school_name(test_input)
    assert actual == expected
