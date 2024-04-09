"""Utilities for the file conversion router."""

import math
from typing import Any

import pytz
from dateutil import parser as dateutil_parser

from ctk_functions import config
from ctk_functions.functions.intake import descriptors, transformers

logger = config.get_logger()


class IntakeInformation:
    """The extracts the intake information for a patient."""

    def __init__(
        self,
        patient_data: dict[str, Any],
        *,
        timezone: str = "US/Eastern",
    ) -> None:
        """Initializes the intake information.

        Args:
            patient_data: The patient dataframe.
            timezone: The timezone of the intake.
        """
        logger.info("Parsing intake information.")
        self.patient = Patient(patient_data, timezone=timezone)
        self.phone = patient_data["phone"]


class Patient:
    """The patient model."""

    def __init__(
        self,
        patient_data: dict[str, Any],
        timezone: str = "US/Eastern",
    ) -> None:
        """Initializes the patient.

        Args:
            patient_data: The patient dataframe.
            timezone: The timezone of the intake.
        """
        logger.debug("Parsing patient information.")
        self.first_name = patient_data["firstname"]
        self.last_name = patient_data["lastname"]
        self.nickname = patient_data["othername"]
        self.age = math.floor(patient_data["age"])
        self.date_of_birth = dateutil_parser.parse(
            patient_data["dob"],
        ).replace(tzinfo=pytz.timezone(timezone))
        self._gender_enum = descriptors.Gender(patient_data["childgender"]).name
        self._gender_other = patient_data["childgender_other"]
        self._pronouns_enum = descriptors.Pronouns(patient_data["pronouns"]).name
        self._pronouns_other = patient_data["pronouns_other"]
        self.handedness = transformers.Handedness(
            descriptors.Handedness(patient_data["dominant_hand"]),
        )

        self.psychiatric_history = PsychiatricHistory(patient_data)

        self.languages = [
            Language(patient_data, identifier)
            for identifier in range(1, 3)
            if patient_data[f"child_language{identifier}"]
        ]
        self.language_spoken_best = descriptors.Language(
            patient_data["language_spoken"],
        ).name.replace("_", " ")
        if self.language_spoken_best == "other":
            self.language_spoken_best = patient_data["language_spoken_other"]
        self.education = Education(patient_data)
        self.development = Development(patient_data)
        self.guardian = Guardian(patient_data)
        self.household = Household(patient_data)

    @property
    def full_name(self) -> str:
        """The full name of the patient."""
        if self.nickname:
            return f'{self.first_name} "{self.nickname}" {self.last_name}'
        return f"{self.first_name} {self.last_name}"

    @property
    def gender(self) -> str:
        """The patient's gender."""
        if self._gender_enum == "other":
            return self._gender_other
        return self._gender_enum

    @property
    def pronouns(self) -> list[str]:
        """The patient's pronouns."""
        if self._pronouns_enum != "other":
            return self._pronouns_enum.split("_")

        pronouns = self._pronouns_other.split("/")
        defaults = [
            "he/she/they",
            "him/her/them",
            "his/her/their",
            "his/hers/theirs",
            "himself/herself/themselves",
        ]
        return pronouns + defaults[len(pronouns) :]

    @property
    def age_gender_label(self) -> str:
        """Converts the gender and age to an appropriate string."""
        child_age_cutoff = 15
        upper_age_cutoff = 18

        if self.age < child_age_cutoff:
            return (
                "girl"
                if "female" in self.gender
                else "boy"
                if "male" in self.gender
                else "child"
            )

        gender_string = (
            "woman"
            if "female" in self.gender
            else "man"
            if "male" in self.gender
            else "adult"
        )

        if self.age < upper_age_cutoff:
            return f"young {gender_string}"
        return gender_string


class Guardian:
    """The parser for a parent or guardian."""

    def __init__(self, patient_data: dict[str, Any]) -> None:
        """Initializes the guardian.

        Args:
            patient_data: The patient dataframe.
        """
        logger.debug("Parsing guardian information.")
        self.first_name = patient_data["guardian_first_name"]
        self.last_name = patient_data["guardian_last_name"]
        relationship_id = next(
            (
                identifier
                for identifier in range(1, 13)
                if patient_data[f"guardian_relationship___{identifier}"]
            ),
            descriptors.GuardianRelationship.other.value,
        )

        if relationship_id == descriptors.GuardianRelationship.other.value:
            self.relationship = (
                patient_data["other_relation"] or "no relationship provided"
            )
        else:
            self.relationship = descriptors.GuardianRelationship(
                relationship_id,
            ).name.replace("_", " ")

    @property
    def title_name(self) -> str:
        """The full name of the guardian."""
        return f"{self.title} {self.last_name}"

    @property
    def title_full_name(self) -> str:
        """The full name of the guardian."""
        return f"{self.title} {self.first_name} {self.last_name}"

    @property
    def title(self) -> str:
        """The title of the guardian.

        We scan for more keywords than are available in the descriptor to attempt
        to catch some of the "other" cases.

        Returns:
            str: The title of the guardian based on their inferred gender.
        """
        female_keywords = ["mother", "aunt", "carrier", "sister"]
        male_keywords = ["father", "uncle", "brother"]

        if any(keyword in self.relationship.lower() for keyword in male_keywords):
            return "Mr."
        if any(keyword in self.relationship.lower() for keyword in female_keywords):
            return "Ms./Mrs."
        return "Mr./Ms./Mrs."

    @property
    def parent_or_guardian(self) -> str:
        """The parent or guardian."""
        parent_keywords = ["mother", "father"]
        if any(keyword in self.relationship.lower() for keyword in parent_keywords):
            return "parent"
        return "guardian"


