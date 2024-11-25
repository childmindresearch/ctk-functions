"""Tests for the textual output of intake transformers."""

import pytest

from ctk_functions.functions.intake import transformers
from ctk_functions.microservices import redcap


@pytest.mark.parametrize(
    ("iep", "expected"),
    [
        (
            redcap.IndividualizedEducationProgram.yes,
            (
                "had an Individualized Education Program (IEP) with an educational "
                'classification of "Autism"'
            ),
        ),
        (
            redcap.IndividualizedEducationProgram.no,
            "did not have an Individualized Education Program (IEP)",
        ),
    ],
)
def test_individualized_education_program_transformer(
    iep: redcap.IndividualizedEducationProgram,
    expected: str,
) -> None:
    """Test that the IEP transformer returns the expected strings."""
    transformer = transformers.IndividualizedEducationProgram(iep, other="Autism")

    assert str(transformer) == expected


@pytest.mark.parametrize(
    ("value", "expected", "other"),
    [
        (
            [redcap.BirthComplications.none_of_the_above],
            "no birth complications",
            None,
        ),
        (
            [redcap.BirthComplications.spotting_or_vaginal_bleeding],
            "the following birth complication: spotting or vaginal bleeding",
            None,
        ),
        (
            [
                redcap.BirthComplications.emotional_problems,
                redcap.BirthComplications.diabetes,
            ],
            "the following birth complications: emotional problems and diabetes",
            None,
        ),
        (
            [redcap.BirthComplications.other_illnesses],
            "the following birth complication: tester",
            "tester",
        ),
    ],
)
def test_birth_complications_transformer(
    value: list[redcap.BirthComplications],
    expected: str,
    other: str | None,
) -> None:
    """Test that the BirthComplications transformer returns the expected strings."""
    transformer = transformers.BirthComplications(value, other)

    assert str(transformer) == expected


@pytest.mark.parametrize(
    ("value", "expected", "other"),
    [
        (
            redcap.BirthDelivery.unknown,
            "an unknown type of delivery",
            None,
        ),
        (
            redcap.BirthDelivery.vaginal,
            "a vaginal delivery",
            None,
        ),
        (
            redcap.BirthDelivery.cesarean,
            'a cesarean section due to "unspecified"',
            None,
        ),
        (
            redcap.BirthDelivery.cesarean,
            'a cesarean section due to "test reason"',
            "test reason",
        ),
    ],
)
def test_birth_delivery_transformer(
    value: redcap.BirthDelivery,
    expected: str,
    other: str | None,
) -> None:
    """Test that the BirthDelivery transformer returns the expected strings."""
    transformer = transformers.BirthDelivery(value, other)

    assert str(transformer) == expected


@pytest.mark.parametrize(
    ("value", "expected", "other"),
    [
        (
            redcap.DeliveryLocation.other,
            "an unspecified location",
            None,
        ),
        (
            redcap.DeliveryLocation.other,
            "test location",
            "test location",
        ),
        (
            redcap.DeliveryLocation.hospital,
            "a hospital",
            None,
        ),
        (
            redcap.DeliveryLocation.home,
            "home",
            None,
        ),
        (
            redcap.DeliveryLocation.hospital,
            "a hospital",
            "should not appear",
        ),
    ],
)
def test_delivery_location_transformer(
    value: redcap.DeliveryLocation,
    other: str | None,
    expected: str,
) -> None:
    """Test that the DeliveryLocation transformer returns the expected strings."""
    transformer = transformers.DeliveryLocation(value, other)

    assert str(transformer) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (
            redcap.Adaptability.difficult,
            "a slow to warm up temperament",
        ),
        (
            redcap.Adaptability.easy,
            "an adaptable temperament",
        ),
    ],
)
def test_adaptability_transformer(
    value: redcap.Adaptability,
    expected: str,
) -> None:
    """Test that the Adaptability transformer returns the expected strings."""
    transformer = transformers.Adaptability(value)

    assert str(transformer) == expected


@pytest.mark.parametrize(
    ("base", "expected"),
    [
        (3, "talked at 3 years"),
        (
            12,
            "talked at 12 months",
        ),
        (
            "not yet",
            "has not talked yet",
        ),
        (
            "normal",
            "talked at a normal age",
        ),
        (
            "early",
            "talked at an early age",
        ),
        (
            "2022-01-01",
            "talked at 2022-01-01",
        ),
    ],
)
def test_development_skill_transformer(
    base: str | int,
    expected: str,
) -> None:
    """Test that the DevelopmentSkill transformer returns the expected strings."""
    other = "talked"
    transformer = transformers.DevelopmentSkill(base, other)

    assert str(transformer) == expected


