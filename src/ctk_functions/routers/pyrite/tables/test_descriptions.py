import dataclasses


@dataclasses.dataclass
class TestDescription:
    """Protocol defining what's required to use the WordTableSectionAppendixAMixin."""

    title: str
    description: str
    reference: str


class TestDescriptionManager:
    def __init__(self) -> None:
        self.cbcl = TestDescription(
            title="Child Behavior Checklist (CBCL)",
            description=(
                "The CBCL is a questionnaire on which parents rate a child's problem "
                "behaviors and competencies. The CBCL also obtains parents’ reports of "
                "the amount and quality of their child’s participation in sports, "
                "hobbies, games, activities, organizations, jobs and chores, "
                "friendships, how well the child gets along with others and plays and "
                "works by himself, and school functioning."
            ),
            reference=(
                "Achenbach, T. M. (1991). Integrative Guide to the CBCL/4-18, YSR, and "
                "TRF Profiles. Burlington, VT: University of Vermont, Department of "
                "Psychology."
            ),
        )

        self.conners_3 = TestDescription(
            title="Conners’ ADHD Rating Scale (Conners)",
            description=(
                "The Conners is a questionnaire that uses child and adolescent self-report "
                "ratings to assess symptoms of attention deficit/hyperactivity disorder (ADHD) "
                "and evaluate problem behavior in children and adolescents."
            ),
            reference=(
                "Conners, C. K. (2001). Conners’ Rating Scales-Revised. North Tonawanda, NY: "
                "Multi-Health Systems, Inc."
            ),
        )

        self.ctopp_2 = TestDescription(
            title=(
                "Comprehensive Test of Phonological Processing - Second Edition (CTOPP - 2)"
            ),
            description=(
                "The CTOPP - 2 is an assessment of reading related phonological "
                "processing skills including fluency."
            ),
            reference=(
                "Wagner, R. K., Torgesen, J. K., Rashotte, C. A., & Pearson, N. A. "
                "(2013). Comprehensive test of phonological processing–second edition. "
                "Canadian Journal of School Psychology."
            ),
        )

        self.grooved_pegboard = TestDescription(
            title="Lafayette Grooved Pegboard Test",
            description=(
                "The Grooved Pegboard is a manipulative dexterity test. This unit "
                "consists of 25 holes with randomly positioned slots. Pegs, which "
                "have a key along one side, must be rotated to match the hole before "
                "the can be inserted."
            ),
            reference=(
                "Lafayette Instrument Company (1989). Grooved Pegboard: Owner’s "
                "Manual. Lafayette, IN: Lafayette Instrument Company."
            ),
        )

        self.mfq = TestDescription(
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

        self.scared = TestDescription(
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

        self.srs = TestDescription(
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

        self.eswan = TestDescription(
            title=(
                "Extended Strengths and Weaknesses of Attention-Deficit/Hyperactivity Disorder "
                "Symptoms and Normal Behavior Scale (ESWAN)"
            ),
            description=(
                "The ESWAN is parent-report questionnaire that assesses symptoms of attention "
                "deficit/hyperactivity disorder (ADHD) and evaluates problem behavior in "
                "children and adolescents."
            ),
            reference=(
                "Swanson, J. M., et al. (2006). Categorical and dimensional definitions and "
                "evaluations of symptoms of ADHD: The SNAP and SWAN Rating Scales. Available "
                "from http://www.ADHD.net."
            ),
        )

        self.towre_2 = TestDescription(
            title="Test of Word Reading Efficiency - Second Edition (TOWRE - 2)",
            description=(
                "The TOWRE - 2 efficiently assesses two important components of the reading "
                "process: sight word reading and phonetic decoding."
            ),
            reference=(
                "Torgesen, J. K., Wagner, R. K., & Rashotte, C. A. (2012). Test of Word "
                "Reading Efficiency"
            ),
        )

        self.wiat_4 = TestDescription(
            title="Wechsler Individual Achievement Test - 4th Edition (WIAT - 4)",
            description=(
                "The WIAT -4 is a clinician-administered measurement tool useful for academic "
                "achievement skills assessment, learning disability diagnosis, special "
                "education placement, and clinical appraisal."
            ),
            reference=(
                "NCS Pearson. (2020). Wechsler Individual Achievement Test, 4th Ed. Bloomington: Author."
            ),
        )

        self.wisc_5 = TestDescription(
            title="Wechsler Intelligence Scale for Children - V (WISC - V)",
            description=(
                "The WISC-V is a measure of general intellectual ability for children age 6 "
                "to 16 years. Seven subtests are used to calculate a Full Scale IQ, and ten "
                "subtests are used to calculate indices of verbal reasoning (VCI), non-verbal "
                "reasoning (VSI, FRI), working memory (WMI), and processing speed (PSI)."
            ),
            reference=(
                "Wechsler, D. (2014). Wechsler Intelligence Scale for Children-Fifth Edition "
                "(WISC-V). San Antonio, TX: NCS Pearson."
            ),
        )
