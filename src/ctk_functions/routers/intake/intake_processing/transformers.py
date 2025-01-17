"""Contains the transformers for intake form conversion.

These transformers are used to create more complicated strings based on the
intake form data. It uses an abstract base class that enforces the creation of a
transform method for each transformer.

For strings too complicated for the transformers, a large language model is used.
"""

import abc
import enum
import re
from typing import Generic, TypeVar

from ctk_functions.core import exceptions
from ctk_functions.microservices import redcap
from ctk_functions.routers.intake.intake_processing import parser_models
from ctk_functions.routers.intake.intake_processing.utils import string_utils

T = TypeVar("T")


class ReplacementTags(str, enum.Enum):
    """These tags will be replaced with the actual values in the final report."""

    PREFERRED_NAME = "{{PREFERRED_NAME}}"
    REPORTING_GUARDIAN = "{{REPORTING_GUARDIAN}}"
    PRONOUN_0 = "{{PRONOUN_0}}"
    PRONOUN_2 = "{{PRONOUN_2}}"


class Transformer(Generic[T], abc.ABC):
    """Base class for transformers.

    Transformers are used to match and transform objects based on certain conditions.
    These are used to generalize the process of handling complicated cases for the
    parent intake form conversions.
    """

    def __init__(
        self,
        value: T,
        other: None | str = None,
    ) -> None:
        """Initializes the transformer.

        Args:
            value: The value to be transformed.
            other: Specifier for a freeform value.
        """
        self.base = value
        self.other = other

    def __str__(self) -> str:
        """Returns the transformed object.

        This is overwritten as accidentally printing the object, rather than the
        transformed object, is an easy mistake to make but should rarely, if ever, be
        done.
        """
        return self.transform()

    @abc.abstractmethod
    def transform(self) -> str:
        """Transforms the given object.

        Args:
            obj: The object to be transformed.

        Returns:
            T: The transformed object.
        """
        ...


class MultiTransformer(Transformer[list[T]]):
    """A transformer that can handle multiple values."""

    def __init__(self, value: list[T], other: None | str = None) -> None:
        """Initializes the multi transformer."""
        super().__init__(value, other)

    def __str__(self) -> str:
        """Returns the transformed object.

        This is overwritten as accidentally printing the object, rather than the
        transformed object, is an easy mistake to make but should rarely, if ever, be
        done.
        """
        return self.transform()

    @abc.abstractmethod
    def transform(self) -> str:
        """Transforms the given object.

        Args:
            obj: The object to be transformed.

        Returns:
            T: The transformed object.
        """
        ...


class Handedness(Transformer[redcap.Handedness]):
    """The transformer for handedness."""

    def transform(self) -> str:
        """Transforms the handedness information to a string.

        Returns:
            str: The transformed object.
        """
        if self.base == redcap.Handedness.unknown:
            return ""
        return f"{self.base.name}-handed"


class IndividualizedEducationProgram(
    Transformer[redcap.IndividualizedEducationProgram],
):
    """The transformer for individualized education programs."""

    def transform(self) -> str:
        """Transforms the individualized education program information to a string.

        Returns:
            str: The transformed object.
        """
        if self.base == redcap.IndividualizedEducationProgram.no:
            return "did not have an Individualized Education Program (IEP)"
        return (
            "had an Individualized Education Program (IEP) with an educational "
            f'classification of "{self.other}"'
        )


class DurationOfPregnancy(Transformer[str | None]):
    """The transfomer for time of pregnancy."""

    def transform(self) -> str:
        """Transforms the time of pregnancy information to a string.

        Though most guardians answer with just a number, the field is a freeform string.
        This transformer attempts to wrangle the data into a consistent format of
        "X weeks", but will fall back to the quoted original string if it can't.

        Returns:
            str: The transformed object.
        """
        if not self.base:
            return "unspecified"
        try:
            duration_of_pregnancy = float(self.base)
        except ValueError:
            parts = self.base.split()
            numeric_pattern = (
                r"[0-9]{2}"  # A 2-digit number
                r"((\.|\,)[0-9])?"  # Optionally a period or comma followed by 1 number.
            )
            if (
                len(parts) == 2  # noqa: PLR2004
                and re.match(numeric_pattern, parts[0])
                and parts[1].lower() == "weeks"
            ):
                # Common edge case: guardian writes "40 weeks".
                # This doesn't need additional quotes.
                return self.base.lower()
            return f'"{self.base}"'
        return f"{duration_of_pregnancy:g} weeks"