class Household:
    """The parser for household information."""

    def __init__(self, patient_data: dict[str, Any]) -> None:
        """Initializes the household.

        Args:
            patient_data: The patient dataframe.
        """
        logger.debug("Parsing household information.")
        n_members = patient_data["residing_number"]
        self.members = transformers.HouseholdMembers(
            [HouseholdMember(patient_data, i) for i in range(1, n_members + 1)],
        )
        self.guardian_marital_status = descriptors.GuardianMaritalStatus(
            patient_data["guardian_maritalstatus"],
        ).name.replace("_", " ")
        self.city = patient_data["city"]

        self.state = descriptors.USState(int(patient_data["state"])).name.replace(
            "_",
            " ",
        )
        self.languages = [
            descriptors.Language(identifier).name.replace("_", " ")
            for identifier in range(1, 25)
            if patient_data[f"language___{identifier}"] == "1"
        ]
        if patient_data["language_other"]:
            self.languages.append(patient_data["language_other"])


class Language:
    """The parser for a language."""

    def __init__(self, patient_data: dict[str, Any], identifier: int) -> None:
        """Initializes the language.

        Args:
            patient_data: The patient dataframe.
            identifier: The id of the language.
        """
        logger.debug(f"Parsing language {identifier}.")
        self.name = patient_data[f"child_language{identifier}"]
        self.spoken_whole_life = patient_data[f"child_language{identifier}_spoken"]
        self.spoken_since_age = patient_data[f"child_language{identifier}_age"]
        self.setting = patient_data[f"child_language{identifier}_setting"]
        self.fluency = descriptors.LanguageFluency(
            patient_data[f"child_language{identifier}_fluency"],
        ).name


class HouseholdMember:
    """The parser for a household member."""

    def __init__(self, patient_data: dict[str, Any], identifier: int) -> None:
        """Initializes the household member.

        Args:
            patient_data: The patient dataframe.
            identifier: The id of the household member.
        """
        logger.debug(f"Parsing household member {identifier}.")
        self.name = patient_data[f"peopleinhome{identifier}"]
        self.age = patient_data[f"peopleinhome{identifier}_age"]
        self.relationship = transformers.HouseholdRelationship(
            descriptors.HouseholdRelationship(
                patient_data[f"peopleinhome{identifier}_relation"],
            ),
            patient_data[f"peopleinhome{identifier}_relation_other"],
        ).transform()

        faulty_tag = 2  # Member 2's ID is missing in this field.
        if identifier != faulty_tag:
            self.relationship_quality = descriptors.RelationshipQuality(
                patient_data[f"peopleinhome{identifier}_relationship"],
            ).name
        else:
            self.relationship_quality = descriptors.RelationshipQuality(
                patient_data["peopleinhome_relationship"],
            ).name
        self.grade_occupation = patient_data[f"peopleinhome{identifier}_gradeocc"]


class Education:
    """The parser for the patient's education."""

    def __init__(self, patient_data: dict[str, Any]) -> None:
        """Initializes the education.

        Args:
            patient_data: The patient dataframe.
        """
        logger.debug("Parsing education information.")
        self.years_of_education = patient_data["yrs_school"]
        self.school_name = patient_data["school"]
        self.grade = patient_data["grade"]
        self.individualized_educational_program = (
            transformers.IndividualizedEducationProgram(
                descriptors.IndividualizedEducationProgram(patient_data["iep"]),
            )
        )
        self.school_type = descriptors.SchoolType(patient_data["schooltype"])
        self.classroom_type = transformers.ClassroomType(
            descriptors.ClassroomType(patient_data["classroomtype"]),
            other=patient_data["classroomtype_other"],
        )
        self.past_schools = transformers.PastSchools(
            [
                transformers.PastSchoolInterface(
                    name=patient_data[f"pastschool{identifier}"],
                    grades=patient_data[f"pastschool{identifier}_grades"],
                )
                for identifier in range(1, 11)
                if patient_data[f"pastschool{identifier}"]
            ],
        )


