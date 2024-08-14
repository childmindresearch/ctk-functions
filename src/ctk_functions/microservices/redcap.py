"""This module contains functions for interacting with REDcap."""

import csv
import enum
import io
import re
from typing import Any, Literal, Self

import pydantic
import redcap

from ctk_functions import config, exceptions

settings = config.get_settings()
REDCAP_ENDPOINT = settings.REDCAP_ENDPOINT
REDCAP_API_TOKEN = settings.REDCAP_API_TOKEN

logger = config.get_logger()


class Gender(enum.Enum):
    """The gender of the patient."""

    male = "0"
    female = "1"
    non_binary = "2"
    transgender_male = "3"
    transgender_female = "4"
    other = "5"


class Pronouns(enum.Enum):
    """The pronouns of the patient."""

    he_him_his_his_himself = "0"
    she_her_her_hers_herself = "1"
    they_them_their_theirs_themselves = "2"
    ze_zir_zir_zirs_zirself = "3"
    other = "4"


class Handedness(enum.Enum):
    """The dominant hand of the patient."""

    left = "1"
    right = "2"
    unknown = "3"


class GuardianRelationship(enum.Enum):
    """The relationship of the guardian to the patient."""

    biological_mother = 1
    biological_father = 2
    grandparent = 3
    aunt = 4
    uncle = 5
    foster_father = 6
    foster_mother = 7
    adoptive_father = 8
    adoptive_mother = 9
    state_or_foster_care_representative = 10
    gestational_carrier = 11
    other = 12


class SchoolType(enum.Enum):
    """The type of school the patient attends."""

    boarding = "1"
    home = "2"
    parochial = "3"
    private = "4"
    public = "5"
    special = "6"
    vocational = "7"
    charter = "8"
    other = "9"


class ClassroomType(enum.Enum):
    """The type of classroom the patient is in.

    To make the names legal for Python enums, but also compliant with the REDCap form,
    classroom types starting with a number have an underscore prepended. and
    colons have been replaced with "COLON".
    """

    general_education = "1"
    integrated = "2"
    self_contained = "3"
    _12COLON1COLON1 = "4"
    _12COLON1COLON4 = "5"
    _8COLON1COLON1 = "6"
    other = "7"


class IndividualizedEducationProgram(enum.Enum):
    """The type of education program the patient is in."""

    no = "0"
    yes = "1"


class BirthDelivery(enum.Enum):
    """The type of delivery the patient had."""

    vaginal = "1"
    cesarean = "2"
    unknown = "3"


class DeliveryLocation(enum.Enum):
    """The location of the patient's birth."""

    hospital = "1"
    home = "2"
    other = "3"


class Adaptability(enum.Enum):
    """The adaptability of the patient during infancy."""

    easy = "1"
    difficult = "2"


class SoothingDifficulty(enum.Enum):
    """The difficulty of soothing the patient during infancy."""

    easy = "1"
    difficult = "2"


class EducationPerformance(enum.Enum):
    """Subjective performance in education."""

    excellent = "1"
    good = "2"
    satisfactory = "3"
    poor = "4"
    failing = "5"


class BirthComplications(enum.Enum):
    """The birth complications experienced by the patient."""

    spotting_or_vaginal_bleeding = "1"
    emotional_problems = "2"
    threatened_miscarriage = "3"
    diabetes = "4"
    high_blood_pressure = "5"
    pre_term_labor = "6"
    kidney_disease = "7"
    took_any_prescriptions = "8"
    drug_use = "9"
    alcohol_use = "10"
    tobacco_use = "11"
    swollen_ankles = "12"
    placenta_previa = "13"
    family_stress = "14"
    rh_or_other_incompatibilities = "15"
    flu_or_virus = "16"
    accident_or_injury = "17"
    bedrest = "18"
    other_illnesses = "19"
    none_of_the_above = "20"


class GuardianMaritalStatus(enum.Enum):
    """The marital status of the patient's guardian."""

    married = "1"
    domestic_partnership = "2"
    separated = "3"
    divorced = "4"
    never_married = "5"
    widowed = "6"


class HouseholdRelationship(enum.Enum):
    """The relationship of the patient to the head of the household."""

    mother = "1"
    father = "2"
    brother = "3"
    sister = "4"
    half_brother = "5"
    half_sister = "6"
    step_sister = "7"
    step_brother = "8"
    grandmother = "9"
    grandfather = "10"
    stepfather = "11"
    stepmother = "12"
    uncle = "13"
    aunt = "14"
    cousin = "15"
    nephew = "16"
    niece = "17"
    friend = "18"
    other_relative = "19"


