"""Contains the transformers for intake form conversion.

These transformers are used to create more complicated strings based on the
intake form data. It uses an abstract base class that enforces the creation of a
transform method for each transformer.

For strings too complicated for the transformers, a large language model is used.
"""

import abc
import enum
from typing import Any, Generic, Protocol, TypeVar

from ctk_functions.functions.intake import descriptors
from ctk_functions.functions.intake.utils import string_utils

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
        other: Any = None,  # noqa: ANN401
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


class Handedness(Transformer[descriptors.Handedness]):
    """The transformer for handedness."""

    def transform(self) -> str:
        """Transforms the handedness information to a string.

        Returns:
            str: The transformed object.
        """
        if self.base == descriptors.Handedness.unknown:
            return ""
        return f"{self.base.name}-handed"


class IndividualizedEducationProgram(
    Transformer[descriptors.IndividualizedEducationProgram],
):
    """The transformer for individualized education programs."""

    def transform(self) -> str:
        """Transforms the individualized education program information to a string.

        Returns:
            str: The transformed object.
        """
        if self.base == descriptors.IndividualizedEducationProgram.no:
            return "did not have an Individualized Education Program (IEP)"
        return "had an Individualized Education Program (IEP)"


class BirthComplications(
    MultiTransformer[descriptors.BirthComplications],
):
    """The transformer for birth complications."""

    def __init__(self, value: list[int], other: str | None = None) -> None:
        """Initializes the pregnancy symptoms transformer.

        Args:
            value: The birth complication enum values.
            other: Specifier for a freeform value.

        """
        super().__init__([descriptors.BirthComplications(val) for val in value], other)

    def transform(self) -> str:
        """Transforms the birth complications information to a string.

        Returns:
            str: The transformed object.
        """
        if (
            descriptors.BirthComplications.none_of_the_above in self.base
            and len(self.base) > 1
        ):
            return """MANUAL INTERVENTION REQUIRED: 'None of the above' should not
            be selected with other birth complications."""
        if descriptors.BirthComplications.none_of_the_above in self.base:
            return "no birth complications"

        names = []
        for val in self.base:
            if val == descriptors.BirthComplications.other_illnesses:
                if self.other is None:
                    names.append("an unspecified illness")
                else:
                    names.append(self.other)
            else:
                names.append(val.name.replace("_", " "))
        if len(names) == 1:
            return f"the following birth complication: {names[0]}"
        return (
            "the following birth complications: "
            + string_utils.join_with_oxford_comma(
                names,
            )
        )


class DurationOfPregnancy(Transformer[str]):
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
            if len(parts) == 2 and parts[0].isnumeric() and parts[1].lower() == "weeks":  # noqa: PLR2004
                # Common edge case: guardian writes "40 weeks".
                # This doesn't need additional quotes.
                return self.base.lower()
            return f'"{self.base}"'
        return f"{duration_of_pregnancy:g} weeks"


class BirthDelivery(Transformer[descriptors.BirthDelivery]):
    """The transformer for birth delivery."""

    def transform(self) -> str:
        """Transforms the birth delivery information to a string.

        Returns:
            str: The transformed object.
        """
        if self.base == descriptors.BirthDelivery.unknown:
            return "an unknown type of delivery"
        if self.base == descriptors.BirthDelivery.vaginal:
            return "a vaginal delivery"

        other = self.other if self.other else "unspecified"
        return f'a cesarean section due to "{other}"'


class DeliveryLocation(Transformer[descriptors.DeliveryLocation]):
    """The transformer for birth location."""

    def transform(self) -> str:
        """Transforms the birth location information to a string.

        Returns:
            str: The transformed object.
        """
        if self.base == descriptors.DeliveryLocation.other:
            if self.other is None:
                return "an unspecified location"
            return self.other

        if self.base == descriptors.DeliveryLocation.hospital:
            return "a hospital"
        return "home"


class Adaptability(Transformer[descriptors.Adaptability]):
    """The transformer for infant adaptability."""

    def transform(self) -> str:
        """Transforms the infant adaptability information to a string.

        Returns:
            str: The transformed object.
        """
        if self.base == descriptors.Adaptability.difficult:
            return "a slow to warm up temperament"
        return "an adaptable temperament"


