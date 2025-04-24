"""Descriptions of the HBN tests for Appendix A."""

from typing import Literal, cast

import pydantic

TestId = Literal[
    "asr",
    "cbcl",
    "celf_5",
    "conners_3",
    "ctopp_2",
    "grooved_pegboard",
    "mfq",
    "scared",
    "srs",
    "swan",
    "towre_2",
    "trf",
    "wiat_4",
    "wisc_5",
    "ysr",
]


@pydantic.dataclasses.dataclass
class TestDescription:
    """Definition of the Appendix A description of a test."""

    id: TestId
    title: str
    description: str
    reference: str


@pydantic.dataclasses.dataclass
class TestDescriptionManager:
    """Dataclass for all test descriptions."""

    def fetch(self, test_id: TestId) -> TestDescription:
        """Convenience method that mimics getattr with correct typing."""
        return cast("TestDescription", getattr(self, test_id))

    asr = TestDescription(
        id="asr",
        title="Adult Self-Report (ASR)",
        description=(
            "The ASR is a questionnaire on which individuals rate their own problem "
            "behaviors and competencies. The ASR also obtains reports of the amount "
            "and quality of participation in sports, hobbies, games, activities, "
            "organizations, jobs and chores, friendships, how well the individual gets "
            "along with others and works by themselves."
        ),
        reference=(
            "Achenbach, T. M., & Rescorla, L. A. (2003). Manual for the ASEBA adult "
            "forms & profiles. Burlington: University of Vermont, Research Center for "
            "Children, Youth, and Families. "
        ),
    )

    cbcl = TestDescription(
        id="cbcl",
        title="Child Behavior Checklist (CBCL)",
        description=(
            "The CBCL is a questionnaire on which parents rate a child's problem "
            "behaviors and competencies. The CBCL also obtains parents' reports of "
            "the amount and quality of their child's participation in sports, "
            "hobbies, games, activities, organizations, jobs and chores, "
            "friendships, how well the child gets along with others and plays and "
            "works by himself, and school functioning."
        ),
        reference=(
            "Achenbach, T. M., & Rescorla, L. A. (2001). Manual for the ASEBA "
            "school-age forms & profiles. Burlington: University of Vermont, Research "
            "Center for Children, Youth, and Families."
        ),
    )

    celf_5 = TestDescription(
        id="celf_5",
        title=(
            "Clinical Evaluation of Language Fundamentals - Fifth Edition Screener "
            "(CELF-5)"
        ),
        description=(
            "The CELF-5 screener is a brief measure of basic aspects of "
            "language, including morphology, syntax, semantics, and pragmatics."
        ),
        reference=(
            "Semel, E., Wiig, E. H., & Secord, W. A. (2013). Clinical Evaluation of "
            "Language Fundamentals: Screening Test (5th ed.) Bloomington, MN: Pearson."
        ),
    )

    conners_3 = TestDescription(
        id="conners_3",
        title="Conners' ADHD Rating Scale (Conners)",
        description=(
            "The Conners is a questionnaire that uses child and adolescent self-report "
            "ratings to assess symptoms of attention deficit/hyperactivity disorder "
            "(ADHD) and evaluate problem behavior in children and adolescents."
        ),
        reference=(
            "Conners, C. K. (2001). Conners' Rating Scales-Revised. North Tonawanda, "
            "NY: Multi-Health Systems, Inc."
        ),
    )

    ctopp_2 = TestDescription(
        id="ctopp_2",
        title=(
            "Comprehensive Test of Phonological Processing - Second Edition (CTOPP - 2)"
        ),
        description=(
            "The CTOPP - 2 is an assessment of reading related phonological "
            "processing skills including fluency."
        ),
        reference=(
            "Wagner, R. K., Torgesen, J. K., Rashotte, C. A., & Pearson, N. A. "
            "(2013). Comprehensive test of phonological processing-second edition. "
            "Canadian Journal of School Psychology."
        ),
    )

    grooved_pegboard = TestDescription(
        id="grooved_pegboard",
        title="Lafayette Grooved Pegboard Test",
        description=(
            "The Grooved Pegboard is a manipulative dexterity test. This unit "
            "consists of 25 holes with randomly positioned slots. Pegs, which "
            "have a key along one side, must be rotated to match the hole before "
            "the can be inserted."
        ),
        reference=(
            "Lafayette Instrument Company (1989). Grooved Pegboard: Owner's "
            "Manual. Lafayette, IN: Lafayette Instrument Company."
        ),
    )

    mfq = TestDescription(
        id="mfq",
        title="Mood and Feelings Questionnaire (MFQ)",
        description=(
            "The MFQ consists of a series of descriptive phrases for children and "
            "their parents to report on mood and depressive symptoms currently and "
            "in the past."
        ),
        reference=(
            "Angold, A., Costello, E. J., Messer, S. C., Pickles, A., Winder, F., "
            "& Silver, D. (1995) The development of a short questionnaire for use "
            "in epidemiological studies of depression in children and adolescents. "
            "International Journal of Methods in Psychiatric Research, 5, 237 - "
            "249."
        ),
    )

    scared = TestDescription(
        id="scared",
        title="Screen for Child Anxiety Related Disorders (SCARED)",
        description=(
            "The SCARED is a self- and parent-report measure of symptoms of "
            "anxiety-related disorders among children and adolescents, including "
            "general anxiety disorder, separation anxiety disorder, panic "
            "disorder, and social phobia. In addition, the SCARED assesses "
            "symptoms related to school phobias."
        ),
        reference=(
            "Birmaher, B., et al.  (1999). Psychometric properties of the Screen "
            "for Child Anxiety Related Emotional Disorders (SCARED): a replication "
            "study. Journal of the American Academy of Child and Adolescent "
            "Psychiatry, 38(10), 1230-1236."
        ),
    )

    srs = TestDescription(
        id="srs",
        title="Social Responsiveness Scale-2 (SRS-2)",
        description=(
            "The SRS-2 is a parent-report measure of the various dimensions of "
            "interpersonal behavior, communication, and repetitive/stereotypic "
            "behavior characteristic of autism spectrum disorders."
        ),
        reference=(
            "Constantino, J. N. & Gruber, C. P. (2012). The Social Responsiveness "
            "Scale Manual, Second Edition (SRS-2). Los Angeles, CA: Western "
            "Psychological Services."
        ),
    )

    swan = TestDescription(
        id="swan",
        title=(
            "Extended Strengths and Weaknesses of Attention-Deficit/Hyperactivity "
            "Disorder Symptoms and Normal Behavior Scale (ESWAN)"
        ),
        description=(
            "The ESWAN is parent-report questionnaire that assesses symptoms of "
            "attention deficit/hyperactivity disorder (ADHD) and evaluates problem "
            "behavior in children and adolescents."
        ),
        reference=(
            "Swanson, J. M., et al. (2006). Categorical and dimensional definitions "
            "and evaluations of symptoms of ADHD: The SNAP and SWAN Rating Scales. "
            "Available from http://www.ADHD.net."
        ),
    )

    towre_2 = TestDescription(
        id="towre_2",
        title="Test of Word Reading Efficiency - Second Edition (TOWRE - 2)",
        description=(
            "The TOWRE - 2 efficiently assesses two important components of the "
            "reading process: sight word reading and phonetic decoding."
        ),
        reference=(
            "Torgesen, J. K., Wagner, R. K., & Rashotte, C. A. (2012). Test of Word "
            "Reading Efficiency"
        ),
    )

    trf = TestDescription(
        id="trf",
        title="Teacher Report Form (TRF)",
        description=(
            "The TRF is a questionnaire on which teachers rate a child's problem "
            "behaviors and competencies in the school setting. The TRF also obtains "
            "qualitative reports of academic functioning."
        ),
        reference=(
            "Achenbach, T. M., & Rescorla, L. A. (2001). Manual for the ASEBA "
            "school-age forms & profiles. Burlington: University of Vermont, Research "
            "Center for Children, Youth, and Families."
        ),
    )

    wiat_4 = TestDescription(
        id="wiat_4",
        title="Wechsler Individual Achievement Test - 4th Edition (WIAT - 4)",
        description=(
            "The WIAT -4 is a clinician-administered measurement tool useful for "
            "academic achievement skills assessment, learning disability diagnosis, "
            "special education placement, and clinical appraisal."
        ),
        reference=(
            "NCS Pearson. (2020). Wechsler Individual Achievement Test, 4th Ed. "
            "Bloomington: Author."
        ),
    )

    wisc_5 = TestDescription(
        id="wisc_5",
        title="Wechsler Intelligence Scale for Children - V (WISC - V)",
        description=(
            "The WISC-V is a measure of general intellectual ability for children age "
            "6 to 16 years. Seven subtests are used to calculate a Full Scale IQ, and "
            "ten subtests are used to calculate indices of verbal reasoning (VCI), "
            "non-verbal reasoning (VSI, FRI), working memory (WMI), and processing "
            "speed (PSI)."
        ),
        reference=(
            "Wechsler, D. (2014). Wechsler Intelligence Scale for Children-Fifth "
            "Edition (WISC-V). San Antonio, TX: NCS Pearson."
        ),
    )

    ysr = TestDescription(
        id="ysr",
        title="Youth Self Report (YSR)",
        description=(
            "The YSR is a questionnaire on which children rate their own "
            "problem behaviors and competencies. The YSR also obtains self reports of "
            "the amount and quality of participation in sports, hobbies, games, "
            "activities, organizations, jobs and chores, friendships, how well the "
            "child gets along with others and plays and works by themself, and school "
            "functioning. "
        ),
        reference=(
            "Achenbach, T. M., & Rescorla, L. A. (2001). Manual for the ASEBA "
            "school-age forms & profiles. Burlington: University of Vermont, Research "
            "Center for Children, Youth, and Families. "
        ),
    )