class FriendshipQuality(enum.Enum):
    """Class used for the relationship quality with friends."""

    excellent = "1"
    good = "2"
    fair = "3"
    poor = "4"


class RelationshipQuality(enum.Enum):
    """The quality of the patient's relationship with a member of the household."""

    excellent = "1"
    good = "2"
    fair = "3"
    poor = "4"


class USState(enum.Enum):
    """The states of the United States of America."""

    Alabama = "1"
    Alaska = "2"
    Arizona = "3"
    Arkansas = "4"
    California = "5"
    Colorado = "6"
    Connecticut = "7"
    Delaware = "8"
    Florida = "9"
    Georgia = "10"
    Hawaii = "11"
    Idaho = "12"
    Illinois = "13"
    Indiana = "14"
    Iowa = "15"
    Kansas = "16"
    Kentucky = "17"
    Louisiana = "18"
    Maine = "19"
    Maryland = "20"
    Massachusetts = "21"
    Michigan = "22"
    Minnesota = "23"
    Mississippi = "24"
    Missouri = "25"
    Montana = "26"
    Nebraska = "27"
    Nevada = "28"
    New_Hampshire = "29"
    New_Jersey = "30"
    New_Mexico = "31"
    New_York = "32"
    North_Carolina = "33"
    North_Dakota = "34"
    Ohio = "35"
    Oklahoma = "36"
    Oregon = "37"
    Pennsylvania = "38"
    Rhode_Island = "39"
    South_Carolina = "40"
    South_Dakota = "41"
    Tennessee = "42"
    Texas = "43"
    Utah = "44"
    Vermont = "45"
    Virginia = "46"
    Washington = "47"
    West_Virginia = "48"
    Wisconsin = "49"
    Wyoming = "50"
    District_of_Columbia = "51"
    American_Samoa = "52"
    Guam = "53"
    Northern_Mariana_Islands = "54"
    Puerto_Rico = "55"
    US_Virgin_Islands = "56"


class Language(str, enum.Enum):
    """The languages spoken by the patient."""

    English = "1"
    Spanish = "2"
    Mandarin = "3"
    Cantonese = "4"
    French = "5"
    Haitian_Creole = "6"
    Russian = "7"
    Hebrew = "8"
    German = "9"
    Italian = "10"
    American_Sign_Language = "11"
    Portuguese = "12"
    Arabic = "13"
    Bulgarian = "14"
    Farsi = "15"
    Hindi = "16"
    Hmong = "17"
    Khmer = "18"
    Polish = "19"
    Somalian = "20"
    Tagalog = "21"
    Thai = "22"
    Urdu = "23"
    Vietnamese = "24"
    other = "25"


class LanguageFluency(enum.Enum):
    """The fluency of the patient in a language."""

    basic = "1"
    conversational = "2"
    proficient = "3"
    fluent = "4"


class HearingDevice(enum.Enum):
    """Whether the child has a hearing device."""

    no = "1"
    at_school_and_home = "2"
    at_home = "3"
    at_school = "4"


class Glasses(enum.Enum):
    """Whether the child has glasses."""

    no = "1"
    at_school_and_home = "2"
    at_home = "3"
    at_school = "4"


class EducationGrades(enum.Enum):
    """Grades in education."""

    As = "1"
    Bs = "2"
    Cs = "3"
    Ds = "4"
    Fs = "5"
    ONE = "6"
    TWO = "7"
    THREE = "8"
    FOUR = "9"
    not_graded = "10"


class PriorDisease(pydantic.BaseModel):
    """Class used for prior diseases in the Primary Care Information."""

    name: str
    was_positive: bool
    age: str | None
    treatment: str | None


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


class Intervention(pydantic.BaseModel):
    """Information about Early Intervention and CPSE services."""

    code: str
    name: str


interventions = {
    "1": Intervention(code="speechlang", name="speech and language therapy"),
    "2": Intervention(code="occ_therapy", name="occupational therapy"),
    "3": Intervention(code="phy_therapy", name="physical therapy"),
    "4": Intervention(code="seit", name="special education itinerant teacher"),
    "5": Intervention(code="aba", name="applied behavior analysis"),
    "6": Intervention(code="other", name="other"),
}


class EiCpseTherapy(pydantic.BaseModel):
    """Therapies from Committee on Preschool Special Education services."""

    type: Literal["early intervention", "cpse"]
    name: str
    duration: str
    dates: str


class FamilyDiagnosis(pydantic.BaseModel):
    """The model for a family diagnosis."""

    name: str
    checkbox_abbreviation: str
    text_abbreviation: str