@pytest.mark.parametrize(
    ("base", "expected", "short"),
    [
        ([], "with no prior history of psychiatric diagnoses", False),
        (
            [
                redcap.PastDiagnosis(
                    diagnosis="Anxiety",
                    age_at_diagnosis="8",
                    clinician="Dr. Smith",
                ),
                redcap.PastDiagnosis(
                    diagnosis="Depression",
                    age_at_diagnosis="9",
                    clinician="Dr. Johnson",
                ),
            ],
            (
                "was diagnosed with the following psychiatric diagnoses: Anxiety "
                "at 8 by Dr. Smith and Depression at 9 by Dr. Johnson"
            ),
            False,
        ),
        (
            [
                redcap.PastDiagnosis(
                    diagnosis="Anxiety",
                    age_at_diagnosis="2022-01-01",
                    clinician="Dr. Smith",
                ),
                redcap.PastDiagnosis(
                    diagnosis="Depression",
                    age_at_diagnosis="2022-02-01",
                    clinician="Dr. Johnson",
                ),
            ],
            ("with a prior history of Anxiety and Depression"),
            True,
        ),
    ],
)
def test_past_diagnoses_transformer(
    base: list[redcap.PastDiagnosis],
    expected: str,
    *,
    short: bool,
) -> None:
    """Test that the PastDiagnoses transformer returns the expected strings."""
    transformer = transformers.PastDiagnoses(base)

    actual = transformer.transform(short=short)

    assert actual == expected


@pytest.mark.parametrize(
    ("base", "expected", "other"),
    [
        (
            redcap.HouseholdRelationship.other_relative,
            "unspecified relationship",
            None,
        ),
        (
            redcap.HouseholdRelationship.other_relative,
            "test relationship",
            "test relationship",
        ),
        (
            redcap.HouseholdRelationship.brother,
            "brother",
            None,
        ),
    ],
)
def test_household_relationship_transformer(
    base: redcap.HouseholdRelationship,
    expected: str,
    other: str | None,
) -> None:
    """Test that the HouseholdRelationship transformer returns the expected strings."""
    transformer = transformers.HouseholdRelationship(base, other)

    assert str(transformer) == expected


@pytest.mark.parametrize(
    ("duration", "expected"),
    [
        ("", "unspecified"),
        ("42", "42 weeks"),
        ("42.5", "42.5 weeks"),
        ("40 weeks", "40 weeks"),
        ("9 months", '"9 months"'),
        ("non$en$e", '"non$en$e"'),
    ],
)
def test_duration_of_pregnancy_transformer(duration: str, expected: str) -> None:
    """Test that the DurationOfPregnancy transformer returns the expected strings."""
    transformer = transformers.DurationOfPregnancy(duration)

    assert str(transformer) == expected


@pytest.mark.parametrize(
    ("handedness", "expected"),
    [
        (redcap.Handedness.left, "left-handed"),
        (redcap.Handedness.right, "right-handed"),
        (redcap.Handedness.unknown, ""),
    ],
)
def test_handedness_transformer(
    handedness: redcap.Handedness,
    expected: str,
) -> None:
    """Test that the Handedness transformer returns the expected strings."""
    transformer = transformers.Handedness(handedness)

    assert str(transformer) == expected


@pytest.mark.parametrize(
    ("base", "other", "expected"),
    [
        (
            redcap.ClassroomType.general_education,
            None,
            "general education",
        ),
        (
            redcap.ClassroomType._12COLON1COLON1,
            None,
            "12:1:1",
        ),
        (
            redcap.ClassroomType.other,
            "test classroom type",
            "test classroom type",
        ),
        (
            redcap.ClassroomType.other,
            None,
            "an unspecified classroom type",
        ),
    ],
)
def test_classroom_type_transformer(
    base: redcap.ClassroomType,
    other: str | None,
    expected: str,
) -> None:
    """Test that the ClassroomType transformer returns the expected strings."""
    transformer = transformers.ClassroomType(base, other)

    assert str(transformer) == expected


@pytest.mark.parametrize(
    ("base", "expected"),
    [
        (redcap.HearingDevice.no, "does not use a hearing device"),
        (
            redcap.HearingDevice.at_school_and_home,
            "uses a hearing device at school and at home",
        ),
        (redcap.HearingDevice.at_school, "uses a hearing device at school"),
        (redcap.HearingDevice.at_home, "uses a hearing device at home"),
    ],
)
def test_hearing_device_transformer(
    base: redcap.HearingDevice,
    expected: str,
) -> None:
    """Test that the HearingDevice transformer returns the expected strings."""
    transformer = transformers.HearingDevice(base)

    assert str(transformer) == expected


@pytest.mark.parametrize(
    ("base", "expected"),
    [
        (
            redcap.EducationGrades.As,
            "as {{PRONOUN_0}} receives mostly As",
        ),
        (
            redcap.EducationGrades.ONE,
            "as {{PRONOUN_0}} receives mostly 1s",
        ),
        (
            redcap.EducationGrades.not_graded,
            "though {{PRONOUN_0}} is not formally graded",
        ),
    ],
)
def test_education_grades_transformer(
    base: redcap.EducationGrades,
    expected: str,
) -> None:
    """Test that the EducationGrades transformer returns the expected strings."""
    transformer = transformers.EducationGrades(base)

    assert str(transformer) == expected
