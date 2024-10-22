"""Utilities for the file conversion router."""

import math

import pytz
from dateutil import parser as dateutil_parser

from ctk_functions import config
from ctk_functions.functions.intake import parser_models, transformers
from ctk_functions.microservices import redcap

logger = config.get_logger()


class IntakeInformation:
    """The extracts the intake information for a patient."""

    def __init__(
        self,
        patient_data: redcap.RedCapData,
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
        self.phone = patient_data.phone


class Patient:
    """The patient model."""

    def __init__(
        self,
        patient_data: redcap.RedCapData,
        timezone: str = "US/Eastern",
    ) -> None:
        """Initializes the patient.

        Args:
            patient_data: The patient dataframe.
            timezone: The timezone of the intake.
        """
        logger.debug("Parsing patient information.")
        self.first_name = all_caps_to_title(patient_data.firstname)
        self.last_name = all_caps_to_title(patient_data.lastname)
        self.nickname = (
            all_caps_to_title(patient_data.othername)
            if patient_data.othername
            else None
        )
        self.age = math.floor(patient_data.age)
        self.date_of_birth = dateutil_parser.parse(
            patient_data.dob,
        ).replace(tzinfo=pytz.timezone(timezone))
        self._gender = (
            patient_data.childgender.name if patient_data.childgender else "other"
        )
        self._gender_other = patient_data.childgender_other
        self._pronouns = patient_data.pronouns.name
        self._pronouns_other = patient_data.pronouns_other
        self.handedness = transformers.Handedness(
            patient_data.dominant_hand,
        )

        self.reason_for_visit = patient_data.concern_current
        self.hopes = patient_data.outcome2
        self.learned_of_study = patient_data.referral2
        self.primary_care = PrimaryCareInformation(patient_data)

        self.psychiatric_history = PsychiatricHistory(patient_data)

        self.languages = [
            Language(patient_data, identifier)
            for identifier in range(1, 4)
            if getattr(patient_data, f"child_language{identifier}")
        ]
        if patient_data.language_spoken_other:
            self.language_spoken_best = patient_data.language_spoken_other
        else:
            self.language_spoken_best = patient_data.language_spoken.name.replace(
                "_",
                " ",
            )

        self.education = Education(patient_data)
        self.development = Development(patient_data)
        self.guardian = Guardian(patient_data)
        self.household = Household(patient_data)
        self.social_functioning = SocialFunctioning(patient_data)

    @property
    def full_name(self) -> str:
        """The full name of the patient."""
        return f"{self.first_name} {self.last_name}"

    @property
    def gender(self) -> str:
        """The patient's gender."""
        if self._gender == "other":
            return self._gender_other if self._gender_other else "NOT PROVIDED"
        return self._gender

    @property
    def pronouns(self) -> list[str]:
        """The patient's pronouns."""
        if self._pronouns != "other":
            return self._pronouns.split("_")

        pronouns = self._pronouns_other.split("/") if self._pronouns_other else []
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

    def __init__(self, patient_data: redcap.RedCapData) -> None:
        """Initializes the guardian.

        Args:
            patient_data: The patient dataframe.
        """
        logger.debug("Parsing guardian information.")
        self.first_name = all_caps_to_title(patient_data.guardian_first_name)
        self.last_name = all_caps_to_title(patient_data.guardian_last_name)
        if patient_data.guardian_relationship == redcap.GuardianRelationship.other:
            self.relationship = patient_data.other_relation or "NOT PROVIDED"
        else:
            self.relationship = patient_data.guardian_relationship.name.replace(
                "_",
                " ",
            )

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

    def __init__(self, patient_data: redcap.RedCapData) -> None:
        """Initializes the household.

        Args:
            patient_data: The patient dataframe.
        """
        logger.debug("Parsing household information.")
        n_members = patient_data.residing_number
        self.members = [
            HouseholdMember(patient_data, i) for i in range(1, n_members + 1)
        ]
        self.guardian_marital_status = patient_data.guardian_maritalstatus.name.replace(
            "_",
            " ",
        )
        self.city = all_caps_to_title(patient_data.city)

        self.state = patient_data.state.name.replace(
            "_",
            " ",
        )
        self.home_functioning = patient_data.home_func
        self.languages = patient_data.household_languages


class Language:
    """The parser for a language."""

    def __init__(self, patient_data: redcap.RedCapData, identifier: int) -> None:
        """Initializes the language.

        Args:
            patient_data: The patient dataframe.
            identifier: The id of the language.
        """
        logger.debug("Parsing language %s.", identifier)
        self.name = getattr(patient_data, f"child_language{identifier}")
        self.spoken_whole_life = getattr(
            patient_data,
            f"child_language{identifier}_spoken",
        )
        self.spoken_since_age: str = getattr(
            patient_data,
            f"child_language{identifier}_age",
        )
        self.setting: str = getattr(patient_data, f"child_language{identifier}_setting")
        self.fluency: str = getattr(
            patient_data,
            f"child_language{identifier}_fluency",
        ).name


class HouseholdMember:
    """The parser for a household member."""

    def __init__(self, patient_data: redcap.RedCapData, identifier: int) -> None:
        """Initializes the household member.

        Args:
            patient_data: The patient dataframe.
            identifier: The id of the household member.
        """
        logger.debug("Parsing household member %s.", identifier)
        self.name = all_caps_to_title(
            getattr(patient_data, f"peopleinhome{identifier}"),
        )
        self.age = getattr(patient_data, f"peopleinhome{identifier}_age")
        self.relationship = transformers.HouseholdRelationship(
            getattr(patient_data, f"peopleinhome{identifier}_relation"),
            getattr(patient_data, f"peopleinhome{identifier}_relation_other"),
        ).transform()

        self.relationship_quality = getattr(
            patient_data,
            f"peopleinhome{identifier}_relationship",
        ).name

        self.grade_occupation = getattr(
            patient_data,
            f"peopleinhome{identifier}_gradeocc",
        )


class Education:
    """The parser for the patient's education."""

    def __init__(self, patient_data: redcap.RedCapData) -> None:
        """Initializes the education.

        Args:
            patient_data: The patient dataframe.
        """
        logger.debug("Parsing education information.")
        self.years_of_education = patient_data.yrs_school
        self.school_name = all_caps_to_title(patient_data.school)
        self.grade = patient_data.grade
        self.individualized_educational_program = (
            transformers.IndividualizedEducationProgram(
                patient_data.iep,
            )
        )
        self.school_type = patient_data.schooltype
        self.classroom_type = transformers.ClassroomType(
            patient_data.classroomtype,
            other=patient_data.classroomtype_other,
        )
        self.past_schools = [
            parser_models.PastSchool(
                name=getattr(patient_data, f"pastschool{identifier}"),
                grades=getattr(patient_data, f"pastschool{identifier}_grades"),
                experience=getattr(patient_data, f"pastschool{identifier}comments"),
            )
            for identifier in range(1, 11)
            if getattr(patient_data, f"pastschool{identifier}")
        ]

        self.performance = patient_data.recent_academicperformance.name
        self.grades = transformers.EducationGrades(
            patient_data.current_grades,
        ).transform()
        self.school_functioning = patient_data.school_func


class PsychiatricMedication:
    """The parser for psychiatric medication."""

    def __init__(self, patient_data: redcap.RedCapData) -> None:
        """Initializes the psychiatric medication.

        Args:
            patient_data: The patient dataframe.
        """
        logger.debug("Parsing psychiatric medication.")
        if patient_data.psychmed_num:
            self.current_medication: (
                list[parser_models.CurrentPsychiatricMedication] | None
            ) = [
                parser_models.CurrentPsychiatricMedication(
                    name=getattr(patient_data, f"psychmed_name_{index}"),
                    initial_dosage=getattr(patient_data, f"startdose_{index}"),
                    current_dosage=getattr(patient_data, f"currentdose_{index}"),
                    reason_for_taking=getattr(patient_data, f"med{index}_reason"),
                    date_started=getattr(patient_data, f"med{index}_start"),
                    response_to_medication=getattr(patient_data, f"med{index}_se"),
                    prescribing_doctor=getattr(patient_data, f"med{index}_doc"),
                )
                for index in range(1, patient_data.psychmed_num + 1)
            ]
        else:
            self.current_medication = None

        if patient_data.past_psychmed_num:
            self.past_medication: (
                list[parser_models.PastPsychiatricMedication] | None
            ) = [
                parser_models.PastPsychiatricMedication(
                    name=getattr(patient_data, f"medname{index}_past"),
                    initial_dosage=getattr(patient_data, f"dose{index}_start_past"),
                    maximum_dosage=getattr(patient_data, f"dose{index}_max_past"),
                    date_taken=getattr(patient_data, f"med{index}_past_date"),
                    targetted_symptoms=getattr(patient_data, f"med{index}_past_reason"),
                    response=getattr(patient_data, f"med{index}_past_se"),
                    prescribing_doctor=getattr(patient_data, f"med{index}_past_doc"),
                )
                for index in range(1, patient_data.past_psychmed_num + 1)
            ]
        else:
            self.past_medication = None


class Development:
    """The parser for the patient's development history."""

    def __init__(self, patient_data: redcap.RedCapData) -> None:
        """Initalizes the development history.

        Args:
            patient_data: The patient dataframe.
        """
        logger.debug("Parsing development information.")
        self.duration_of_pregnancy = transformers.DurationOfPregnancy(
            patient_data.txt_duration_preg_num,
        )
        self.delivery = transformers.BirthDelivery(
            patient_data.opt_delivery,
            other=patient_data.csection_reason,
        )
        self.delivery_location = transformers.DeliveryLocation(
            patient_data.birth_location,
            patient_data.birth_other,
        )

        self.birth_complications = transformers.BirthComplications(
            patient_data.preg_symp,
            other=patient_data.pregnancyhistory,
        )
        self.premature_birth = bool(patient_data.premature)
        self.premature_birth_specify = patient_data.premature_specify
        self.adaptability = transformers.Adaptability(
            patient_data.infanttemp_adapt,
        )
        self.infant_difficulties = parser_models.InfantDifficulties(
            colic=patient_data.colic,
            eating_difficulties=patient_data.eating_difficulties,
            sleeping_difficulties=patient_data.sleeping_difficulties,
            did_not_enjoy_body_contact=patient_data.no_bodycontact,
            limp_or_stiff=patient_data.limp,
            problems_with_social_relatedness=patient_data.social_relatedness,
            overly_sensitive_to_sound=patient_data.sound_sensitivity,
        )
        self.soothing_difficulty = patient_data.infanttemp1

        cpse_encodings = (
            ("speechlang", "speech and language therapy"),
            ("occ_therapy", "occupational therapy"),
            ("phy_therapy", "physical therapy"),
            ("seit", "special education itinerant teacher"),
            ("aba", "applied behavior analysis"),
            ("other", "other"),
        )

        self.early_intervention = [
            parser_models.EiCpseTherapy(
                name=service[1],
                type="early intervention",
                dates=getattr(patient_data, f"{service[0]}_dates"),
                duration=getattr(patient_data, f"{service[0]}_dur"),
            )
            for index, service in enumerate(cpse_encodings)
            if getattr(patient_data, f"schoolservices___{index+1}") == "1"
        ]

        self.cpse_services = [
            parser_models.EiCpseTherapy(
                name=service[1],
                type="cpse",
                dates=getattr(patient_data, f"cpse_{service[0]}_dates"),
                duration=getattr(patient_data, f"cpse_{service[0]}_dur"),
            )
            for index, service in enumerate(cpse_encodings)
            if getattr(patient_data, f"cpse_services___{index+1}") == "1"
        ]

        self.started_walking = transformers.DevelopmentSkill(
            patient_data.skill6,
            other="started walking",
        )
        self.started_talking = transformers.DevelopmentSkill(
            patient_data.skill16,
            other="started using meaningful words",
        )
        self.daytime_dryness = transformers.DevelopmentSkill(
            patient_data.skill12,
            other="achieved daytime dryness",
        )
        self.nighttime_dryness = transformers.DevelopmentSkill(
            patient_data.skill13,
            other="achieved nighttime dryness",
        )


class PsychiatricHistory:
    """The parser for the patient's psychiatric history."""

    def __init__(self, patient_data: redcap.RedCapData) -> None:
        """Initializes the psychiatric history.

        Args:
            patient_data: The patient dataframe.
        """
        logger.debug("Parsing psychiatric history.")
        past_diagnoses = [
            redcap.PastDiagnosis(
                diagnosis=getattr(patient_data, f"pastdx_{index}"),
                clinician=getattr(patient_data, f"dx_name{index}"),
                age_at_diagnosis=str(getattr(patient_data, f"age_{index}")),
            )
            for index in range(1, 11)
            if getattr(patient_data, f"pastdx_{index}")
        ]
        self.past_diagnoses = transformers.PastDiagnoses(past_diagnoses)
        self.therapeutic_interventions = [
            TherapeuticInterventions(patient_data, identifier)
            for identifier in range(1, 11)
            if getattr(patient_data, f"txhx_{identifier}")
        ]
        self.medications = PsychiatricMedication(patient_data)
        self.is_follow_up_done = patient_data.clinician is not None
        self.aggresive_behaviors: str | None = patient_data.agress_exp
        self.children_services: str | None = patient_data.acs_exp
        self.violence_and_trauma: str | None = patient_data.violence_exp
        self.self_harm: str | None = patient_data.selfharm_exp
        self.family_psychiatric_history = FamilyPyshicatricHistory(
            patient_data,
        ).get_family_diagnoses(patient_data)


class FamilyPyshicatricHistory:
    """The parser for the patient's family's psychiatric history."""

    def __init__(self, patient_data: redcap.RedCapData) -> None:
        """Initializes the psychiatric history.

        Args:
            patient_data: The patient dataframe.
        """
        self.is_father_history_known = patient_data.biohx_dad_other
        self.is_mother_history_known = patient_data.biohx_mom_other
        self.family_diagnoses = self.get_family_diagnoses(patient_data)

    def get_family_diagnoses(
        self,
        patient_data: redcap.RedCapData,
    ) -> transformers.FamilyDiagnoses:
        """Gets the family diagnoses.

        There's an edge-case where the complete family history is unknown.
        REDCap defaults to True for diagnoses in this case, but this is
        undesired.

        Args:
            patient_data: The patient dataframe.

        Returns:
            The family diagnoses transformers.
        """
        if not self.is_father_history_known and not self.is_mother_history_known:
            history_known = "Family psychiatric history is unknown."
            return transformers.FamilyDiagnoses(
                [],
                history_known,
            )

        if not self.is_father_history_known:
            history_known = "Family history for the father is unknown."
        elif not self.is_mother_history_known:
            history_known = "Family history for the mother is unknown."
        else:
            history_known = ""

        family_diagnoses = [
            parser_models.FamilyPsychiatricHistory(
                diagnosis=diagnosis.name,
                no_formal_diagnosis=getattr(
                    patient_data,
                    f"{diagnosis.checkbox_abbreviation}___4",
                ),
                family_members=getattr(
                    patient_data,
                    f"{diagnosis.text_abbreviation}_text",
                ),
            )
            for diagnosis in redcap.family_psychiatric_diagnoses
        ]
        return transformers.FamilyDiagnoses(
            family_diagnoses,
            history_known,
        )


class TherapeuticInterventions:
    """The parser for the patient's therapeutic history."""

    def __init__(self, patient_data: redcap.RedCapData, identifier: int) -> None:
        """Initializes the therapeutic history.

        Args:
            patient_data: The patient data.
            identifier: The id of the therapeutic history instance.
        """
        logger.debug("Parsing therapeutic intervention %s.", identifier)
        self.therapist = getattr(patient_data, f"txhx_{identifier}")
        self.reason = getattr(patient_data, f"txhx{identifier}_reason")
        self.start = getattr(patient_data, f"txhx{identifier}_start")
        self.end = getattr(patient_data, f"txhx{identifier}_end")
        self.frequency = getattr(patient_data, f"txhx{identifier}_freq")
        self.effectiveness = getattr(patient_data, f"txhx{identifier}_effectiveness")
        self.reason_ended = getattr(patient_data, f"txhx{identifier}_terminate")


class PrimaryCareInformation:
    """The parser for the patient's primary care information."""

    def __init__(self, patient_data: redcap.RedCapData) -> None:
        """Initializes the primary care information.

        Args:
            patient_data: The patient data.
        """
        logger.debug("Parsing primary care information.")
        hearing_device = transformers.HearingDevice(
            patient_data.child_hearing_aid,
        )
        glasses = transformers.Glasses(
            patient_data.child_glasses,
        )
        if (
            glasses.base == redcap.Glasses.no
            and hearing_device.base == redcap.HearingDevice.no
        ):
            self.glasses_hearing_device = """
                {{PREFERRED_NAME}} does not wear prescription
                glasses or use a hearing device
              """
        else:
            self.glasses_hearing_device = f"""
                {{{{PREFERRED_NAME}}}} {glasses.transform()}.
                {{{{PRONOUN_0}}}} {hearing_device.transform()}
            """

        diseases = [
            redcap.PriorDisease(
                name=disease,
                was_positive=getattr(patient_data, disease),
                age=getattr(patient_data, f"{disease}_age"),
                treatment=getattr(patient_data, f"{disease}_treatment"),
            )
            for disease in ("seizures", "migraines", "meningitis", "encephalitis")
        ]
        self.prior_diseases = transformers.PriorDiseases(diseases).transform()


class SocialFunctioning:
    """The parser for the patient's social functioning."""

    def __init__(self, patient_data: redcap.RedCapData) -> None:
        """Initializes the social functioning.

        Args:
            patient_data: The patient data.
        """
        logger.debug("Parsing social functioning.")
        self.hobbies = patient_data.child_interests
        self.n_friends = patient_data.close_friends
        self.friendship_quality = patient_data.peer_relations.name


def all_caps_to_title(name: str) -> str:
    """Converts a name from all caps to title case.

    Though this won't always be correct, it's a good heuristic for names.

    Args:
        name: The name to convert.

    Returns:
        The name in title case.
    """
    if all(char.isupper() for char in name if char.isalpha()):
        return name.title()
    return name