family_psychiatric_diagnoses = [
    FamilyDiagnosis(
        name="attention deficit hyperactivity disorder",
        checkbox_abbreviation="adhd",
        text_abbreviation="adhd",
    ),
    FamilyDiagnosis(
        name="alcohol abuse",
        checkbox_abbreviation="aa",
        text_abbreviation="aa",
    ),
    FamilyDiagnosis(
        name="autism",
        checkbox_abbreviation="autism",
        text_abbreviation="autism",
    ),
    FamilyDiagnosis(
        name="bipolar disorder",
        checkbox_abbreviation="bipolar",
        text_abbreviation="bipolar",
    ),
    FamilyDiagnosis(
        name="conduct disorder",
        checkbox_abbreviation="conduct",
        text_abbreviation="conduct",
    ),
    FamilyDiagnosis(
        name="depression",
        checkbox_abbreviation="depression",
        text_abbreviation="depression",
    ),
    FamilyDiagnosis(
        name="disruptive mood dysregulation disorder",
        checkbox_abbreviation="dmdd",
        text_abbreviation="dmdd",
    ),
    FamilyDiagnosis(
        name="eating disorders",
        checkbox_abbreviation="eating",
        text_abbreviation="eating",
    ),
    FamilyDiagnosis(
        name="enuresis/encopresis",
        checkbox_abbreviation="enuresis_encopresis",
        text_abbreviation="ee",
    ),
    FamilyDiagnosis(
        name="excoriation",
        checkbox_abbreviation="excoriation",
        text_abbreviation="exco",
    ),
    FamilyDiagnosis(
        name="gender dysphoria",
        checkbox_abbreviation="gender",
        text_abbreviation="gender",
    ),
    FamilyDiagnosis(
        name="generalized anxiety disorder",
        checkbox_abbreviation="gad",
        text_abbreviation="genanx",
    ),
    FamilyDiagnosis(
        name="intellectual disability",
        checkbox_abbreviation="intellectual",
        text_abbreviation="id",
    ),
    FamilyDiagnosis(
        name="language disorder",
        checkbox_abbreviation="language_disorder",
        text_abbreviation="ld",
    ),
    FamilyDiagnosis(
        name="OCD",
        checkbox_abbreviation="ocd",
        text_abbreviation="ocd",
    ),
    FamilyDiagnosis(
        name="oppositional defiant disorder",
        checkbox_abbreviation="odd",
        text_abbreviation="odd",
    ),
    FamilyDiagnosis(
        name="panic disorder",
        checkbox_abbreviation="panic",
        text_abbreviation="panic",
    ),
    FamilyDiagnosis(
        name="personality disorder",
        checkbox_abbreviation="personality",
        text_abbreviation="personality",
    ),
    FamilyDiagnosis(
        name="psychosis",
        checkbox_abbreviation="psychosis",
        text_abbreviation="psychosis",
    ),
    FamilyDiagnosis(
        name="PTSD",
        checkbox_abbreviation="ptsd",
        text_abbreviation="ptsd",
    ),
    FamilyDiagnosis(
        name="reactive attachment",
        checkbox_abbreviation="rad",
        text_abbreviation="rad",
    ),
    FamilyDiagnosis(
        name="selective mutism",
        checkbox_abbreviation="selective_mutism",
        text_abbreviation="selective",
    ),
    FamilyDiagnosis(
        name="separation anxiety",
        checkbox_abbreviation="separation_anx",
        text_abbreviation="sa",
    ),
    FamilyDiagnosis(
        name="social anxiety",
        checkbox_abbreviation="social_anx",
        text_abbreviation="social",
    ),
    FamilyDiagnosis(
        name="specific learning disorder, with impairment in mathematics",
        checkbox_abbreviation="sld_math",
        text_abbreviation="sldmath",
    ),
    FamilyDiagnosis(
        name="specific learning disorder, with impairment in reading",
        checkbox_abbreviation="sld_read",
        text_abbreviation="sldread",
    ),
    FamilyDiagnosis(
        name="specific learning disorder, with impairment in written expression",
        checkbox_abbreviation="sld_write",
        text_abbreviation="sldexp",
    ),
    FamilyDiagnosis(
        name="specific phobias",
        checkbox_abbreviation="phobias",
        text_abbreviation="spho",
    ),
    FamilyDiagnosis(
        name="substance abuse",
        checkbox_abbreviation="substance",
        text_abbreviation="suba",
    ),
    FamilyDiagnosis(
        name="suicidality",
        checkbox_abbreviation="suicide",
        text_abbreviation="suicide",
    ),
    FamilyDiagnosis(
        name="tics/Tourette's",
        checkbox_abbreviation="tic_tourette",
        text_abbreviation="tt",
    ),
]


