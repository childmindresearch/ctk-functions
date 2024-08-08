"""Tests for the textual output of intake transformers."""

import pytest

from ctk_functions.functions.intake import descriptors, transformers


@pytest.mark.parametrize(
    ("iep", "expected"),
    [
        (
            descriptors.IndividualizedEducationProgram.yes,
            "had an Individualized Education Program (IEP)",
        ),
        (
            descriptors.IndividualizedEducationProgram.no,
            "did not have an Individualized Education Program (IEP)",
        ),
    ],
)
def test_individualized_education_program_transformer(
    iep: descriptors.IndividualizedEducationProgram,
    expected: str,
) -> None:
    """Test that the IEP transformer returns the expected strings."""
    transformer = transformers.IndividualizedEducationProgram(iep)

    assert str(transformer) == expected


@pytest.mark.parametrize(
    ("value", "expected", "other"),
    [
        (
            [descriptors.BirthComplications.none_of_the_above],
            "no birth complications",
            None,
        ),
        (
            [descriptors.BirthComplications.spotting_or_vaginal_bleeding],
            "the following birth complication: spotting or vaginal bleeding",
            None,
        ),
        (
            [
                descriptors.BirthComplications.emotional_problems,
                descriptors.BirthComplications.diabetes,
            ],
            "the following birth complications: emotional problems and diabetes",
            None,
        ),
        (
            [descriptors.BirthComplications.other_illnesses],
            "the following birth complication: tester",
            "tester",
        ),
    ],
)
def test_birth_complications_transformer(
    value: list[int],
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
            descriptors.BirthDelivery.unknown,
            "an unknown type of delivery",
            None,
        ),
        (
            descriptors.BirthDelivery.vaginal,
            "a vaginal delivery",
            None,
        ),
        (
            descriptors.BirthDelivery.cesarean,
            'a cesarean section due to "unspecified"',
            None,
        ),
        (
            descriptors.BirthDelivery.cesarean,
            'a cesarean section due to "test reason"',
            "test reason",
        ),
    ],
)
def test_birth_delivery_transformer(
    value: descriptors.BirthDelivery,
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
            descriptors.DeliveryLocation.other,
            "an unspecified location",
            None,
        ),
        (
            descriptors.DeliveryLocation.other,
            "test location",
            "test location",
        ),
        (
            descriptors.DeliveryLocation.hospital,
            "a hospital",
            None,
        ),
        (
            descriptors.DeliveryLocation.home,
            "home",
            None,
        ),
        (
            descriptors.DeliveryLocation.hospital,
            "a hospital",
            "should not appear",
        ),
    ],
)
def test_delivery_location_transformer(
    value: descriptors.DeliveryLocation,
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
            descriptors.Adaptability.difficult,
            "a slow to warm up temperament",
        ),
        (
            descriptors.Adaptability.easy,
            "an adaptable temperament",
        ),
    ],
)
def test_adaptability_transformer(
    value: descriptors.Adaptability,
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
                descriptors.PastDiagnosis(
                    diagnosis="Anxiety",
                    age_at_diagnosis="8",
                    clinician="Dr. Smith",
                ),
                descriptors.PastDiagnosis(
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
                descriptors.PastDiagnosis(
                    diagnosis="Anxiety",
                    age_at_diagnosis="2022-01-01",
                    clinician="Dr. Smith",
                ),
                descriptors.PastDiagnosis(
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
    base: list[descriptors.PastDiagnosis],
    expected: str,
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
            descriptors.HouseholdRelationship.other_relative,
            "unspecified relationship",
            None,
        ),
        (
            descriptors.HouseholdRelationship.other_relative,
            "test relationship",
            "test relationship",
        ),
        (
            descriptors.HouseholdRelationship.brother,
            "brother",
            None,
        ),
    ],
)
def test_household_relationship_transformer(
    base: descriptors.HouseholdRelationship,
    expected: str,
    other: str | None,
) -> None:
    """Test that the HouseholdRelationship transformer returns the expected strings."""
    transformer = transformers.HouseholdRelationship(base, other)

    assert str(transformer) == expected


