"""Contains descriptors of the columns of the REDCap intake form."""

import enum

import pydantic


class Gender(enum.Enum):
    """The gender of the patient."""

    male = 0
    female = 1
    non_binary = 2
    transgender_male = 3
    transgender_female = 4
    other = 5


class Pronouns(enum.Enum):
    """The pronouns of the patient."""

    he_him_his_his_himself = 0
    she_her_her_hers_herself = 1
    they_them_their_theirs_themselves = 2
    ze_zir_zir_zirs_zirself = 3
    other = 4


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


class Handedness(enum.Enum):
    """The dominant hand of the patient."""

    left = 1
    right = 2
    unknown = 3


class SchoolType(enum.Enum):
    """The type of school the patient attends."""

    boarding = 1
    home = 2
    parochial = 3
    private = 4
    public = 5
    special = 6
    vocational = 7
    charter = 8
    other = 9


class ClassroomType(enum.Enum):
    """The type of classroom the patient is in.

    To make the names legal for Python enums, but also compliant with the REDCap form,
    classroom types starting with a number have an underscore prepended. and
    colons have been replaced with "COLON".
    """

    general_education = 1
    integrated = 2
    self_contained = 3
    _12COLON1COLON1 = 4
    _12COLON1COLON4 = 5
    _8COLON1COLON1 = 6
    other = 7


class IndividualizedEducationProgram(enum.Enum):
    """The type of education program the patient is in."""

    no = 0
    yes = 1


class BirthDelivery(enum.Enum):
    """The type of delivery the patient had."""

    vaginal = 1
    cesarean = 2
    unknown = 3


class DeliveryLocation(enum.Enum):
    """The location of the patient's birth."""

    hospital = 1
    home = 2
    other = 3


class Adaptability(enum.Enum):
    """The adaptability of the patient during infancy."""

    easy = 1
    difficult = 2


class SoothingDifficulty(enum.Enum):
    """The difficulty of soothing the patient during infancy."""

    easy = 1
    difficult = 2


class BirthComplications(enum.Enum):
    """The birth complications experienced by the patient."""

    spotting_or_vaginal_bleeding = 1
    emotional_problems = 2
    threatened_miscarriage = 3
    diabetes = 4
    high_blood_pressure = 5
    pre_term_labor = 6
    kidney_disease = 7
    took_any_prescriptions = 8
    drug_use = 9
    alcohol_use = 10
    tobacco_use = 11
    swollen_ankles = 12
    placenta_previa = 13
    family_stress = 14
    rh_or_other_incompatibilities = 15
    flu_or_virus = 16
    accident_or_injury = 17
    bedrest = 18
    other_illnesses = 19
    none_of_the_above = 20


class GuardianMaritalStatus(enum.Enum):
    """The marital status of the patient's guardian."""

    married = 1
    domestic_partnership = 2
    separated = 3
    divorced = 4
    never_married = 5
    widowed = 6


class HouseholdRelationship(enum.Enum):
    """The relationship of the patient to the head of the household."""

    mother = 1
    father = 2
    brother = 3
    sister = 4
    half_brother = 5
    half_sister = 6
    step_sister = 7
    step_brother = 8
    grandmother = 9
    grandfather = 10
    stepfather = 11
    stepmother = 12
    uncle = 13
    aunt = 14
    cousin = 15
    nephew = 16
    niece = 17
    friend = 18
    other_relative = 19


class RelationshipQuality(enum.Enum):
    """The quality of the patient's relationship with a member of the household."""

    excellent = 1
    good = 2
    fair = 3
    poor = 4


class USState(enum.Enum):
    """The states of the United States of America."""

    Alabama = 1
    Alaska = 2
    Arizona = 3
    Arkansas = 4
    California = 5
    Colorado = 6
    Connecticut = 7
    Delaware = 8
    Florida = 9
    Georgia = 10
    Hawaii = 11
    Idaho = 12
    Illinois = 13
    Indiana = 14
    Iowa = 15
    Kansas = 16
    Kentucky = 17
    Louisiana = 18
    Maine = 19
    Maryland = 20
    Massachusetts = 21
    Michigan = 22
    Minnesota = 23
    Mississippi = 24
    Missouri = 25
    Montana = 26
    Nebraska = 27
    Nevada = 28
    New_Hampshire = 29
    New_Jersey = 30
    New_Mexico = 31
    New_York = 32
    North_Carolina = 33
    North_Dakota = 34
    Ohio = 35
    Oklahoma = 36
    Oregon = 37
    Pennsylvania = 38
    Rhode_Island = 39
    South_Carolina = 40
    South_Dakota = 41
    Tennessee = 42
    Texas = 43
    Utah = 44
    Vermont = 45
    Virginia = 46
    Washington = 47
    West_Virginia = 48
    Wisconsin = 49
    Wyoming = 50
    District_of_Columbia = 51
    American_Samoa = 52
    Guam = 53
    Northern_Mariana_Islands = 54
    Puerto_Rico = 55
    US_Virgin_Islands = 56


class Language(enum.Enum):
    """The languages spoken by the patient."""

    English = 1
    Spanish = 2
    Mandarin = 3
    Cantonese = 4
    French = 5
    Haitian_Creole = 6
    Russian = 7
    Hebrew = 8
    German = 9
    Italian = 10
    American_Sign_Language = 11
    Portuguese = 12
    Arabic = 13
    Bulgarian = 14
    Farsi = 15
    Hindi = 16
    Hmong = 17
    Khmer = 18
    Polish = 19
    Somalian = 20
    Tagalog = 21
    Thai = 22
    Urdu = 23
    Vietnamese = 24
    other = 25


class LanguageFluency(enum.Enum):
    """The fluency of the patient in a language."""

    basic = 1
    conversational = 2
    proficient = 3
    fluent = 4


class PastDiagnosis(pydantic.BaseModel):
    """The model for the patient's past diagnosis."""

    diagnosis: str
    clinician: str
    age: str


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
        name="suicide",
        checkbox_abbreviation="suicide",
        text_abbreviation="suicide",
    ),
    FamilyDiagnosis(
        name="tics/Tourette's",
        checkbox_abbreviation="tic_tourette",
        text_abbreviation="tt",
    ),
]
