"""Definitions of the used tables in the SQL Database.

These tables were created by first auto-generating the schema with
sqlacodegen, and then rewriting it to a class-based format with
Claude Sonnet 3.7. As such, some care may need to be taken with
interpreting the in-line comments.

"""

import sqlalchemy
from sqlalchemy import orm


class Base(orm.DeclarativeBase):
    """Base class for all tables."""


class Cbcl(Base):
    """SQLAlchemy model representing the I2B2_Export_CBCL_t table in the nextgen schema.

    This table stores the Child Behavior Checklist (CBCL) assessment data.
    """

    __tablename__ = "I2B2_Export_CBCL_t"
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

    # Individual CBCL item scores (1-112)
    CBCL_01 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_02 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_03 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_04 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_05 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_06 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_07 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_08 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_09 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_10 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_11 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_12 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_13 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_14 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_15 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_16 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_17 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_18 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_19 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_20 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_21 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_22 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_23 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_24 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_25 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_26 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_27 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_28 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_29 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_30 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_31 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_32 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_33 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_34 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_35 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_36 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_37 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_38 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_39 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_40 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_41 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_42 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_43 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_44 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_45 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_46 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_47 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_48 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_49 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_50 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_51 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_52 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_53 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_54 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_55 = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Item 56 has multiple sub-items (a-h)
    CBCL_56A = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_56B = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_56C = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_56D = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_56E = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_56F = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_56G = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_56H = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Continuing individual items
    CBCL_57 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_58 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_59 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_60 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_61 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_62 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_63 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_64 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_65 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_66 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_67 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_68 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_69 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_70 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_71 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_72 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_73 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_74 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_75 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_76 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_77 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_78 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_79 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_80 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_81 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_82 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_83 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_84 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_85 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_86 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_87 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_88 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_89 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_90 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_91 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_92 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_93 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_94 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_95 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_96 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_97 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_98 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_99 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_100 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_101 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_102 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_103 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_104 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_105 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_106 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_107 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_108 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_109 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_110 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_111 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_112 = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Item 113 has multiple sub-items
    CBCL_113A = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_113B = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_113C = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Syndrome scales

    # Anxious/Depressed scale
    CBCL_AD = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_AD_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Withdrawn/Depressed scale
    CBCL_WD = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_WD_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Somatic Complaints scale
    CBCL_SC = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_SC_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Social Problems scale
    CBCL_SP = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_SP_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Thought Problems scale
    CBCL_TP = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_TP_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Attention Problems scale
    CBCL_AP = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_AP_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Rule-Breaking Behavior scale
    CBCL_RBB = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_RBB_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Aggressive Behavior scale
    CBCL_AB = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_AB_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Other Problems scale
    CBCL_OP = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Composite scales

    # Internalizing Problems
    CBCL_Int = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_Int_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Externalizing Problems
    CBCL_Ext = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_Ext_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Competence score
    CBCL_C = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Total Problems
    CBCL_Total = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_Total_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)