class GuardianMaritalStatus(Transformer[descriptors.GuardianMaritalStatus]):
    """The transformer for guardian marital status."""

    def transform(self) -> str:
        """Transforms the guardian marital status information to a string.

        Returns:
            str: The transformed object.
        """
        if self.base == descriptors.GuardianMaritalStatus.domestic_partnership:
            return "The parents/guardians are in a domestic partnership"
        if self.base == descriptors.GuardianMaritalStatus.widowed:
            return "The parent/guardian is widowed"
        if self.base == descriptors.GuardianMaritalStatus.never_married:
            return "The parents/guardians were never married"
        return f"The parents/guardians are {self.base.name.replace('_', ' ')}"


class ClassroomType(Transformer[descriptors.ClassroomType]):
    """The transformer for classroom type."""

    def transform(self) -> str:
        """Transforms the classroom type information to a string.

        Returns:
            str: The transformed object.
        """
        if self.base == descriptors.ClassroomType.other:
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
            if float(self.base) > 6:
                return f"{self.other} at {self.base} months"
            return f"{self.other} at {self.base} years"
        if self.base.lower() == "not yet":
            return f"has not {self.other} yet"
        if self.base.lower() in ["normal", "late"]:
            return f"{self.other} at a {self.base.lower()} age"
        if self.base.lower() == "early":
            return f"{self.other} at an early age"
        return f"{self.other} at {self.base}"


class PastDiagnoses(MultiTransformer[descriptors.PastDiagnosis]):
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


class HouseholdRelationship(Transformer[descriptors.HouseholdRelationship]):
    """The transformer for household members."""

    def transform(self) -> str:
        """Transforms the household member information to a string.

        Returns:
            str: The transformed object.
        """
        if self.base == descriptors.HouseholdRelationship.other_relative:
            return self.other if self.other else "unspecified relationship"
        return self.base.name.replace("_", " ")


class HouseholdMemberInterface(Protocol):
    """Interface for household members.

    Needed to prevent circular import from parsers.
    """

    name: str
    age: str
    relationship: str
    relationship_quality: str
    grade_occupation: str


class HouseholdMembers(MultiTransformer[HouseholdMemberInterface]):
    """The transformer for household members."""

    def transform(self) -> str:
        """Transforms the household member information to a string.

        Returns:
            str: The transformed object.
        """
        if len(self.base) == 0:
            return "no other household members"

        member_strings = [
            self.household_member_to_string(member) for member in self.base
        ]

        return string_utils.join_with_oxford_comma(member_strings)

    def household_member_to_string(self, member: HouseholdMemberInterface) -> str:
        """Converts a household member to a string representation.

        Clinical staff prefers to only use the name of the parents, and only include
        occupation for those who are not students. We use age as a proxy for this.

        Args:
            member: The HouseholdMemberInterface object to convert.

        Returns:
            The string representation of the household member.

        """
        string = f"{ReplacementTags.PRONOUN_2.value} {member.relationship}"
        is_parent = any(
            parent in member.relationship.lower() for parent in ["father", "mother"]
        )
        if is_parent:
            string += f" {member.name}"
        member_properties = [
            str(member.age),
            member.relationship_quality + " relationship",
        ]

        age = string_utils.StringToInt().parse(member.age)
        if (isinstance(age, int) and age > 21) or isinstance(age, str):  # noqa: PLR2004
            member_properties.append(member.grade_occupation.lower())

        string += f" ({', '.join(member_properties)})"
        return string


class HearingDevice(Transformer[descriptors.HearingDevice]):
    """Transformer for the hearing device information."""

    def transform(self) -> str:
        """Transforms the hearing device information to a string.

        Returns:
            str: The transformed object.
        """
        if self.base == descriptors.HearingDevice.no:
            return "does not use a hearing device"
        if self.base == descriptors.HearingDevice.at_school_and_home:
            return "uses a hearing device at school and at home"
        if self.base == descriptors.HearingDevice.at_school:
            return "uses a hearing device at school"
        if self.base == descriptors.HearingDevice.at_home:
            return "uses a hearing device at home"
        raise ValueError("Invalid hearing device value.")