class Development:
    """The parser for the patient's development history."""

    def __init__(self, patient_data: dict[str, Any]) -> None:
        """Initalizes the development history.

        Args:
            patient_data: The patient dataframe.
        """
        logger.debug("Parsing development information.")
        self.duration_of_pregnancy = transformers.DurationOfPregnancy(
            patient_data["txt_duration_preg_num"],
        )
        self.delivery = transformers.BirthDelivery(
            descriptors.BirthDelivery(patient_data["opt_delivery"]),
            other=patient_data["csection_reason"],
        )
        self.delivery_location = transformers.DeliveryLocation(
            descriptors.DeliveryLocation(patient_data["birth_location"]),
            patient_data["birth_other"],
        )

        pregnancy_symptoms = [
            index
            for index in range(1, len(descriptors.BirthComplications) + 1)
            if patient_data[f"preg_symp___{index}"] == "1"
        ]
        self.birth_complications = transformers.BirthComplications(
            pregnancy_symptoms,
            other=patient_data["pregnancyhistory"],
        )
        self.premature_birth = bool(patient_data["premature"])
        self.premature_birth_specify = patient_data["premature_specify"]
        self.adaptability = transformers.Adaptability(
            descriptors.Adaptability(patient_data["infanttemp_adapt"]),
        )
        self.soothing_difficulty = descriptors.SoothingDifficulty(
            patient_data["infanttemp1"],
        )
        self.early_intervention_age = transformers.EarlyIntervention(
            patient_data["ei_age"],
        )
        self.cpse_age = transformers.CPSE(patient_data["cpse_age"])
        self.started_walking = transformers.DevelopmentSkill(
            patient_data["skill6"],
            other="started walking",
        )
        self.started_talking = transformers.DevelopmentSkill(
            patient_data["skill16"],
            other="started using meaningful words",
        )
        self.daytime_dryness = transformers.DevelopmentSkill(
            patient_data["skill12"],
            other="achieved daytime dryness",
        )
        self.nighttime_dryness = transformers.DevelopmentSkill(
            patient_data["skill13"],
            other="achieved nighttime dryness",
        )


class PsychiatricHistory:
    """The parser for the patient's psychiatric history."""

    def __init__(self, patient_data: dict[str, Any]) -> None:
        """Initializes the psychiatric history.

        Args:
            patient_data: The patient dataframe.
        """
        logger.debug("Parsing psychiatric history.")
        past_diagnoses = [
            descriptors.PastDiagnosis(
                diagnosis=patient_data[f"pastdx_{index}"],
                clinician=patient_data[f"dx_name{index}"],
                age=str(patient_data[f"age_{index}"]),
            )
            for index in range(1, 11)
            if patient_data[f"pastdx_{index}"]
        ]
        self.past_diagnoses = transformers.PastDiagnoses(past_diagnoses)
        self.therapeutic_interventions = [
            TherapeuticInterventions(patient_data, identifier)
            for identifier in range(1, 11)
            if patient_data[
                f"txhx_{identifier}" if identifier != 2 else f"txhx{identifier}"  # noqa: PLR2004
            ]
        ]
        self.aggresive_behaviors = transformers.AggressiveBehavior(
            patient_data["agress_exp"],
        )
        self.children_services = transformers.ChildrenServices(
            patient_data["acs_exp"],
        )
        self.violence_and_trauma = transformers.ViolenceAndTrauma(
            patient_data["violence_exp"],
        )
        self.self_harm = transformers.SelfHarm(patient_data["selfharm_exp"])


class TherapeuticInterventions:
    """The parser for the patient's therapeutic history."""

    def __init__(self, patient_data: dict[str, Any], identifier: int) -> None:
        """Initializes the therapeutic history.

        Args:
            patient_data: The patient dataframe.
            identifier: The id of the therapeutic history instance.
        """
        logger.debug(f"Parsing therapeutic intervention {identifier}.")
        faulty_identifier = 2
        if identifier != faulty_identifier:
            self.therapist = patient_data[f"txhx_{identifier}"]
        else:
            self.therapist = patient_data[f"txhx{identifier}"]
        self.reason = patient_data[f"txhx{identifier}_reason"]
        self.start = patient_data[f"txhx{identifier}_start"]
        self.end = patient_data[f"txhx{identifier}_end"]
        self.frequency = patient_data[f"txhx{identifier}_freq"]
        self.effectiveness = patient_data[f"txhx{identifier}_effectiveness"]
        self.reason_ended = patient_data[f"txhx{identifier}_terminate"]