@pytest.mark.parametrize(
    ("base", "expected"),
    [
        (
            descriptors.GuardianMaritalStatus.domestic_partnership,
            "The parents/guardians are in a domestic partnership",
        ),
        (
            descriptors.GuardianMaritalStatus.widowed,
            "The parent/guardian is widowed",
        ),
        (
            descriptors.GuardianMaritalStatus.never_married,
            "The parents/guardians were never married",
        ),
        (
            descriptors.GuardianMaritalStatus.married,
            "The parents/guardians are married",
        ),
        (
            descriptors.GuardianMaritalStatus.divorced,
            "The parents/guardians are divorced",
        ),
        (
            descriptors.GuardianMaritalStatus.separated,
            "The parents/guardians are separated",
        ),
    ],
)
def test_guardian_marital_status_transformer(
    base: descriptors.GuardianMaritalStatus,
    expected: str,
) -> None:
    """Test that the GuardianMaritalStatus transformer returns the expected strings."""
    transformer = transformers.GuardianMaritalStatus(base)

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
        (descriptors.Handedness.left, "left-handed"),
        (descriptors.Handedness.right, "right-handed"),
        (descriptors.Handedness.unknown, ""),
    ],
)
def test_handedness_transformer(
    handedness: descriptors.Handedness,
    expected: str,
) -> None:
    """Test that the Handedness transformer returns the expected strings."""
    transformer = transformers.Handedness(handedness)

    assert str(transformer) == expected


@pytest.mark.parametrize(
    ("base", "other", "expected"),
    [
        (
            descriptors.ClassroomType.general_education,
            None,
            "general education",
        ),
        (
            descriptors.ClassroomType._12COLON1COLON1,
            None,
            "12:1:1",
        ),
        (
            descriptors.ClassroomType.other,
            "test classroom type",
            "test classroom type",
        ),
        (
            descriptors.ClassroomType.other,
            None,
            "an unspecified classroom type",
        ),
    ],
)
def test_classroom_type_transformer(
    base: descriptors.ClassroomType,
    other: str | None,
    expected: str,
) -> None:
    """Test that the ClassroomType transformer returns the expected strings."""
    transformer = transformers.ClassroomType(base, other)

    assert str(transformer) == expected


@pytest.mark.parametrize(
    ("base", "expected"),
    (
        (descriptors.HearingDevice.no, "does not use a hearing device"),
        (
            descriptors.HearingDevice.at_school_and_home,
            "uses a hearing device at school and at home",
        ),
        (descriptors.HearingDevice.at_school, "uses a hearing device at school"),
        (descriptors.HearingDevice.at_home, "uses a hearing device at home"),
    ),
)
def test_hearing_device_transformer(
    base: descriptors.HearingDevice,
    expected: str,
) -> None:
    """Test that the HearingDevice transformer returns the expected strings."""
    transformer = transformers.HearingDevice(base)

    assert str(transformer) == expected


@pytest.mark.parametrize(
    ("base", "expected"),
    [
        (
            descriptors.EducationGrades.As,
            "As",
        ),
        (
            descriptors.EducationGrades.Bs,
            "Bs",
        ),
        (
            descriptors.EducationGrades.Cs,
            "Cs",
        ),
        (
            descriptors.EducationGrades.Ds,
            "Ds",
        ),
        (
            descriptors.EducationGrades.Fs,
            "Fs",
        ),
        (
            descriptors.EducationGrades.ONE,
            "1s",
        ),
        (
            descriptors.EducationGrades.TWO,
            "2s",
        ),
        (
            descriptors.EducationGrades.THREE,
            "3s",
        ),
        (
            descriptors.EducationGrades.FOUR,
            "4s",
        ),
        (
            descriptors.EducationGrades.not_graded,
            "not graded",
        ),
    ],
)
def test_education_grades_transformer(
    base: descriptors.EducationGrades,
    expected: str,
) -> None:
    """Test that the EducationGrades transformer returns the expected strings."""
    transformer = transformers.EducationGrades(base)

    assert str(transformer) == expected