class BirthDelivery(Transformer[redcap.BirthDelivery]):
    """The transformer for birth delivery."""

    def transform(self) -> str:
        """Transforms the birth delivery information to a string.

        Returns:
            str: The transformed object.
        """
        if self.base == redcap.BirthDelivery.unknown:
            return "an unknown type of delivery"
        if self.base == redcap.BirthDelivery.vaginal:
            return "a vaginal delivery"

        other = self.other if self.other else "unspecified"
        return f'a cesarean section due to "{other}"'


class DeliveryLocation(Transformer[redcap.DeliveryLocation]):
    """The transformer for birth location."""

    def transform(self) -> str:
        """Transforms the birth location information to a string.

        Returns:
            str: The transformed object.
        """
        if self.base == redcap.DeliveryLocation.other:
            if self.other is None:
                return "an unspecified location"
            return self.other

        if self.base == redcap.DeliveryLocation.hospital:
            return "a hospital"
        return "home"


class Adaptability(Transformer[redcap.Adaptability]):
    """The transformer for infant adaptability."""

    def transform(self) -> str:
        """Transforms the infant adaptability information to a string.

        Returns:
            str: The transformed object.
        """
        if self.base == redcap.Adaptability.difficult:
            return "a slow to warm up temperament"
        return "an adaptable temperament"


class ClassroomType(Transformer[redcap.ClassroomType]):
    """The transformer for classroom type."""

    def transform(self) -> str:
        """Transforms the classroom type information to a string.

        Returns:
            str: The transformed object.
        """
        if self.base == redcap.ClassroomType.other:
            if self.other is None:
                return "an unspecified classroom type"
            return self.other

        return self.base.name.replace("_", " ").replace("COLON", ":").strip()


class DevelopmentSkill(Transformer[str | int]):
    """The transformer for developmental skills."""

    def transform(self) -> str:
        """Transforms the developmental skills information to a string.

        It is assumed that any integer value less than 7 is in years, and
        otherwise it is in months.

        Returns:
            str: The transformed object.
        """
        if isinstance(self.base, int) or self.base.isnumeric():
            month_threshold = 6
            if float(self.base) > month_threshold:
                return f"{self.other} at {self.base} months"
            return f"{self.other} at {self.base} years"
        if self.base.lower() == "not yet":
            return f"has not {self.other} yet"
        if self.base.lower() in ["normal", "late"]:
            return f"{self.other} at a {self.base.lower()} age"
        if self.base.lower() == "early":
            return f"{self.other} at an early age"
        return f"{self.other} at {self.base}"


class PastDiagnoses(MultiTransformer[parser_models.PastDiagnosis]):
    """The transformer for past diagnoses."""

    def transform(self, *, short: bool = True) -> str:
        """Transforms the past diagnoses information to a string.

        Args:
            short: Whether to use the short form of the string.

        Returns:
            str: The transformed object.
        """
        if len(self.base) == 0:
            return "with no prior history of psychiatric diagnoses"

        if short:
            return "with a prior history of " + string_utils.join_with_oxford_comma(
                [val.diagnosis for val in self.base],
            )

        return (
            "was diagnosed with the following psychiatric diagnoses: "
            + string_utils.join_with_oxford_comma(
                [
                    f"{val.diagnosis} at {val.age_at_diagnosis} by {val.clinician}"
                    for val in self.base
                ],
            )
        )


class HouseholdRelationship(Transformer[redcap.HouseholdRelationship]):
    """The transformer for household members."""

    def transform(self) -> str:
        """Transforms the household member information to a string.

        Returns:
            str: The transformed object.
        """
        if self.base == redcap.HouseholdRelationship.other_relative:
            return self.other if self.other else "unspecified relationship"
        return self.base.name.replace("_", " ")


class HearingDevice(Transformer[redcap.HearingDevice]):
    """Transformer for the hearing device information."""

    def transform(self) -> str:
        """Transforms the hearing device information to a string.

        Returns:
            str: The transformed object.
        """
        if self.base == redcap.HearingDevice.no:
            return "does not use a hearing device"
        if self.base == redcap.HearingDevice.at_school_and_home:
            return "uses a hearing device at school and at home"
        if self.base == redcap.HearingDevice.at_school:
            return "uses a hearing device at school"
        if self.base == redcap.HearingDevice.at_home:
            return "uses a hearing device at home"

        msg = "Invalid hearing device value."
        raise exceptions.TransformerError(msg)


