"""Definitions of the used tables in the SQL Database."""

import sqlalchemy
from sqlalchemy import orm


class Base(orm.DeclarativeBase):
    """Base class for all tables."""


class Wisc5(Base):
    """SQLAlchemy model representing I2B2_Export_WISC_V_t in the nextgen schema.

    This table stores Wechsler Intelligence Scale for Children (WISC-V) assessment data,
    including raw scores, scaled scores, indexes, and percentiles.
    """

    __tablename__ = "I2B2_Export_WISC_V_t"
    __table_args__ = {"schema": "nextgen"}  # noqa: RUF012

    URSI = orm.mapped_column(
        sqlalchemy.String(10, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )
    SiteID = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    RaterID = orm.mapped_column(
        sqlalchemy.String(4, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )
    SourceType = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    AssessmentStartDate = orm.mapped_column(
        sqlalchemy.String(10, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )
    AssessmentStartTime = orm.mapped_column(
        sqlalchemy.String(5, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )
    Successful = orm.mapped_column(
        sqlalchemy.String(1, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )
    EID = orm.mapped_column(
        sqlalchemy.String(15, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )
    START_DATE = orm.mapped_column(
        sqlalchemy.String(20, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=False,
        primary_key=True,
    )
    Study = orm.mapped_column(
        sqlalchemy.String(3, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )
    Site = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Days_Baseline = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Year = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Season = orm.mapped_column(
        sqlalchemy.String(6, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=False,
    )
    WISC_complete = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_incomplete_reason = orm.mapped_column(
        sqlalchemy.String(100, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )

    # Raw and Scaled Scores
    WISC_BD_Raw = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_BD_Scaled = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_Similarities_Raw = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_Similarities_Scaled = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_MR_Raw = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_MR_Scaled = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_DS_Raw = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_DS_Scaled = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_Coding_Raw = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_Coding_Scaled = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_Vocab_Raw = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_Vocab_Scaled = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_FW_Raw = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_FW_Scaled = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_VP_Raw = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_VP_Scaled = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_PS_Raw = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_PS_Scaled = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_SS_Raw = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_SS_Scaled = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Composite Scores - Visual Spatial Index
    WISC_VSI_Sum = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_VSI = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_VSI_Percentile = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)

    # Composite Scores - Verbal Comprehension Index
    WISC_VCI_Sum = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_VCI = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_VCI_Percentile = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)

    # Composite Scores - Fluid Reasoning Index
    WISC_FRI_Sum = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_FRI = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_FRI_Percentile = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)

    # Composite Scores - Working Memory Index
    WISC_WMI_Sum = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_WMI = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_WMI_Percentile = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)

    # Composite Scores - Processing Speed Index
    WISC_PSI_Sum = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_PSI = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_PSI_Percentile = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)

    # Full Scale IQ
    WISC_FSIQ_Sum = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_FSIQ = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_FSIQ_Percentile = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)


class Towre(Base):
    """SQLAlchemy model representing I2B2_Export_TOWRE_t in the nextgen schema.

    This table stores Test of Word Reading Efficiency (TOWRE) assessment data,
    including raw scores, scaled scores, percentiles, and age/grade equivalents.
    """

    __tablename__ = "I2B2_Export_TOWRE_t"
    __table_args__ = {"schema": "nextgen"}  # noqa: RUF012

    URSI = orm.mapped_column(
        sqlalchemy.String(10, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )
    SiteID = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    RaterID = orm.mapped_column(
        sqlalchemy.String(4, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )
    SourceType = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    AssessmentStartDate = orm.mapped_column(
        sqlalchemy.String(10, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )
    AssessmentStartTime = orm.mapped_column(
        sqlalchemy.String(5, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )
    Successful = orm.mapped_column(
        sqlalchemy.String(1, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )
    EID = orm.mapped_column(
        sqlalchemy.String(15, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )
    START_DATE = orm.mapped_column(
        sqlalchemy.String(20, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=False,
        primary_key=True,
    )
    Study = orm.mapped_column(
        sqlalchemy.String(3, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )
    Site = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Days_Baseline = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Year = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Season = orm.mapped_column(
        sqlalchemy.String(6, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=False,
    )
    TOWRE_Complete = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TOWRE_IncompleteReason = orm.mapped_column(
        sqlalchemy.String(100, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )
    TOWRE_Valid = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TOWRE_Invalid_Reason = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Phonemic Decoding Efficiency (PDE) scores
    TOWRE_PDE_Raw = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TOWRE_PDE_Scaled = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TOWRE_PDE_Perc = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    TOWRE_PDE_AE = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TOWRE_PDE_GE = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TOWRE_PDE_Desc = orm.mapped_column(
        sqlalchemy.String(20, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )

    # Sight Word Efficiency (SWE) scores
    TOWRE_SWE_Raw = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TOWRE_SWE_Scaled = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TOWRE_SWE_Perc = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    TOWRE_SWE_AE = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TOWRE_SWE_GE = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TOWRE_SWE_Desc = orm.mapped_column(
        sqlalchemy.String(20, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )

    # Total scores
    TOWRE_Total_Scaled = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TOWRE_Total_Perc = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    TOWRE_Total_Desc = orm.mapped_column(
        sqlalchemy.String(20, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )


class Wiat(Base):
    """SQLAlchemy model representing the I2B2_Export_WIAT_t table in the nextgen schema.

    This table stores Wechsler Individual Achievement Test (WIAT) assessment data,
    including raw scores, standardized scores, and percentiles for various subtests
    measuring academic achievement in areas like reading, spelling, and mathematics.
    """

    __tablename__ = "I2B2_Export_WIAT_t"
    __table_args__ = {"schema": "nextgen"}  # noqa: RUF012

    URSI = orm.mapped_column(
        sqlalchemy.String(10, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )
    SiteID = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    RaterID = orm.mapped_column(
        sqlalchemy.String(4, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )
    SourceType = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    AssessmentStartDate = orm.mapped_column(
        sqlalchemy.String(10, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )
    AssessmentStartTime = orm.mapped_column(
        sqlalchemy.String(5, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )
    Successful = orm.mapped_column(
        sqlalchemy.String(1, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )
    EID = orm.mapped_column(
        sqlalchemy.String(15, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )
    START_DATE = orm.mapped_column(
        sqlalchemy.String(20, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=False,
        primary_key=True,
    )
    Study = orm.mapped_column(
        sqlalchemy.String(3, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )
    Site = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Days_Baseline = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Year = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Season = orm.mapped_column(
        sqlalchemy.String(6, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=False,
    )

    # Assessment status
    WIAT_Complete = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WIAT_Incomplete_reason = orm.mapped_column(
        sqlalchemy.String(300, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )
    WIAT_Valid = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WIAT_Invalid_Reason = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Numerical Operations subtest
    WIAT_Num_Raw = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WIAT_Num_Stnd = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_Num_P = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)

    # Pseudoword Decoding subtest
    WIAT_Pseudo_Raw = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WIAT_Pseudo_Stnd = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_Pseudo_P = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)

    # Spelling subtest
    WIAT_Spell_Raw = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WIAT_Spell_Stnd = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_Spell_P = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)

    # Word Reading subtest
    WIAT_Word_Raw = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WIAT_Word_Stnd = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_Word_P = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)

    # Listening Comprehension - Receptive Vocabulary
    WIAT_LCRV_Raw = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_LCRV_Std = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WIAT_LCRV_P = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)

    # Listening Comprehension - Oral Discourse Comprehension
    WIAT_LCODC_Raw = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_LCODC_Stnd = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WIAT_LCODC_P = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)

    # Listening Comprehension composite
    WIAT_LC_Stnd = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_LC_P = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)

    # Reading Comprehension subtest
    WIAT_RC_Raw = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_RC_Stnd = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_RC_P = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)

    # Math Problem Solving subtest
    WIAT_MP_Raw = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_MP_Stnd = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_MP_P = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)


class Srs(Base):
    """SQLAlchemy model representing the I2B2_Export_SRS_t table in the nextgen schema.

    This table stores the Social Responsiveness Scale (SRS) assessment data,
    which measures social impairment associated with autism spectrum disorders.
    It includes individual item scores (1-65) and derived subscale scores with
    corresponding T-scores for different domains of social functioning.
    """

    __tablename__ = "I2B2_Export_SRS_t"
    __table_args__ = {"schema": "nextgen"}  # noqa: RUF012

    URSI = orm.mapped_column(
        sqlalchemy.String(10, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )
    SiteID = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    RaterID = orm.mapped_column(
        sqlalchemy.String(4, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )
    SourceType = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    AssessmentStartDate = orm.mapped_column(
        sqlalchemy.String(10, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )
    AssessmentStartTime = orm.mapped_column(
        sqlalchemy.String(5, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )
    Successful = orm.mapped_column(
        sqlalchemy.String(1, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )
    EID = orm.mapped_column(
        sqlalchemy.String(15, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )
    START_DATE = orm.mapped_column(
        sqlalchemy.String(20, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=False,
        primary_key=True,
    )
    Study = orm.mapped_column(
        sqlalchemy.String(3, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )
    Site = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Days_Baseline = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Year = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Season = orm.mapped_column(
        sqlalchemy.String(6, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=False,
    )

    # Individual SRS item scores (1-65)
    SRS_01 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_02 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_03 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_04 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_05 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_06 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_07 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_08 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_09 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_10 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_11 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_12 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_13 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_14 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_15 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_16 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_17 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_18 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_19 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_20 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_21 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_22 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_23 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_24 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_25 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_26 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_27 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_28 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_29 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_30 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_31 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_32 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_33 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_34 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_35 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_36 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_37 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_38 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_39 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_40 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_41 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_42 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_43 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_44 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_45 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_46 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_47 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_48 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_49 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_50 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_51 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_52 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_53 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_54 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_55 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_56 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_57 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_58 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_59 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_60 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_61 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_62 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_63 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_64 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_65 = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Social Awareness subscale
    SRS_AWR = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_AWR_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Social Cognition subscale
    SRS_COG = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_COG_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Social Communication subscale
    SRS_COM = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_COM_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # DSM-compatible Restricted & Repetitive Behavior subscale
    SRS_DSMRRB = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_DSMRRB_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Social Motivation subscale
    SRS_MOT = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_MOT_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Restricted & Repetitive Behavior subscale
    SRS_RRB = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_RRB_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Social Communication and Interaction subscale
    SRS_SCI = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_SCI_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # SRS Total Score
    SRS_Total = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_Total_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)
