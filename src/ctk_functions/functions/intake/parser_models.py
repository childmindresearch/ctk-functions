"""Models for parsing the intake data.

Separate module is used as some of these need to be imported in both the parser and
the transformers.
"""

from typing import Literal

import pydantic


class InfantDifficulties(pydantic.BaseModel):
    """Difficulties during infancy."""

    colic: str | None
    eating_difficulties: str | None
    sleeping_difficulties: str | None
    did_not_enjoy_body_contact: str | None
    overly_sensitive_to_sound: str | None
    limp_or_stiff: str | None
    problems_with_social_relatedness: str | None

    def any(self) -> bool:
        """True if any of the properties are truthy.

        Returns:
            True if any of the properties are truthy, otherwise False.
        """
        return any(value for value in self.model_dump().values())


class PastSchool(pydantic.BaseModel):
    """The model for past schools."""

    name: str
    grades: str
    experience: str


class CurrentPsychiatricMedication(pydantic.BaseModel):
    """The model for current psychiatric medication."""

    name: str
    initial_dosage: str
    current_dosage: str
    date_started: str
    reason_for_taking: str
    response_to_medication: str
    prescribing_doctor: str


class PastPsychiatricMedication(pydantic.BaseModel):
    """The model for past psychiatric medication."""

    name: str
    initial_dosage: str
    maximum_dosage: str
    date_taken: str
    targetted_symptoms: str
    response: str
    prescribing_doctor: str


class EiCpseTherapy(pydantic.BaseModel):
    """Therapies from Committee on Preschool Special Education services."""

    type: Literal["early intervention", "cpse"]
    name: str
    duration: str
    dates: str


class FamilyPsychiatricHistory(pydantic.BaseModel):
    """The model for the patient's family psychiatric history."""

    diagnosis: str
    no_formal_diagnosis: bool
    family_members: list[str]

    @pydantic.field_validator("family_members", mode="before")
    def split_comma_separated_values(cls, value: str | list[str] | None) -> list[str]:  # noqa: N805
        """Splits comma separated values."""
        if isinstance(value, list):
            return [string.lower() for string in value]
        if value is None:
            return []
        return value.lower().split(",")