class Glasses(Transformer[redcap.Glasses]):
    """Transformer for the glasses information."""

    def transform(self) -> str:
        """Transforms the glasses information to a string.

        Returns:
            str: The transformed object.
        """
        if self.base == redcap.Glasses.no:
            return "does not wear prescription glasses"
        if self.base == redcap.Glasses.at_school_and_home:
            return "wears prescription glasses at school and at home"
        if self.base == redcap.Glasses.at_school:
            return "wears prescription glasses at school"
        if self.base == redcap.Glasses.at_home:
            return "wears prescription glasses at home"
        msg = "Invalid glasses value."
        raise exceptions.TransformerError(msg)


class PriorDiseases(
    MultiTransformer[parser_models.PriorDisease],
):
    """Transformer for the prior diseases' information."""

    def transform(self) -> str:
        """Transforms the prior diseases information to a string.

        Returns:
            str: The transformed object.
        """
        if len(self.base) == 0:
            return "no prior history of diseases"

        positive_diseases = [
            disease.name for disease in self.base if disease.was_positive
        ]
        negative_diseases = [
            disease.name for disease in self.base if not disease.was_positive
        ]

        if not negative_diseases:
            string = f"""
                {ReplacementTags.REPORTING_GUARDIAN.value} reported a history of
                {string_utils.join_with_oxford_comma(
                    [disease.name for disease in self.base],
                )}"""
        elif not positive_diseases:
            string = f"""
                {ReplacementTags.REPORTING_GUARDIAN.value} denied any history of
                {string_utils.join_with_oxford_comma(
                    [disease.name for disease in self.base],
                )}"""
        else:
            string = f"""
                {ReplacementTags.REPORTING_GUARDIAN.value} reported a history of
                {string_utils.join_with_oxford_comma(positive_diseases)} and denied
                any history of
                {string_utils.join_with_oxford_comma(negative_diseases)}
            """

        return string_utils.remove_excess_whitespace(string)


class EducationGrades(Transformer[redcap.EducationGrades]):
    """Transformer for the education grades information."""

    def transform(self) -> str:
        """Transforms the education grades information to a string.

        Returns:
            str: The transformed object.
        """
        if self.base == redcap.EducationGrades.not_graded:
            return f"though {ReplacementTags.PRONOUN_0.value} is not formally graded"

        word_to_number = {
            "ONE": "1's",
            "TWO": "2's",
            "THREE": "3's",
            "FOUR": "4's",
        }
        grades = word_to_number.get(self.base.name, self.base.name)
        text = f"as {ReplacementTags.PRONOUN_0.value} receives mostly {grades}"
        if self.base in (
            redcap.EducationGrades.ONE,
            redcap.EducationGrades.TWO,
            redcap.EducationGrades.THREE,
            redcap.EducationGrades.FOUR,
        ):
            text += " on a 4-point scale"
        return text


class FamilyDiagnoses(MultiTransformer[parser_models.FamilyPsychiatricHistory]):
    """The transformer for family diagnoses."""

    def transform(self) -> str:
        """Transforms the family diagnoses information to a string.

        Returns:
            str: The transformed object.
        """
        if not self.base:
            return self.other if self.other else ""

        no_past_diagnosis = [val for val in self.base if val.no_formal_diagnosis]
        past_diagnosis = [val for val in self.base if not val.no_formal_diagnosis]

        text = self.other if self.other else ""
        if len(past_diagnosis) > 0:
            if text:
                text += " "
            text += (
                f"{ReplacementTags.PREFERRED_NAME.value}'s family history is "
                "significant for "
            )
            past_diagosis_texts = [
                self._past_diagnosis_text(val) for val in past_diagnosis
            ]
            text += string_utils.join_with_oxford_comma(past_diagosis_texts)
            text += "."

        if len(no_past_diagnosis) > 0:
            if text:
                text += " "
            if len(no_past_diagnosis) > 1:
                no_diagnosis_names = [val.diagnosis for val in no_past_diagnosis]
                text += (
                    "Family history of the following diagnoses was denied: "
                    + string_utils.join_with_oxford_comma(no_diagnosis_names)
                )
            else:
                text += f"Family history of {no_past_diagnosis[0].diagnosis} was denied"
            text += "."
        return text

    @staticmethod
    def _past_diagnosis_text(diagnosis: parser_models.FamilyPsychiatricHistory) -> str:
        """Transforms a family diagnosis to a string.

        Args:
            diagnosis: The family diagnosis.

        Returns:
            str: The transformed object.
        """
        family_members = string_utils.join_with_oxford_comma(diagnosis.family_members)
        if family_members:
            return f"{diagnosis.diagnosis} ({family_members})"
        return diagnosis.diagnosis