class Glasses(Transformer[descriptors.Glasses]):
    """Transformer for the glasses information."""

    def transform(self) -> str:
        """Transforms the glasses information to a string.

        Returns:
            str: The transformed object.
        """
        if self.base == descriptors.Glasses.no:
            return "does not wear prescription glasses"
        if self.base == descriptors.Glasses.at_school_and_home:
            return "wears prescription glasses at school and at home"
        if self.base == descriptors.Glasses.at_school:
            return "wears prescription glasses at school"
        if self.base == descriptors.Glasses.at_home:
            return "wears prescription glasses at home"
        raise ValueError("Invalid glasses value.")


class GlassesHearingDevice(Transformer[Transformer[descriptors.Glasses]]):
    """Transformer for the glasses and hearing device information.

    The phrasing of this changes when both are no, hence the need for a combined
    transformer. The other paramaeter is set to the hearing device transformer.
    """

    def transform(self) -> str:
        """Transforms the glasses and hearing device information to a string.

        Returns:
            str: The transformed object.
        """
        if not isinstance(self.other, HearingDevice):
            raise ValueError("Invalid hearing device value.")
        if (
            self.base.base == descriptors.Glasses.no
            and self.other.base == descriptors.HearingDevice.no
        ):
            string = f"""
                {ReplacementTags.PREFERRED_NAME.value} does not wear prescription
                glasses or use a hearing device
              """
        else:
            string = f"""
                {ReplacementTags.PREFERRED_NAME.value} {self.base.transform()}.
                {ReplacementTags.PRONOUN_0.value} {self.other.transform()}
            """

        return string_utils.remove_excess_whitespace(string)


class PriorDiseases(MultiTransformer[descriptors.PriorDisease]):
    """Transformer for the prior diseases information."""

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
                {ReplacementTags.REPORTING_GUARDIAN.value} reported a prior history of
                {string_utils.join_with_oxford_comma(
                    [disease.name for disease in self.base],
                )}"""
        elif not positive_diseases:
            string = f"""
                {ReplacementTags.REPORTING_GUARDIAN.value} denied any prior history of
                {string_utils.join_with_oxford_comma(
                    [disease.name for disease in self.base],
                )}"""
        else:
            string = f"""
                {ReplacementTags.REPORTING_GUARDIAN.value} reported a prior history of:
                {string_utils.join_with_oxford_comma(positive_diseases)} and denied
                any history of:
                {string_utils.join_with_oxford_comma(negative_diseases)}
            """

        return string_utils.remove_excess_whitespace(string)


class EducationGrades(Transformer[descriptors.EducationGrades]):
    """Transformer for the education grades information."""

    def transform(self) -> str:
        """Transforms the education grades information to a string.

        Returns:
            str: The transformed object.
        """
        word_to_number = {
            "ONE": "1s",
            "TWO": "2s",
            "THREE": "3s",
            "FOUR": "4s",
        }
        if self.base.name in word_to_number:
            return word_to_number[self.base.name]
        return self.base.name.replace("_", " ")


class FamilyDiagnoses(MultiTransformer[descriptors.FamilyPsychiatricHistory]):
    """The transformer for family diagnoses."""

    def transform(self) -> str:
        """Transforms the family diagnoses information to a string.

        Returns:
            str: The transformed object.
        """
        if not self.base:
            return self.other

        no_past_diagnosis = [val for val in self.base if val.no_formal_diagnosis]
        past_diagnosis = [val for val in self.base if not val.no_formal_diagnosis]

        text = self.other if self.other else ""
        if len(past_diagnosis) > 0:
            if text:
                text += " "
            text += (
                f"{ReplacementTags.PREFERRED_NAME.value}'s family history is "
                + "significant for "
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
    def _past_diagnosis_text(diagnosis: descriptors.FamilyPsychiatricHistory) -> str:
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