class Celf5(Base):
    """SQLAlchemy model representing the I2B2_Export_CELF_t table in the nextgen schema.

    This table stores Clinical Evaluation of Language Fundamentals assessment data,
    """

    __tablename__ = "I2B2_Export_CELF_t"
    __table_args__ = {"schema": "nextgen"}

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
    CELF_Complete = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CELF_Incomplete_Reason = orm.mapped_column(
        sqlalchemy.String(30, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )
    CELF_Valid = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CELF_Invalid_Reason = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Scores
    CELF_Total = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CELF_CriterionScore = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CELF_ExceedCutoff = orm.mapped_column(sqlalchemy.Integer, nullable=True)


class CmiHbnIdTrack(Base):
    """SQLAlchemy model representing the CMI_HBN_IDTrack_t table in the nextgen schema.

    This table stores participant identification and tracking information for the
    Child Mind Institute Healthy Brain Network (CMI-HBN) study, including participant
    identifiers, personal information, and demographic data.
    """

    __tablename__ = "CMI_HBN_IDTrack_t"
    __table_args__ = {"schema": "nextgen"}  # noqa: RUF012

    # Primary identification fields
    person_nbr = orm.mapped_column(
        sqlalchemy.CHAR(12, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=False,
        primary_key=True,
    )
    person_id = orm.mapped_column(sqlalchemy.Uuid, nullable=False)
    create_timestamp = orm.mapped_column(sqlalchemy.DateTime, nullable=False)

    # Alternative identifiers
    GUID = orm.mapped_column(
        sqlalchemy.String(15, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )
    person_number = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Rand_ID = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MRN = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Personal information
    last_name = orm.mapped_column(
        sqlalchemy.String(60, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=False,
    )
    first_name = orm.mapped_column(
        sqlalchemy.String(60, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=False,
    )
    sex = orm.mapped_column(
        sqlalchemy.CHAR(1, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )

    # Age and date information
    Age = orm.mapped_column(sqlalchemy.Numeric(17, 6), nullable=True)
    Age_Today = orm.mapped_column(sqlalchemy.Numeric(17, 6), nullable=True)
    DOB = orm.mapped_column(sqlalchemy.Date, nullable=True)

    # Site information
    Study_Site = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    site_txt = orm.mapped_column(
        sqlalchemy.String(50, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )


class Conners3(Base):
    """SQLAlchemy model representing the I2B2_Export_C3SR_t table in the nextgen schema.

    This table stores the Conners-3 Self-Report Scale (C3SR) assessment data.
    """

    __tablename__ = "I2B2_Export_C3SR_t"
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

    # Individual C3SR item scores (1-39)
    C3SR_01 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_02 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_03 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_04 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_05 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_06 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_07 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_08 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_09 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_10 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_11 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_12 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_13 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_14 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_15 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_16 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_17 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_18 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_19 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_20 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_21 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_22 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_23 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_24 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_25 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_26 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_27 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_28 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_29 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_30 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_31 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_32 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_33 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_34 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_35 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_36 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_37 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_38 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_39 = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Subscale scores and T-scores

    # Aggression subscale
    C3SR_AG = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_AG_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Family Relations subscale
    C3SR_FR = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_FR_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Hyperactivity/Impulsivity subscale
    C3SR_HY = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_HY_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Inattention subscale
    C3SR_IN = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_IN_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Learning Problems subscale
    C3SR_LP = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_LP_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Validity indicators
    C3SR_NI = orm.mapped_column(
        sqlalchemy.String(1, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )
    C3SR_PI = orm.mapped_column(
        sqlalchemy.String(1, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )


class Ctopp2(Base):
    """SQLAlchemy model representing the I2B2_Export_CTOPP_t table in the nextgen schema.

    This table stores the Comprehensive Test of Phonological Processing (CTOPP) assessment data,
    """

    __tablename__ = "I2B2_Export_CTOPP_t"
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
    CTOPP_Complete = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CTOPP_Incomplete_Reason = orm.mapped_column(
        sqlalchemy.String(100, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )
    CTOPP_Valid = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CTOPP_Invalid_Reason = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Elision subtest (EL)
    CTOPP_EL_R = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CTOPP_EL_P = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    CTOPP_EL_S = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CTOPP_EL_D = orm.mapped_column(
        sqlalchemy.String(30, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )

    # Blending Words subtest (BW)
    CTOPP_BW_R = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CTOPP_BW_P = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    CTOPP_BW_S = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CTOPP_BW_D = orm.mapped_column(
        sqlalchemy.String(30, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )

    # Number Repetition subtest (NR)
    CTOPP_NR_R = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CTOPP_NR_P = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    CTOPP_NR_S = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CTOPP_NR_D = orm.mapped_column(
        sqlalchemy.String(30, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )

    # Rapid Digit Naming subtest (RD)
    CTOPP_RD_R = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CTOPP_RD_P = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    CTOPP_RD_S = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CTOPP_RD_D = orm.mapped_column(
        sqlalchemy.String(30, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )

    # Rapid Letter Naming subtest (RL)
    CTOPP_RL_R = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CTOPP_RL_P = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    CTOPP_RL_S = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CTOPP_RL_D = orm.mapped_column(
        sqlalchemy.String(30, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )

    # Rapid Object Naming subtest (RO)
    CTOPP_RO_R = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CTOPP_RO_P = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    CTOPP_RO_S = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CTOPP_RO_D = orm.mapped_column(
        sqlalchemy.String(30, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )

    # Rapid Symbolic Naming composite (RSN)
    CTOPP_RSN_Sum = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CTOPP_RSN_P = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    CTOPP_RSN_Comp = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CTOPP_RSN_D = orm.mapped_column(
        sqlalchemy.String(30, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )

    # Phonological Awareness composite (PA)
    CTOPP_PA_SS = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CTOPP_PA_Comp = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CTOPP_PA_P = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CTOPP_PA_Desc = orm.mapped_column(
        sqlalchemy.String(30, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )

    # Rapid Non-Symbolic Naming composite (RnSN)
    CTOPP_RnSN_Comp = orm.mapped_column(sqlalchemy.Integer, nullable=True)


class Gars(Base):
    """SQLAlchemy model representing the I2B2_Export_GARS_t table in the nextgen schema.

    This table stores the Gilliam Autism Rating Scale (GARS) assessment data,
    which is used to identify and assess the severity of autism spectrum disorder.
    It includes individual item responses (1-59) and derived scores for six subscales:
    Restricted/Repetitive Behaviors, Social Interaction, Social Communication,
    Emotional Responses, Cognitive Style, and Maladaptive Speech, as well as
    the Autism Index (AI) composite score.
    """

    __tablename__ = "I2B2_Export_GARS_t"
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

    # Individual GARS item responses (1-59)
    GARS_01 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_02 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_03 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_04 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_05 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_06 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_07 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_08 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_09 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_10 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_11 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_12 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_13 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_14 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_15 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_16 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_17 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_18 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_19 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_20 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_21 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_22 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_23 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_24 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_25 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_26 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_27 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_28 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_29 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_30 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_31 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_32 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_33 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_34 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_35 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_36 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_37 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_38 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_39 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_40 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_41 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_42 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_43 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_44 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_45 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_46 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_47 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_48 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_49 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_50 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_51 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_52 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_53 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_54 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_55 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_56 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_57 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_58 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_59 = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Restricted/Repetitive Behaviors subscale
    GARS_RB_Raw = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_RB_Perc = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_RB_Scaled = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Social Interaction subscale
    GARS_SI_Raw = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_SI_Perc = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_SI_Scaled = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Social Communication subscale
    GARS_SC_Raw = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_SC_Perc = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_SC_Scaled = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Emotional Responses subscale
    GARS_ER_Raw = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_ER_Perc = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_ER_Scaled = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Cognitive Style subscale
    GARS_CS_Raw = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_CS_Perc = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_CS_Scaled = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Maladaptive Speech subscale
    GARS_MS_Raw = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_MS_Perc = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_MS_Scaled = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Autism Index composite score
    GARS_AI_SumScaled = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_AI = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_AI_Perc = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_AI_Prob = orm.mapped_column(
        sqlalchemy.String(100, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )
    GARS_AI_Sev = orm.mapped_column(
        sqlalchemy.String(100, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )


class GroovedPegboard(Base):
    """SQLAlchemy model representing the I2B2_Export_GroovedPeg_t table in the nextgen schema.

    This table stores Grooved Pegboard Test data.
    """

    __tablename__ = "I2B2_Export_GroovedPeg_t"
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
    peg_complete = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    peg_incomplete = orm.mapped_column(
        sqlalchemy.String(140, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )
    peg_valid = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    peg_invalid = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Hand dominance
    peg_dom_hand = orm.mapped_column(
        sqlalchemy.String(13, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=True,
    )

    # Dominant hand performance
    peg_drops_d = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    peg_time_d = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    peg_z_d = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)

    # Non-dominant hand performance
    peg_drops_nd = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    peg_time_nd = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    peg_z_nd = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)


class MfqParent(Base):
    """SQLAlchemy model representing the I2B2_Export_MFQ_Parent_t table in the nextgen schema.

    This table stores the Mood and Feelings Questionnaire (MFQ) Parent Report data.
    """

    __tablename__ = "I2B2_Export_MFQ_Parent_t"
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

    # Individual MFQ Parent Report item responses (1-34)
    MFQ_P_01 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_P_02 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_P_03 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_P_04 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_P_05 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_P_06 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_P_07 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_P_08 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_P_09 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_P_10 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_P_11 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_P_12 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_P_13 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_P_14 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_P_15 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_P_16 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_P_17 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_P_18 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_P_19 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_P_20 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_P_21 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_P_22 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_P_23 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_P_24 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_P_25 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_P_26 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_P_27 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_P_28 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_P_29 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_P_30 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_P_31 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_P_32 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_P_33 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_P_34 = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Total score
    MFQ_P_Total = orm.mapped_column(sqlalchemy.Integer, nullable=True)


class MfqSelf(Base):
    """SQLAlchemy model representing the I2B2_Export_MFQ_Self_t table in the nextgen schema.

    This table stores the Mood and Feelings Questionnaire (MFQ) Self Report data.
    """

    __tablename__ = "I2B2_Export_MFQ_Self_t"
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

    # Individual MFQ Self Report item responses (1-33)
    MFQ_SR_01 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_SR_02 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_SR_03 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_SR_04 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_SR_05 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_SR_06 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_SR_07 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_SR_08 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_SR_09 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_SR_10 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_SR_11 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_SR_12 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_SR_13 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_SR_14 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_SR_15 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_SR_16 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_SR_17 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_SR_18 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_SR_19 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_SR_20 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_SR_21 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_SR_22 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_SR_23 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_SR_24 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_SR_25 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_SR_26 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_SR_27 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_SR_28 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_SR_29 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_SR_30 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_SR_31 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_SR_32 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_SR_33 = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Total score
    MFQ_SR_Total = orm.mapped_column(sqlalchemy.Integer, nullable=True)


class ScaredParent(Base):
    """SQLAlchemy model representing the I2B2_Export_SCARED_Parent_t table in the nextgen schema.

    This table stores the Screen for Child Anxiety Related Disorders (SCARED) Parent Report data,
    """

    __tablename__ = "I2B2_Export_SCARED_Parent_t"
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

    # Individual SCARED Parent Report item responses (1-41)
    SCARED_P_01 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_P_02 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_P_03 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_P_04 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_P_05 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_P_06 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_P_07 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_P_08 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_P_09 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_P_10 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_P_11 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_P_12 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_P_13 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_P_14 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_P_15 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_P_16 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_P_17 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_P_18 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_P_19 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_P_20 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_P_21 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_P_22 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_P_23 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_P_24 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_P_25 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_P_26 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_P_27 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_P_28 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_P_29 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_P_30 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_P_31 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_P_32 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_P_33 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_P_34 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_P_35 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_P_36 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_P_37 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_P_38 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_P_39 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_P_40 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_P_41 = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Subscale scores
    # Generalized Anxiety Disorder
    SCARED_P_GD = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Panic Disorder
    SCARED_P_PN = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Separation Anxiety
    SCARED_P_SC = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Social Anxiety/School Avoidance
    SCARED_P_SH = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Social Phobia
    SCARED_P_SP = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Total score
    SCARED_P_Total = orm.mapped_column(sqlalchemy.Integer, nullable=True)


class ScaredSelf(Base):
    """SQLAlchemy model representing the I2B2_Export_SCARED_Self_t table in the nextgen schema.

    This table stores the Screen for Child Anxiety Related Disorders (SCARED) Self Report data,
    """

    __tablename__ = "I2B2_Export_SCARED_Self_t"
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

    # Individual SCARED Self Report item responses (1-41)
    SCARED_SR_01 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SR_02 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SR_03 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SR_04 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SR_05 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SR_06 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SR_07 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SR_08 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SR_09 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SR_10 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SR_11 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SR_12 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SR_13 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SR_14 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SR_15 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SR_16 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SR_17 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SR_18 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SR_19 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SR_20 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SR_21 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SR_22 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SR_23 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SR_24 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SR_25 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SR_26 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SR_27 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SR_28 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SR_29 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SR_30 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SR_31 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SR_32 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SR_33 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SR_34 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SR_35 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SR_36 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SR_37 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SR_38 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SR_39 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SR_40 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SR_41 = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Subscale scores
    # Generalized Anxiety Disorder
    SCARED_SR_GD = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Panic Disorder
    SCARED_SR_PN = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Separation Anxiety
    SCARED_SR_SC = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Social Anxiety/School Avoidance
    SCARED_SR_SH = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Social Phobia
    SCARED_SR_SP = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Total score
    SCARED_SR_Total = orm.mapped_column(sqlalchemy.Integer, nullable=True)


class Scq(Base):
    """SQLAlchemy model representing the I2B2_Export_SCQ_t table in the nextgen schema.

    This table stores the Social Communication Questionnaire (SCQ) assessment data.
    """

    __tablename__ = "I2B2_Export_SCQ_t"
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

    # Individual SCQ item responses (1-40)
    # Items assess reciprocal social interaction, communication, and
    # restricted, repetitive, and stereotyped patterns of behavior
    SCQ_01 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCQ_02 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCQ_03 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCQ_04 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCQ_05 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCQ_06 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCQ_07 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCQ_08 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCQ_09 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCQ_10 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCQ_11 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCQ_12 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCQ_13 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCQ_14 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCQ_15 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCQ_16 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCQ_17 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCQ_18 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCQ_19 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCQ_20 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCQ_21 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCQ_22 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCQ_23 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCQ_24 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCQ_25 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCQ_26 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCQ_27 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCQ_28 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCQ_29 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCQ_30 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCQ_31 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCQ_32 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCQ_33 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCQ_34 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCQ_35 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCQ_36 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCQ_37 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCQ_38 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCQ_39 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCQ_40 = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Total score - scores of 15 or higher indicate possible ASD
    SCQ_Total = orm.mapped_column(sqlalchemy.Integer, nullable=True)


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


class Swan(Base):
    """SQLAlchemy model representing the I2B2_Export_SWAN_t table in the nextgen schema.

    This table stores the Strengths and Weaknesses of ADHD Symptoms and Normal Behavior
    (SWAN) assessment data.
    """

    __tablename__ = "I2B2_Export_SWAN_t"
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

    # Individual SWAN item responses (1-18)
    # Items 1-9 assess inattention symptoms
    # Items 10-18 assess hyperactivity/impulsivity symptoms
    SWAN_01 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SWAN_02 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SWAN_03 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SWAN_04 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SWAN_05 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SWAN_06 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SWAN_07 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SWAN_08 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SWAN_09 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SWAN_10 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SWAN_11 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SWAN_12 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SWAN_13 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SWAN_14 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SWAN_15 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SWAN_16 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SWAN_17 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SWAN_18 = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Subscale scores

    # Inattention subscale (average of items 1-9)
    SWAN_IN = orm.mapped_column(sqlalchemy.Numeric(18, 6), nullable=True)

    # Hyperactivity/Impulsivity subscale (average of items 10-18)
    SWAN_HY = orm.mapped_column(sqlalchemy.Numeric(18, 6), nullable=True)

    # Total score (average of all items)
    SWAN_Total = orm.mapped_column(sqlalchemy.Numeric(18, 6), nullable=True)


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


class Ysr(Base):
    """SQLAlchemy model representing the I2B2_Export_YSR_t table in the nextgen schema.

    This table stores the Youth Self-Report (YSR) assessment data.
    """

    __tablename__ = "I2B2_Export_YSR_t"
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

    # Individual YSR item scores (1-55)
    YSR_01 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_02 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_03 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_04 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_05 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_06 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_07 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_08 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_09 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_10 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_11 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_12 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_13 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_14 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_15 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_16 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_17 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_18 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_19 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_20 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_21 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_22 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_23 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_24 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_25 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_26 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_27 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_28 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_29 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_30 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_31 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_32 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_33 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_34 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_35 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_36 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_37 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_38 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_39 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_40 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_41 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_42 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_43 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_44 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_45 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_46 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_47 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_48 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_49 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_50 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_51 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_52 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_53 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_54 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_55 = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Item 56 has multiple sub-items (a-h)
    YSR_56a = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_56b = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_56c = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_56d = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_56e = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_56f = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_56g = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_56h = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Continuing individual items (57-112)
    YSR_57 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_58 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_59 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_60 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_61 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_62 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_63 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_64 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_65 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_66 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_67 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_68 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_69 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_70 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_71 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_72 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_73 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_74 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_75 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_76 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_77 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_78 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_79 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_80 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_81 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_82 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_83 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_84 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_85 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_86 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_87 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_88 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_89 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_90 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_91 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_92 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_93 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_94 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_95 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_96 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_97 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_98 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_99 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_100 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_101 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_102 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_103 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_104 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_105 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_106 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_107 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_108 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_109 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_110 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_111 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_112 = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Syndrome scales

    # Aggressive Behavior scale
    YSR_AB = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_AB_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Anxious/Depressed scale
    YSR_AD = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_AD_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Attention Problems scale
    YSR_AP = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_AP_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Withdrawn/Depressed scale
    YSR_WD = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_WD_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Rule-Breaking Behavior scale
    YSR_RBB = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_RBB_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Somatic Complaints scale
    YSR_SC = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_SC_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Social Problems scale
    YSR_SP = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_SP_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Thought Problems scale
    YSR_TP = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_TP_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Composite scales

    # Externalizing Problems
    YSR_Ext = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_Ext_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Internalizing Problems
    YSR_Int = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_Int_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Other Problems scale
    YSR_OP = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Competence score
    YSR_C = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Total Problems
    YSR_Total = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_Total_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)
