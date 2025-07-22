"""Models for parsing the intake data.

Separate module is used as some of these need to be imported in both the parser and
the transformers.
"""

from collections.abc import Iterable
from typing import Literal

import pydantic


class CommentBaseModel:
    """Base model that can generate a human-readable string representation of itself."""

    def __str__(self) -> str:
        """Converts a class to a human read-able format."""
        properties = []
        for key, value in vars(self).items():
            if value is None or key.startswith("_"):
                continue

            if isinstance(value, Iterable) and not isinstance(value, str | bytes):
                text = ", ".join(str(val) for val in value)
            else:
                text = str(value)
            properties.append(f"{key.replace('_', ' ')}: {text}")

        return "\n".join(properties)


class PastDiagnosis(CommentBaseModel, pydantic.BaseModel):
    """The model for the patient's past diagnosis."""

    diagnosis: str
    clinician: str
    age_at_diagnosis: str


class InfantDifficulties(CommentBaseModel, pydantic.BaseModel):
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


class IepService(CommentBaseModel, pydantic.BaseModel):
    """Specifics of an IEP service."""

    name: str
    duration: str | None = None
    frequency: str | None = None


class PastSchool(CommentBaseModel, pydantic.BaseModel):
    """The model for past schools."""

    name: str
    grades: str
    experience: str


class CurrentPsychiatricMedication(CommentBaseModel, pydantic.BaseModel):
    """The model for current psychiatric medication."""

    name: str
    initial_dosage: str
    current_dosage: str
    date_started: str
    reason_for_taking: str
    response_to_medication: str
    prescribing_doctor: str


class PastPsychiatricMedication(CommentBaseModel, pydantic.BaseModel):
    """The model for past psychiatric medication."""

    name: str
    initial_dosage: str
    maximum_dosage: str
    date_taken: str
    targeted_symptoms: str
    response: str
    prescribing_doctor: str


class EiCpseTherapy(CommentBaseModel, pydantic.BaseModel):
    """Therapies from Committee on Preschool Special Education services."""

    type: Literal["early intervention", "cpse"]
    name: str
    duration: str
    dates: str


class FamilyPsychiatricHistory(CommentBaseModel, pydantic.BaseModel):
    """The model for the patient's family psychiatric history.

    Attributes:
        name: Name of the disorder.
        first_degree: Whether a first-degree family member was diagnosed.
        second_degree: Whether a second-degree family member was diagnosed.
        third_degree: Whether a third-degree family member was diagnosed.
        is_diagnosed: Whether a family member has been diagnosed.
        family_members: String containing elaboration on which family members were
            diagnosed.
    """

    name: str
    first_degree: bool
    second_degree: bool
    third_degree: bool
    is_diagnosed: bool
    family_members: str


class PriorDisease(pydantic.BaseModel):
    """Class used for prior diseases in the Primary Care Information."""

    name: str
    was_positive: bool
    age: str | None = None
    treatment: str | None = None