class PastDiagnosis(pydantic.BaseModel):
    """The model for the patient's past diagnosis."""

    diagnosis: str
    clinician: str
    age_at_diagnosis: str


class RedCapData(pydantic.BaseModel):
    """Validation for the REDcap data.

    The RedCap data is a bit messy with regards to typing. This model is a best-effort
    to type coerce and do some basic processing on the data or fail early for
    unexpected data.
    """

    adhd_text: str | None
    adhd___4: bool
    aa_text: str | None
    aa___4: bool
    autism_text: str | None
    autism___4: bool
    bipolar_text: str | None
    bipolar___4: bool
    conduct_text: str | None
    conduct___4: bool
    depression_text: str | None
    depression___4: bool
    dmdd_text: str | None
    dmdd___4: bool
    eating_text: str | None
    eating___4: bool
    ee_text: str | None
    enuresis_encopresis___4: bool
    exco_text: str | None
    excoriation___4: bool
    gender_text: str | None
    gender___4: bool
    genanx_text: str | None
    gad___4: bool
    id_text: str | None
    intellectual___4: bool
    ld_text: str | None
    language_disorder___4: bool
    ocd_text: str | None
    ocd___4: bool
    odd_text: str | None
    odd___4: bool
    panic_text: str | None
    panic___4: bool
    personality_text: str | None
    personality___4: bool
    psychosis_text: str | None
    psychosis___4: bool
    ptsd_text: str | None
    ptsd___4: bool
    rad_text: str | None
    rad___4: bool
    selective_text: str | None
    selective_mutism___4: bool
    sa_text: str | None
    separation_anx___4: bool
    social_text: str | None
    social_anx___4: bool
    sldmath_text: str | None
    sld_math___4: bool
    sldread_text: str | None
    sld_read___4: bool
    sldexp_text: str | None
    sld_write___4: bool
    spho_text: str | None
    phobias___4: bool
    suba_text: str | None
    substance___4: bool
    suicide_text: str | None
    suicide___4: bool
    tt_text: str | None
    tic_tourette___4: bool

    acs_exp: str | None
    age_1: str | None
    age_2: str | None
    age_3: str | None
    age_4: str | None
    age_5: str | None
    age_6: str | None
    age_7: str | None
    age_8: str | None
    age_9: str | None
    age_10: str | None
    age: float
    agress_exp: str | None
    biohx_dad_other: bool
    biohx_mom_other: bool
    birth_location: DeliveryLocation
    birth_other: str | None
    child_glasses: Glasses
    child_hearing_aid: HearingDevice
    child_interests: str
    child_language1: str | None
    child_language1_spoken: int | None
    child_language1_age: str | None
    child_language1_setting: str | None
    child_language1_fluency: LanguageFluency | None
    child_language2: str | None
    child_language2_spoken: int | None
    child_language2_age: str | None
    child_language2_setting: str | None
    child_language2_fluency: LanguageFluency | None
    child_language3: str | None
    child_language3_spoken: int | None
    child_language3_age: str | None
    child_language3_setting: str | None
    child_language3_fluency: LanguageFluency | None
    childgender_other: str | None
    childgender: Gender
    city: str
    classroomtype_other: str | None
    classroomtype: ClassroomType
    clinician: str | None
    close_friends: int
    concern_current: str
    cpse_services___1: bool
    cpse_services___2: bool
    cpse_services___3: bool
    cpse_services___4: bool
    cpse_services___5: bool
    cpse_services___6: bool
    csection_reason: str | None
    current_grades: EducationGrades
    currentdose_1: str | None
    currentdose_2: str | None
    currentdose_3: str | None
    currentdose_4: str | None
    currentdose_5: str | None
    dob: str
    dominant_hand: Handedness
    dose1_max_past: str | None
    dose1_start_past: str | None
    dose2_max_past: str | None
    dose2_start_past: str | None
    dose3_max_past: str | None
    dose3_start_past: str | None
    dose4_max_past: str | None
    dose_4_start_past: str | None
    dose5_max_past: str | None
    dose5_start_past: str | None
    dx_name1: str | None
    dx_name2: str | None
    dx_name3: str | None
    dx_name4: str | None
    dx_name5: str | None
    dx_name6: str | None
    dx_name7: str | None
    dx_name8: str | None
    dx_name9: str | None
    dx_name10: str | None
    encephalitis_age: str | None
    encephalitis_treatment: str | None
    encephalitis: bool
    firstname: str
    grade: str
    guardian_first_name: str
    guardian_last_name: str
    guardian_maritalstatus: GuardianMaritalStatus
    guardian_relationship___1: bool
    guardian_relationship___2: bool
    guardian_relationship___3: bool
    guardian_relationship___4: bool
    guardian_relationship___5: bool
    guardian_relationship___6: bool
    guardian_relationship___7: bool
    guardian_relationship___8: bool
    guardian_relationship___9: bool
    guardian_relationship___10: bool
    guardian_relationship___11: bool
    guardian_relationship___12: bool
    home_func: str
    iep: IndividualizedEducationProgram
    infanttemp_adapt: Adaptability
    infanttemp1: SoothingDifficulty
    language_other: str | None
    language_spoken_other: str | None
    language_spoken: Language
    language___1: bool
    language___2: bool
    language___3: bool
    language___4: bool
    language___5: bool
    language___6: bool
    language___7: bool
    language___8: bool
    language___9: bool
    language___10: bool
    language___11: bool
    language___12: bool
    language___13: bool
    language___14: bool
    language___15: bool
    language___16: bool
    language___17: bool
    language___18: bool
    language___19: bool
    language___20: bool
    language___21: bool
    language___22: bool
    language___23: bool
    language___24: bool
    language___25: bool
    lastname: str
    med1_past_date: str | None
    med1_past_doc: str | None
    med1_past_reason: str | None
    med1_past_se: str | None
    med2_past_date: str | None
    med2_past_doc: str | None
    med2_past_reason: str | None
    med2_past_se: str | None
    med3_past_date: str | None
    med3_past_doc: str | None
    med3_past_reason: str | None
    med3_past_se: str | None
    med4_past_date: str | None
    med4_past_doc: str | None
    med4_past_reason: str | None
    med4_past_se: str | None
    med5_past_date: str | None
    med5_past_doc: str | None
    med5_past_reason: str | None
    med5_past_se: str | None
    med1_start: str | None
    med1_reason: str | None
    med1_se: str | None
    med1_doc: str | None
    med2_start: str | None
    med2_current_reason: str | None
    med2_se: str | None
    med2_doc: str | None
    med3_start: str | None
    med3_reason: str | None
    med3_se: str | None
    med3_doc: str | None
    med4_date: str | None
    med4_reason: str | None
    med4_se: str | None
    med4_doc: str | None
    med5_date: str | None
    med5_reason: str | None
    med5_se: str | None
    med5_doc: str | None
    medname1_past: str | None
    medname2_past: str | None
    medname3_past: str | None
    medname4_past: str | None
    medname_5_past: str | None
    meningitis_age: str | None
    meningitis_treatment: str | None
    meningitis: bool
    migraines_age: str | None
    migraines_treatment: str | None
    migraines: bool
    opt_delivery: BirthDelivery
    other_relation: str | None
    othername: str | None
    outcome2: str
    pastdx_1: str | None
    pastdx_2: str | None
    pastdx_3: str | None
    pastdx_4: str | None
    pastdx_5: str | None
    pastdx_6: str | None
    pastdx_7: str | None
    pastdx_8: str | None
    pastdx_9: str | None
    pastdx_10: str | None
    past_psychmed_num: int | None
    pastschool1: str | None
    pastschool2: str | None
    pastschool3: str | None
    pastschool4: str | None
    pastschool5: str | None
    pastschool6: str | None
    pastschool7: str | None
    pastschool8: str | None
    pastschool9: str | None
    pastschool10: str | None
    pastschool1comments: str | None
    pastschool2comments: str | None
    pastschool3comments: str | None
    pastschool4comments: str | None
    pastschool5comments: str | None
    pastschool6comments: str | None
    pastschool7comments: str | None
    pastschool8comments: str | None
    pastschool9comments: str | None
    pastschool10comments: str | None
    pastschool1_grades: str | None
    pastschool2_grades: str | None
    pastschool3_grades: str | None
    pastschool4_grades: str | None
    pastschool5_grades: str | None
    pastschool6_grades: str | None
    pastschool7_grades: str | None
    pastschool8_grades: str | None
    pastschool9_grades: str | None
    pastschool10_grades: str | None
    peer_relations: FriendshipQuality
    peopleinhome1: str | None
    peopleinhome1_age: str | None
    peopleinhome1_relation: HouseholdRelationship | None
    peopleinhome1_relation_other: str | None
    peopleinhome1_relationship: RelationshipQuality | None
    peopleinhome2: str | None
    peopleinhome2_age: str | None
    peopleinhome2_relation: HouseholdRelationship | None
    peopleinhome2_relation_other: str | None
    peopleinhome_relationship: RelationshipQuality | None
    peopleinhome3: str | None
    peopleinhome3_age: str | None
    peopleinhome3_relation: HouseholdRelationship | None
    peopleinhome3_relation_other: str | None
    peopleinhome3_relationship: RelationshipQuality | None
    peopleinhome4: str | None
    peopleinhome4_age: str | None
    peopleinhome4_relation: HouseholdRelationship | None
    peopleinhome4_relation_other: str | None
    peopleinhome4_relationship: RelationshipQuality | None
    peopleinhome5: str | None
    peopleinhome5_age: str | None
    peopleinhome5_relation: HouseholdRelationship | None
    peopleinhome5_relation_other: str | None
    peopleinhome5_relationship: RelationshipQuality | None
    peopleinhome6: str | None
    peopleinhome6_age: str | None
    peopleinhome6_relation: HouseholdRelationship | None
    peopleinhome6_relation_other: str | None
    peopleinhome6_relationship: RelationshipQuality | None
    peopleinhome7: str | None
    peopleinhome7_age: str | None
    peopleinhome7_relation: HouseholdRelationship | None
    peopleinhome7_relation_other: str | None
    peopleinhome7_relationship: RelationshipQuality | None
    peopleinhome8: str | None
    peopleinhome8_age: str | None
    peopleinhome8_relation: HouseholdRelationship | None
    peopleinhome8_relation_other: str | None
    peopleinhome8_relationship: RelationshipQuality | None
    peopleinhome9: str | None
    peopleinhome9_age: str | None
    peopleinhome9_relation: HouseholdRelationship | None
    peopleinhome9_relation_other: str | None
    peopleinhome9_relationship: RelationshipQuality | None
    peopleinhome10: str | None
    peopleinhome10_age: str | None
    peopleinhome10_relation: HouseholdRelationship | None
    peopleinhome10_relation_other: str | None
    peopleinhome10_relationship: RelationshipQuality | None
    peopleinhome1_gradeocc: str | None
    peopleinhome2_gradeocc: str | None
    peopleinhome3_gradeocc: str | None
    peopleinhome4_gradeocc: str | None
    peopleinhome5_gradeocc: str | None
    peopleinhome6_gradeocc: str | None
    peopleinhome7_gradeocc: str | None
    peopleinhome8_gradeocc: str | None
    peopleinhome9_gradeocc: str | None
    peopleinhome10_gradeocc: str | None
    phone: str
    preg_symp___1: bool
    preg_symp___2: bool
    preg_symp___3: bool
    preg_symp___4: bool
    preg_symp___5: bool
    preg_symp___6: bool
    preg_symp___7: bool
    preg_symp___8: bool
    preg_symp___9: bool
    preg_symp___10: bool
    preg_symp___11: bool
    preg_symp___12: bool
    preg_symp___13: bool
    preg_symp___14: bool
    preg_symp___15: bool
    preg_symp___16: bool
    preg_symp___17: bool
    preg_symp___18: bool
    preg_symp___19: bool
    preg_symp___20: bool
    pregnancyhistory: str
    premature_specify: str | None
    premature: bool
    pronouns_other: str | None
    pronouns: Pronouns
    psychmed_name_1: str | None
    psychmed_name_2: str | None
    psychmed_name_3: str | None
    psychmed_name_4: str | None
    psychmed_name_5: str | None
    psychmed_num: int | None
    recent_academicperformance: EducationPerformance
    referral2: str
    residing_number: int
    school_func: str
    school: str
    schoolservices___1: bool
    schoolservices___2: bool
    schoolservices___3: bool
    schoolservices___4: bool
    schoolservices___5: bool
    schoolservices___6: bool
    schooltype: SchoolType
    seizures_age: str | None
    seizures_treatment: str | None
    seizures: bool
    selfharm_exp: str | None
    skill12: str
    skill13: str
    skill16: str
    skill6: str
    startdose_1: str | None
    startdose_2: str | None
    startdose_3: str | None
    startdose_4: str | None
    startdose_5: str | None
    state: USState
    txhx1_effectiveness: str | None
    txhx1_end: str | None
    txhx1_freq: str | None
    txhx1_reason: str | None
    txhx1_start: str | None
    txhx1_terminate: str | None
    txhx_1: str | None
    txhx2_effectiveness: str | None
    txhx2_end: str | None
    txhx2_freq: str | None
    txhx2_reason: str | None
    txhx2_start: str | None
    txhx2_terminate: str | None
    txhx2: str | None
    txhx3_effectiveness: str | None
    txhx3_end: str | None
    txhx3_freq: str | None
    txhx3_reason: str | None
    txhx3_start: str | None
    txhx3_terminate: str | None
    txhx_3: str | None
    txhx4_effectiveness: str | None
    txhx4_end: str | None
    txhx4_freq: str | None
    txhx4_reason: str | None
    txhx4_start: str | None
    txhx4_terminate: str | None
    txhx_4: str | None
    txhx5_effectiveness: str | None
    txhx5_end: str | None
    txhx5_freq: str | None
    txhx5_reason: str | None
    txhx5_start: str | None
    txhx5_terminate: str | None
    txhx_5: str | None
    txhx6_effectiveness: str | None
    txhx6_end: str | None
    txhx6_freq: str | None
    txhx6_reason: str | None
    txhx6_start: str | None
    txhx6_terminate: str | None
    txhx_6: str | None
    txhx7_effectiveness: str | None
    txhx7_end: str | None
    txhx7_freq: str | None
    txhx7_reason: str | None
    txhx7_start: str | None
    txhx7_terminate: str | None
    txhx_7: str | None
    txhx8_effectiveness: str | None
    txhx8_end: str | None
    txhx8_freq: str | None
    txhx8_reason: str | None
    txhx8_start: str | None
    txhx8_terminate: str | None
    txhx_8: str | None
    txhx9_effectiveness: str | None
    txhx9_end: str | None
    txhx9_freq: str | None
    txhx9_reason: str | None
    txhx9_start: str | None
    txhx9_terminate: str | None
    txhx_9: str | None
    txhx10_effectiveness: str | None
    txhx10_end: str | None
    txhx10_freq: str | None
    txhx10_reason: str | None
    txhx10_start: str | None
    txhx10_terminate: str | None
    txhx_10: str | None
    txt_duration_preg_num: str
    violence_exp: str | None
    yrs_school: int
    speechlang_dates: str | None
    speechlang_dur: str | None
    occ_therapy_dates: str | None
    occ_therapy_dur: str | None
    phy_therapy_dates: str | None
    phy_therapy_dur: str | None
    seit_dates: str | None
    seit_dur: str | None
    aba_dates: str | None
    aba_dur: str | None
    other_dates: str | None
    other_dur: str | None

    @classmethod
    def from_csv(cls, csv_data: str) -> Self:
        """Creates a RedCapData object from a CSV string."""
        reader = csv.DictReader(io.StringIO(csv_data))
        data = next(reader)
        return cls(**data)

    @pydantic.model_validator(mode="before")
    @classmethod
    def set_empty_strings_to_none(
        cls,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        """Sets empty strings to None."""
        for key, value in data.items():
            if value == "":
                data[key] = None
        return data

    @pydantic.field_validator(
        *(
            [f"schoolservices___{index}" for index in range(1, 7)]
            + [f"cpse_services___{index}" for index in range(1, 7)]
            + [f"preg_symp___{index}" for index in range(1, 21)]
            + [f"guardian_relationship___{index}" for index in range(1, 13)]
            + [f"language___{index}" for index in range(1, 26)]
            + [
                "biohx_dad_other",
                "biohx_mom_other",
                "seizures",
                "migraines",
                "meningitis",
                "encephalitis",
            ]
            + [
                f"{diag.checkbox_abbreviation}___4"
                for diag in family_psychiatric_diagnoses
            ]
        ),
        mode="before",
    )
    @classmethod
    def interpret_string_as_bool(cls, v: str) -> bool:
        """Interprets a 0/1 string as a boolean.

        Args:
            v: The value to interpret.

        Returns:
            True if v is "1", False if v is "0".

        Raises:
            ValueError: If v is not "0" or "1".
        """
        if v == "0":
            return False
        if v == "1":
            return True
        msg = f"Expected 0 or 1, got {v}."
        raise ValueError(msg)

    # Interpret family diagnoses

    @property
    def family_diagnoses(self) -> list[FamilyPsychiatricHistory]:
        """The family psychiatric diagnoses."""
        return [
            FamilyPsychiatricHistory(
                diagnosis=diag.name,
                no_formal_diagnosis=getattr(self, f"{diag.checkbox_abbreviation}___4"),
                family_members=getattr(self, f"{diag.text_abbreviation}_text"),
            )
            for diag in family_psychiatric_diagnoses
        ]

    # Interpret multi-column booleans

    @property
    def cpse_services(self) -> list[EiCpseTherapy]:
        """The CPSE services."""
        return [
            EiCpseTherapy(
                name=service.name,
                type="cpse",
                dates=getattr(self, f"{service.code}_dates"),
                duration=getattr(self, f"{service.code}_dur"),
            )
            for index, service in enumerate(interventions.values())
            if getattr(self, f"cpse_services___{index+1}")
        ]

    @property
    def early_intervention(self) -> list[EiCpseTherapy]:
        """The early intervention therapies."""
        return [
            EiCpseTherapy(
                name=service.name,
                type="early intervention",
                dates=getattr(self, f"{service.code}_dates"),
                duration=getattr(self, f"{service.code}_dur"),
            )
            for index, service in enumerate(interventions.values())
            if getattr(self, f"schoolservices___{index+1}")
        ]

    @property
    def guardian_relationship(self) -> GuardianRelationship:
        """The relationship of the patient to the head of the household."""
        for index in range(1, 13):
            if getattr(self, f"guardian_relationship___{index}"):
                return GuardianRelationship(index)
        msg = "No guardian relationship found."
        raise ValueError(msg)

    @property
    def household_languages(self) -> list[Language]:
        """The languages spoken by the patient."""
        household_languages = [
            Language(str(index))
            for index in range(1, 25)
            if getattr(self, f"language___{index}")
        ]
        if self.language_other:
            household_languages.append(Language.other)
        return household_languages

    @property
    def preg_symp(self) -> list[BirthComplications]:
        """The pregnancy symptoms."""
        return [
            BirthComplications(index)
            for index in range(1, 21)
            if getattr(self, f"preg_symp___{index}")
        ]

    # Aliases

    @property
    def peopleinhome2_relationship(self) -> RelationshipQuality | None:
        """The relationship of the second person in the home.

        Alias used to make the name conform to the other peopleinhome#_relationship
        names.
        """
        return self.peopleinhome_relationship

    @property
    def txhx_2(self) -> str | None:
        """The second treatment history.

        Alias used to make the name conform to the other txhx_# names.
        """
        return self.txhx2

    @property
    def med2_reason(self) -> str | None:
        """The reason for the second medication.

        Alias used to make the name conform to the other med#_reason names.
        """
        return self.med2_current_reason

    @property
    def medname5_past(self) -> str | None:
        """The name of the fifth past medication.

        Alias used to make the name conform to the other medname#_past names.
        """
        return self.medname_5_past

    @property
    def med4_start(self) -> str | None:
        """The start date of the fourth medication.

        Alias used to make the name conform to the other med#_start names.
        """
        return self.med4_date

    @property
    def med5_start(self) -> str | None:
        """The start date of the fifth medication.

        Alias used to make the name conform to the other med#_start names.
        """
        return self.med5_date

    @property
    def dose4_start_past(self) -> str | None:
        """The start date of the fourth dose.

        Alias used to make the name conform to the other dose#_start_past names.
        """
        return self.dose_4_start_past


def get_intake_data(mrn: str) -> RedCapData:
    """Gets the intake data from REDcap.

    REDCap does not allow filtering by redcap_survey_identifier, so we have to
    download all records, find the associated record_id, and then filter by that.

    REDCap survey identifiers occasionally get strings appended. We search only for
    five consecutive numbers.


    Args:
        mrn: The patient's MRN (unique identifier).

    Returns:
        The intake data for the survey.
    """
    if not re.match(r"^\d{5}$", mrn):
        msg = "MRN must be five consecutive numbers."
        raise exceptions.RedcapError(msg)

    logger.debug("Getting intake data for MRN %s.", mrn)
    project = redcap.Project(str(REDCAP_ENDPOINT), REDCAP_API_TOKEN.get_secret_value())  # type: ignore[attr-defined]
    redcap_fields = project.export_records(
        format_type="csv",
        fields=["firstname"],
        export_survey_fields=True,
        raw_or_label="label",
    )

    redcap_fields = csv.DictReader(io.StringIO(redcap_fields))
    record_ids = [
        row["record_id"]
        for row in redcap_fields
        if row["redcap_survey_identifier"].find(mrn) != -1
    ]

    if len(record_ids) == 0:
        msg = "No record found for the given MRN."
        raise exceptions.RedcapError(msg)

    patient_data: str = project.export_records(
        format_type="csv",
        export_survey_fields=True,
        records=[record_ids[0]],
    )

    return RedCapData.from_csv(patient_data)
