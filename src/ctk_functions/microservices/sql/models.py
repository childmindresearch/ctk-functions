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


class Asr(Base):
    """SQLAlchemy model representing the I2B2_Export_ASR table."""

    __tablename__ = "I2B2_Export_ASR_T"
    __table_args__ = {"schema": "nextgen"}  # noqa: RUF012

    URSI = orm.mapped_column(sqlalchemy.String(10), nullable=True)
    SiteID = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    RaterID = orm.mapped_column(sqlalchemy.String(4), nullable=True)
    SourceType = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    AssessmentStartDate = orm.mapped_column(sqlalchemy.String(10), nullable=True)
    AssessmentStartTime = orm.mapped_column(sqlalchemy.String(5), nullable=True)
    Successful = orm.mapped_column(sqlalchemy.String(1), nullable=True)
    EID = orm.mapped_column(sqlalchemy.String(15), nullable=True)
    START_DATE = orm.mapped_column(
        sqlalchemy.String(20), nullable=False, primary_key=True
    )
    Study = orm.mapped_column(sqlalchemy.String(3), nullable=True)
    Site = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Days_Baseline = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Year = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Season = orm.mapped_column(sqlalchemy.String(6), nullable=False)

    # ASR items 1-55
    ASR_01 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_02 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_03 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_04 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_05 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_06 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_07 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_08 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_09 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_10 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_11 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_12 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_13 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_14 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_15 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_16 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_17 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_18 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_19 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_20 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_21 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_22 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_23 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_24 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_25 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_26 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_27 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_28 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_29 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_30 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_31 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_32 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_33 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_34 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_35 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_36 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_37 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_38 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_39 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_40 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_41 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_42 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_43 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_44 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_45 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_46 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_47 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_48 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_49 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_50 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_51 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_52 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_53 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_54 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_55 = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # ASR item 56 a-d
    ASR_56a = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_56b = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_56c = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_56d = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # ASR items 57-126
    ASR_57 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_58 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_59 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_60 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_61 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_62 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_63 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_64 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_65 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_66 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_67 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_68 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_69 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_70 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_71 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_72 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_73 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_74 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_75 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_76 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_77 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_78 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_79 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_80 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_81 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_82 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_83 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_84 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_85 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_86 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_87 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_88 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_89 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_90 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_91 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_92 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_93 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_94 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_95 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_96 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_97 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_98 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_99 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_100 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_101 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_102 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_103 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_104 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_105 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_106 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_107 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_108 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_109 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_110 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_111 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_112 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_113 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_114 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_115 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_116 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_117 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_118 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_119 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_120 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_121 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_122 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_123 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_124 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_125 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_126 = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # ASR syndrome scales and T scores
    ASR_AD = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_AD_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_WD = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_WD_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_SC = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_SC_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_TP = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_TP_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_AP = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_AP_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_RBB = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_RBB_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_AB = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_AB_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_OP = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # ASR broad-band scales
    ASR_Int = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_Int_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_Ext = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_Ext_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_Intrusive = orm.mapped_column(sqlalchemy.String(2), nullable=True)
    ASR_Intrusive_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_C = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_Total = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_Total_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)


class Cbcl(Base):
    """SQLAlchemy model representing the I2B2_Export_CBCL_t table in the nextgen schema.

    This table stores the Child Behavior Checklist (CBCL) assessment data.
    """

    __tablename__ = "I2B2_Export_CBCL_T"
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

    __tablename__ = "I2B2_Export_CELF_T"
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

    __tablename__ = "CMI_HBN_IDTrack_T"
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

    __tablename__ = "I2B2_Export_C3SR_T"
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


class Gars(Base):
    """SQLAlchemy model representing the I2B2_Export_GARS_t table in the nextgen schema.

    This table stores the Gilliam Autism Rating Scale (GARS) assessment data,
    which is used to identify and assess the severity of autism spectrum disorder.
    It includes individual item responses (1-59) and derived scores for six subscales:
    Restricted/Repetitive Behaviors, Social Interaction, Social Communication,
    Emotional Responses, Cognitive Style, and Maladaptive Speech, as well as
    the Autism Index (AI) composite score.
    """

    __tablename__ = "I2B2_Export_GARS_T"
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
    """SQLAlchemy model representing the I2B2_Export_GroovedPeg_t table.

    This table stores Grooved Pegboard Test data.
    """

    __tablename__ = "I2B2_Export_GroovedPeg_T"
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
    """SQLAlchemy model representing the I2B2_Export_MFQ_Parent_t table.

    This table stores the Mood and Feelings Questionnaire (MFQ) Parent Report data.
    """

    __tablename__ = "I2B2_Export_MFQ_Parent_T"
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
    """SQLAlchemy model representing the I2B2_Export_MFQ_Self_t table.

    This table stores the Mood and Feelings Questionnaire (MFQ) Self Report data.
    """

    __tablename__ = "I2B2_Export_MFQ_Self_T"
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
    """SQLAlchemy model representing the I2B2_Export_SCARED_Parent_t table.

    This table stores the Screen for Child Anxiety Related Disorders (SCARED) Parent
    Report data,
    """

    __tablename__ = "I2B2_Export_SCARED_Parent_T"
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
    """SQLAlchemy model representing the I2B2_Export_SCARED_Self_t table.

    This table stores the Screen for Child Anxiety Related Disorders (SCARED) Self
    Report data,
    """

    __tablename__ = "I2B2_Export_SCARED_Self_T"
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

    __tablename__ = "I2B2_Export_SCQ_T"
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

    __tablename__ = "I2B2_Export_SRS_T"
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


class SummaryScores(Base):
    """SQLAlchemy model representing CMI_HBN_SummaryScores in the dbo schema."""

    __tablename__ = "CMI_HBN_SummaryScores_T"
    __table_args__ = {"schema": "nextgen"}  # noqa: RUF012

    # Primary demographic information
    person_id = orm.mapped_column(
        sqlalchemy.Uuid(),
        nullable=False,
        primary_key=True,
    )
    last_name = orm.mapped_column(sqlalchemy.String(60), nullable=False)
    preferred_name = orm.mapped_column(sqlalchemy.Integer, nullable=False)
    first_name = orm.mapped_column(sqlalchemy.String(60), nullable=True)
    Age = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    sex = orm.mapped_column(sqlalchemy.CHAR(1), nullable=True)
    date_of_birth = orm.mapped_column(sqlalchemy.String(8), nullable=True)
    Pronoun = orm.mapped_column(sqlalchemy.String(100), nullable=True)

    # WIAT scores - Main subtests
    WIAT_Num_S = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_Num_P = orm.mapped_column(sqlalchemy.DECIMAL(16), nullable=True)
    WIAT_Pseudo_S = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_Pseudo_P = orm.mapped_column(sqlalchemy.DECIMAL(16), nullable=True)
    WIAT_Spell_S = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_Spell_P = orm.mapped_column(sqlalchemy.DECIMAL(16), nullable=True)
    WIAT_Word_S = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_Word_P = orm.mapped_column(sqlalchemy.DECIMAL(16), nullable=True)
    WIAT_Listen_S = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_Listen_P = orm.mapped_column(sqlalchemy.DECIMAL(16), nullable=True)
    WIAT_Read_S = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_Read_P = orm.mapped_column(sqlalchemy.DECIMAL(16), nullable=True)
    WIAT_Math_S = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_Math_P = orm.mapped_column(sqlalchemy.DECIMAL(16), nullable=True)

    # WIAT dates
    WIAT_Date = orm.mapped_column(sqlalchemy.Date, nullable=True)
    WIAT_Abbr_Date = orm.mapped_column(sqlalchemy.Date, nullable=True)
    WIAT_Screen_Date = orm.mapped_column(sqlalchemy.Date, nullable=True)
    WIAT_Part2_Date = orm.mapped_column(sqlalchemy.Date, nullable=True)
    WIAT_Writing_date = orm.mapped_column(sqlalchemy.Date, nullable=True)
    WIAT_GN_Writing_date = orm.mapped_column(sqlalchemy.Date, nullable=True)

    # WIAT Math Fluency scores
    WIAT_MF_S = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_MF_P = orm.mapped_column(sqlalchemy.DECIMAL(16), nullable=True)
    WIAT_MF_Add_S = orm.mapped_column(sqlalchemy.DECIMAL(16, 5), nullable=True)
    WIAT_MF_Add_P = orm.mapped_column(sqlalchemy.DECIMAL(16), nullable=True)
    WIAT_MF_Sub_S = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_MF_Sub_P = orm.mapped_column(sqlalchemy.DECIMAL(16), nullable=True)
    WIAT_MF_Mult_S = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_MF_Mult_P = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)

    # Listening Comprehension scores
    LC_ODC_Std = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    LC_ODC_Perc = orm.mapped_column(sqlalchemy.DECIMAL(16), nullable=True)
    LC_ODC_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    LC_RV_Perc = orm.mapped_column(sqlalchemy.DECIMAL(16), nullable=True)
    LC_RV_Std = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    LC_RV_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)

    # Quotient scores
    Quotient_GlobalScaled = orm.mapped_column(sqlalchemy.DECIMAL(16, 4), nullable=True)
    Quotient_In_Scale = orm.mapped_column(sqlalchemy.DECIMAL(16, 4), nullable=True)
    Quotient_Motion_Scale = orm.mapped_column(sqlalchemy.DECIMAL(16, 4), nullable=True)
    Quotient_SysIndex = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Error scores
    RD_Errors = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    RL_Errors = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    RO_Errors = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    RC_Errors = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # NIH Toolbox scores - 7 task battery
    NIH7_Card = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    NIH7_Card_P = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    NIH7_Comp = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    NIH7_Comp_P = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    NIH7_Flanker = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    NIH7_Flanker_P = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    NIH7_List = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    NIH7_List_P = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    NIH7_Pattern = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    NIH7_Pattern_P = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    NIH7_Picture = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    NIH7_Picture_P = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)

    # NIH Toolbox scores - 5 task battery
    NIH5_Card = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    NIH5_Card_P = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    NIH5_Flanker = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    NIH5_Flanker_P = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    NIH5_Picture = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    NIH5_Picture_P = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    NIH5_List = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    NIH5_List_P = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    NIH5_Pattern = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    NIH5_Pattern_P = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # K-BIT scores
    KBIT_IQ = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    KBIT_IQ_P = orm.mapped_column(sqlalchemy.DECIMAL(16), nullable=True)
    KBIT_IQ_Desc = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    KBIT_NV = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    KBIT_NV_P = orm.mapped_column(sqlalchemy.DECIMAL(16), nullable=True)
    KBIT_NV_Desc = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    KBIT_V = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    KBIT_V_P = orm.mapped_column(sqlalchemy.DECIMAL(16), nullable=True)
    KBIT_V_Desc = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    KBIT_Date = orm.mapped_column(sqlalchemy.Date, nullable=True)
    KBIT_VK_SS = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    KBIT_VK_P = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    KBIT_R_SS = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    KBIT_R_P = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    KBIT_Revised = orm.mapped_column(sqlalchemy.Integer, nullable=False)

    # CELF score
    CELF_CriterionCutoff = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # TOWRE scores
    TOWRE_PDE_S = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TOWRE_PDE_P = orm.mapped_column(sqlalchemy.DECIMAL(16), nullable=True)
    TOWRE_PDE_D = orm.mapped_column(sqlalchemy.String(20), nullable=True)
    TOWRE_SWE_S = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TOWRE_SWE_P = orm.mapped_column(sqlalchemy.DECIMAL(16), nullable=True)
    TOWRE_SWE_D = orm.mapped_column(sqlalchemy.String(20), nullable=True)
    TOWRE_Total_S = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TOWRE_Total_P = orm.mapped_column(sqlalchemy.DECIMAL(16), nullable=True)
    TOWRE_Total_D = orm.mapped_column(sqlalchemy.String(20), nullable=True)
    TOWRE_Date = orm.mapped_column(sqlalchemy.Date, nullable=True)

    # WISC scores - Scaled scores
    WISC_BD_Scaled = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_Similarities_Scaled = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_MR_Scaled = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_DS_Scaled = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_Coding_Scaled = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_Vocab_Scaled = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_FW_Scaled = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_VP_Scaled = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_PS_Scaled = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_SS_Scaled = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # WISC scores - Composite scores
    WISC_VCI = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_VSI = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_FRI = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_WMI = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_PSI = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_FSIQ = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # WISC scores - Percentiles
    WISC_VCI_Percentile = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_VSI_Percentile = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_FRI_Percentile = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_WMI_Percentile = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_PRI_Percentile = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_FSIQ_Percentile = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Various test percentiles and descriptions
    EL_percentile = orm.mapped_column(sqlalchemy.DECIMAL(16), nullable=True)
    WISC_Date = orm.mapped_column(sqlalchemy.Date, nullable=True)
    EL_Desc = orm.mapped_column(sqlalchemy.String(30), nullable=True)
    BW_Percentile = orm.mapped_column(sqlalchemy.DECIMAL(16), nullable=True)
    BW_Desc = orm.mapped_column(sqlalchemy.String(30), nullable=True)
    NR_percentile = orm.mapped_column(sqlalchemy.DECIMAL(16), nullable=True)
    NR_Desc = orm.mapped_column(sqlalchemy.String(30), nullable=True)
    RD_percentile = orm.mapped_column(sqlalchemy.DECIMAL(16), nullable=True)
    RD_Desc = orm.mapped_column(sqlalchemy.String(30), nullable=True)
    RL_percentile = orm.mapped_column(sqlalchemy.DECIMAL(16), nullable=True)
    RL_Desc = orm.mapped_column(sqlalchemy.String(30), nullable=True)
    RO_percentile = orm.mapped_column(sqlalchemy.DECIMAL(16), nullable=True)
    RO_Desc = orm.mapped_column(sqlalchemy.String(30), nullable=True)

    # CTOPP scores
    CTOPP_PA_P = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CTOPP_PA_Comp = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CTOPP_PA_Desc = orm.mapped_column(sqlalchemy.String(30), nullable=True)
    RSN_percentile = orm.mapped_column(sqlalchemy.DECIMAL(16), nullable=True)
    RSN_composite = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    RSN_Desc = orm.mapped_column(sqlalchemy.String(30), nullable=True)
    RC_percentile = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    RC_desc = orm.mapped_column(sqlalchemy.String(30), nullable=True)
    RnSN_composite = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    RnSN_percentile = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    RnSN_Desc = orm.mapped_column(sqlalchemy.String(30), nullable=True)
    CTOPP_Date = orm.mapped_column(sqlalchemy.Date, nullable=True)

    # GFTA scores
    GFTA_SIW_standard = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GFTA_SIW_percentile = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GFTA_Date = orm.mapped_column(sqlalchemy.Date, nullable=True)

    # Behavioral assessment scores
    ASSQ_Total = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_AG = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_FR = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_HY = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_IN = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_LP = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    C3SR_NI = orm.mapped_column(sqlalchemy.String(1), nullable=True)
    C3SR_PI = orm.mapped_column(sqlalchemy.String(1), nullable=True)

    # CBCL scores
    CBCL_AB = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_AD = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_AP = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_Ext = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_Int = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_RBB = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_SC = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_SP = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_Total = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_TP = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CBCL_WD = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Preschool scores
    Pre_APT = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Pre_ExternT = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Pre_InterT = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Pre_SCT = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Pre_SPT = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Pre_WDT = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Pre_ABT = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Pre_ADT = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Pre_TotalT = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Pre_ERT = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # SNAP scores
    SNAP_HY = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    SNAP_IN = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    SNAP_total = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)

    # SCARED scores - Parent report
    SCARED_PN = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SC = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SH = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_SP = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_Total = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SCARED_GD = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # SCARED scores - Child report
    Child_GD = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Child_PN = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Child_SC = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Child_SH = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Child_SP = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Child_Total = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # SCQ scores
    SCQ_Total = orm.mapped_column(sqlalchemy.String(5), nullable=True)
    SCQ_TotalScore = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # SRS scores
    SRS_AWR = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_COG = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_COM = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_MOT = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_RRB = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_Total = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # SRS Parent scores
    SRS_P_AWR = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_P_COG = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_P_COM = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_P_MOT = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_P_RRB = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SRS_P_Total = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # YSR scores
    YSR_AB = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_AD = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_AP = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_Ext = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_Int = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_RBB = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_SC = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_SP = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_TP = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_WD = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    YSR_Total = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # MFQ scores
    MFQ_P_Score = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MFQ_SR_Score = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # WISC percentiles and ranges
    BD_percentile_2 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    BD_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    Coding_percentile = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Coding_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    DS_percentile = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    DS_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    FRI_range = orm.mapped_column(sqlalchemy.String(52), nullable=True)
    FSIQ_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    FW_percentile = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    FW_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    MR_percentile = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    MR_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    PS_percentile = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    PS_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    PSI_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    similarities_percentile_2 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Similarities_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    SS_percentile = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    SS_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    VCI_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    Vocab_percentile = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Vocab_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    VP_percentile = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    VP_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    VSI_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WMI_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)

    # WIAT ranges
    LC_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    MP_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    Math_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    MF_Add_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    MF_Sub_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    MF_Mult_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    Numerical_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    Pseudoword_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    RC_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    Spelling_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    Word_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)

    # TOWRE standardized scores
    TOWRE_SWE_Stnd = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TOWRE_PDE_Stnd = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TOWRE_Total_Stnd = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Additional standardized scores
    EL_Standard = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    BW_Standard = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    NR_Standard = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    RD_Standard = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    RL_Standard = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    RO_Standard = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    RC_standard = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    celf_criterion = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    celf_total = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Pegboard scores
    Rank_NonDominant = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    Rank_Dominant = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    CELF_Date = orm.mapped_column(sqlalchemy.Date, nullable=True)
    Pegboard_Date = orm.mapped_column(sqlalchemy.Date, nullable=True)
    ZScore_NonDominant = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    ZScore_Dominant = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    GFTA_Range = orm.mapped_column(sqlalchemy.String(20), nullable=True)

    # ADHD and ESWAN scores
    ADHD_Clin_Avg = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    ESWAN_IN = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    ESWAN_HY = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)

    # Feedback text fields
    listening_custom_text = orm.mapped_column(sqlalchemy.String(500), nullable=True)
    mathematics_custom_text = orm.mapped_column(sqlalchemy.String(500), nullable=True)
    reading_comp_custom_text = orm.mapped_column(sqlalchemy.String(500), nullable=True)
    reading_custom_text = orm.mapped_column(sqlalchemy.String(500), nullable=True)
    written_custom_text = orm.mapped_column(sqlalchemy.String(500), nullable=True)
    feedback_adhd = orm.mapped_column(sqlalchemy.String(500), nullable=True)
    feedback_assq = orm.mapped_column(sqlalchemy.String(500), nullable=True)
    feedback_cbcl = orm.mapped_column(sqlalchemy.String(500), nullable=True)
    feedback_conners = orm.mapped_column(sqlalchemy.String(500), nullable=True)
    feedback_mfq = orm.mapped_column(sqlalchemy.String(500), nullable=True)
    feedback_scared = orm.mapped_column(sqlalchemy.String(500), nullable=True)
    feedback_srs = orm.mapped_column(sqlalchemy.String(500), nullable=True)
    feedback_swan = orm.mapped_column(sqlalchemy.String(500), nullable=True)
    feedback_ysr = orm.mapped_column(sqlalchemy.String(500), nullable=True)
    fri_custom_text = orm.mapped_column(sqlalchemy.String(1000), nullable=True)
    fsiq_custom_text = orm.mapped_column(sqlalchemy.String(1000), nullable=True)
    kbit_custom_text = orm.mapped_column(sqlalchemy.String(1000), nullable=True)
    psi_custom_text = orm.mapped_column(sqlalchemy.String(1000), nullable=True)
    vci_custom_text = orm.mapped_column(sqlalchemy.String(1000), nullable=True)
    vsi_custom_text = orm.mapped_column(sqlalchemy.String(1000), nullable=True)
    wmi_custom_text = orm.mapped_column(sqlalchemy.String(1000), nullable=True)
    feedback_attention = orm.mapped_column(sqlalchemy.String(500), nullable=True)
    feedback_exec = orm.mapped_column(sqlalchemy.String(500), nullable=True)
    feedback_fine_motor = orm.mapped_column(sqlalchemy.String(500), nullable=True)
    feedback_processing = orm.mapped_column(sqlalchemy.String(500), nullable=True)
    feedback_quotient = orm.mapped_column(sqlalchemy.String(500), nullable=True)
    feedback_wm = orm.mapped_column(sqlalchemy.String(500), nullable=True)
    feedback_articulation = orm.mapped_column(sqlalchemy.String(500), nullable=True)
    feedback_language = orm.mapped_column(sqlalchemy.String(500), nullable=True)
    feedback_phonology = orm.mapped_column(sqlalchemy.String(500), nullable=True)

    # Parent information
    P1_Prefix = orm.mapped_column(sqlalchemy.String(10), nullable=True)
    P1_Last_Name = orm.mapped_column(sqlalchemy.String(20), nullable=True)
    P2_Last_Name = orm.mapped_column(sqlalchemy.String(20), nullable=True)
    P2_Prefix = orm.mapped_column(sqlalchemy.String(10), nullable=True)

    # WASI scores
    WASI_BD_P = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WASI_BD_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WASI_BD_Stnd = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WASI_FSIQ = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WASI_FSIQ_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WASI_FSIQ_P = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WASI_PRI_P = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WASI_PRI = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WASI_VCI = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WASI_VCI_P = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WASI_MR_P = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WASI_MR_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    Matrix_Reasoning_StandardScore = orm.mapped_column(
        sqlalchemy.Integer,
        nullable=True,
    )
    WASI_PRI_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WASI_Sim_P = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WASI_Sim_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WASI_Sim_Stnd = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WASI_VCI_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WASI_Vocab_P = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WASI_Vocab_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WASI_Vocab_Stnd = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # WAIS scores
    WAIS_F_Length = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_B_Length = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_F_Raw = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_B_Raw = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_DS_Scale = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_Seq_Raw = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_Seq_Length = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_Code_Raw = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_Code_Scale = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_Sym_Raw = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_Sym_Scale = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_Proc = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_PSI_Comp = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_Code_Stnd = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_Sym_Stnd = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_Code_P = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WAIS_Sym_P = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WAIS_DS_Stnd = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_DS_P = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WAIS_DS_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WAIS_PSI_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WAIS_Code_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WAIS_Sym_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WAIS_PSI_P = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)

    # Vineland scores
    dls_standard = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    dls_rank = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    dls_desc = orm.mapped_column(sqlalchemy.String(20), nullable=True)
    comm_standard = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    comm_rank = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    comm_desc = orm.mapped_column(sqlalchemy.String(20), nullable=True)
    social_standard = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    social_rank = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    social_desc = orm.mapped_column(sqlalchemy.String(20), nullable=True)
    motor_standard = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    motor_rank = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    motor_desc = orm.mapped_column(sqlalchemy.String(20), nullable=True)
    comp_standard = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    comp_rank = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    comp_desc = orm.mapped_column(sqlalchemy.String(20), nullable=True)
    Range_NonDominant = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    Range_Dominant = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    VL_Date = orm.mapped_column(sqlalchemy.Date, nullable=True)
    Dominant_Hand = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Adult Self-Report
    ASR_AD = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_WD = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_SC = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_SP = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_TP = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_AP = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_RBB = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_AB = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_Ext = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_Total = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    ASR_Int = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Test validity flags
    GFTA_Valid = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    KBIT_Valid = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    NIH7_Valid = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WASI_Valid = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_Valid = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CTOPP_Valid = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    CELF_Valid = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TOWRE_Valid = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Peg_Valid = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_Valid = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Vineland_Valid = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # GAI scores
    GAI_Composite = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GAI_Percentile = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GAI_Range = orm.mapped_column(sqlalchemy.String(25), nullable=True)

    # WAIS-W scores
    WAIS_W_FSIQ = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_W_FSIQ_P = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_W_FSIQ_R = orm.mapped_column(sqlalchemy.String(140), nullable=True)
    WAIS_W_VCI = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_W_VCI_P = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_W_VCI_R = orm.mapped_column(sqlalchemy.String(140), nullable=True)
    WAIS_W_PRI = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_W_PRI_P = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_W_PRI_R = orm.mapped_column(sqlalchemy.String(140), nullable=True)
    WAIS_W_WMI = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_W_WMI_P = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_W_WMI_R = orm.mapped_column(sqlalchemy.String(140), nullable=True)
    WAIS_W_PSI = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_Winston_Date = orm.mapped_column(sqlalchemy.Date, nullable=True)
    WAIS_W_PSI_P = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_W_PSI_R = orm.mapped_column(sqlalchemy.String(140), nullable=True)
    GAI_FB = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # WAIS-W subtest scaled scores
    WAIS_W_BD_S = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_W_SIM_S = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_W_DS_S = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_W_MR_S = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_W_V_S = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_W_A_S = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_W_SS_S = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_W_VP_S = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_W_I_S = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_W_C_S = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # WAIS-W subtest percentiles
    WAIS_W_BD_P = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_W_SIM_P = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_W_DS_P = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_W_MR_P = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_W_V_P = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_W_A_P = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_W_SS_P = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_W_VP_P = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_W_I_P = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_W_C_P = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # WAIS-W subtest ranges
    WAIS_W_BD_R = orm.mapped_column(sqlalchemy.String(140), nullable=True)
    WAIS_W_SIM_R = orm.mapped_column(sqlalchemy.String(140), nullable=True)
    WAIS_W_DS_R = orm.mapped_column(sqlalchemy.String(140), nullable=True)
    WAIS_W_MR_R = orm.mapped_column(sqlalchemy.String(140), nullable=True)
    WAIS_W_V_R = orm.mapped_column(sqlalchemy.String(140), nullable=True)
    WAIS_W_A_R = orm.mapped_column(sqlalchemy.String(140), nullable=True)
    WAIS_W_SS_R = orm.mapped_column(sqlalchemy.String(140), nullable=True)
    WAIS_W_VP_R = orm.mapped_column(sqlalchemy.String(140), nullable=True)
    WAIS_W_I_R = orm.mapped_column(sqlalchemy.String(140), nullable=True)
    WAIS_W_C_R = orm.mapped_column(sqlalchemy.String(140), nullable=True)

    # WAIS-W GAI scores
    WAIS_W_GAI_Comp = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_W_GAI_P = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WAIS_W_GAI_R = orm.mapped_column(sqlalchemy.String(25), nullable=True)
    WAIS_W_GAI_FB = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Assessment flags
    other_gai = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    clin_review = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    gradenorm = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    NIH = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Vineland domain descriptors
    comm1_desc = orm.mapped_column(sqlalchemy.String(20), nullable=True)
    comm2_desc = orm.mapped_column(sqlalchemy.String(20), nullable=True)
    comm3_desc = orm.mapped_column(sqlalchemy.String(20), nullable=True)
    dls1_desc = orm.mapped_column(sqlalchemy.String(20), nullable=True)
    dls2_desc = orm.mapped_column(sqlalchemy.String(20), nullable=True)
    dls3_desc = orm.mapped_column(sqlalchemy.String(20), nullable=True)
    social1_desc = orm.mapped_column(sqlalchemy.String(20), nullable=True)
    social2_desc = orm.mapped_column(sqlalchemy.String(20), nullable=True)
    social3_desc = orm.mapped_column(sqlalchemy.String(20), nullable=True)
    motor1_desc = orm.mapped_column(sqlalchemy.String(20), nullable=True)
    motor2_desc = orm.mapped_column(sqlalchemy.String(20), nullable=True)

    # GARS scores
    GARS_AI = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_AI_Perc = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_AI_Prob_char = orm.mapped_column(sqlalchemy.String(100), nullable=True)
    GARS_AI_Sev = orm.mapped_column(sqlalchemy.String(100), nullable=True)
    GARS_CS_Scaled = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_CS_Perc = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_ER_Perc = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_ER_Scaled = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_MS_Perc = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_MS_Scaled = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_RB_Perc = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_RB_Scaled = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_SI_Perc = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_SI_Scaled = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_SC_Perc = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_SC_Scaled = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GARS_mute = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Remote WISC scores
    Remote_WISC_VCI = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Remote_WISC_VCI_Percentile = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Remtoe_WISC_VCI_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    Remote_WISC_NMVSI = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Remote_WISC_NMVSI_Percentile = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Remote_WISC_NMVSI_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    Remote_WISC_FRI = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Remote_FRI_Percentile = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Remote_FRI_Range = orm.mapped_column(sqlalchemy.String(52), nullable=True)
    Remote_WISC_WMI = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Remote_WISC_WMI_Percentile = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Remote_WISC_WMI_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    Remote_WISC_NSI = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Remote_WISC_NSI_Percentile = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Remote_NSI_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    Remote_WISC_NMFSIQ = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Remote_WISC_NMFSIQ_Percentile = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Remote_WISC_NMFSIQ_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    Remote_WISC_Similarities = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Remote_WISC_Similarities_Percentile = orm.mapped_column(
        sqlalchemy.Integer,
        nullable=True,
    )
    Remote_WISC_Similarities_Range = orm.mapped_column(
        sqlalchemy.String(50),
        nullable=True,
    )
    Remote_WISC_Vocab = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Remote_WISC_Vocab_Percentile = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Remote_WISC_Vocab_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    Remote_WISC_BD = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Remote_WISC_BD_Percentile = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Remote_WISC_BD_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    Remote_WISC_VP = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Remote_WISC_VP_Percentile = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Remote_WISC_VP_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    Remote_WISC_MR = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Remote_WISC_MR_Percentile = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Remote_WISC_MR_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    Remote_WISC_FW = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Remote_WISC_FW_Percentile = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Remote_WISC_FW_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    Remote_WISC_DS = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Remote_WISC_DS_Percentile = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Remote_WISC_DS_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    Remote_WISC_LNS = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Remote_WISC_LNS_Percentile = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Remote_WISC_LNS_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    Remote_WISC_NLS = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Remote_WISC_NLS_Percentile = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Remote_WISC_NLS_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    Remote_WISC_NSQ = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Remote_WISC_NSQ_Percentile = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Remote_WISC_SS_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    Remote_WISC_GAI = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Remote_WISC_GAI_Percentile = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Remote_WISC_GAI_range = orm.mapped_column(sqlalchemy.String(25), nullable=True)
    Remote_WISC_NSL_Stnd = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Remote_WISC_NSQ_Stnd = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Remote testing flags
    CTOPP_Remote = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TOWRE_Remote = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    GFTA_Remote = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WIAT_Remote = orm.mapped_column(sqlalchemy.Integer, nullable=False)
    Remote_WISC_Date = orm.mapped_column(sqlalchemy.Date, nullable=True)

    # TOWRE Grade Norm scores
    TOWRE_Scaled_GN = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TOWRE_Perc_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    TOWRE_Desc_GN = orm.mapped_column(sqlalchemy.String(20), nullable=True)
    TOWRE_SWE_Scaled_GN = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TOWRE_SWE_Perc_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    TOWRE_SWE_Desc_GN = orm.mapped_column(sqlalchemy.String(20), nullable=True)
    TOWRE_PDE_Scaled_GN = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TOWRE_PDE_Perc_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    TWORE_PED_Desc_GN = orm.mapped_column(sqlalchemy.String(20), nullable=True)

    # WIAT Grade Norm scores
    WIAT_Word_Stnd_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_Word_Perc_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_Word_Range_GN = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_Pseudo_Stnd_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_Pseudo_Perc_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_Pseudo_Range_GN = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_RC_Stnd_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_RC_Perc_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_RC_Range_GN = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_Spell_Stnd_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_Spell_Perc_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_Spell_Range_GN = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_Num_Stnd_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_Num_Perc_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_Num_Range_GN = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_Math_Stnd_GN = orm.mapped_column(sqlalchemy.DECIMAL(20, 6), nullable=True)
    WIAT_Math_Perc_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_Math_Range_GN = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_MF_Stnd_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_MF_Perc_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_MF_Range_GN = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_MF_Add_Stnd_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_MF_Add_Perc_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_MF_Add_Range_GN = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_MF_Sub_Stnd_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_MF_Sub_Perc_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_MF_Sub_Range_GN = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_MF_Mult_Stnd_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_MF_Mult_Perc_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_MF_Mult_Range_GN = orm.mapped_column(sqlalchemy.String(50), nullable=True)

    # WISC Abbreviated scores
    WISC_Abbr_VCI = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_Abbr_VCI_Perc = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_Abbr_VCI_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WISC_Abbr_FRI = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_Abbr_FRI_Perc = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_Abbr_FRI_range = orm.mapped_column(sqlalchemy.String(52), nullable=True)
    WISC_Abbr_FSIQ = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_Abbr_FSIQ_Perc = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_Abbr_FSIQ_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WISC_Abbr_Sim = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_Abbr_Sim_Perc = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_Abbr_Sim_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WISC_Abbr_Vocab = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_Abbr_Vocab_Perc = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_Abbr_Vocab_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WISC_Abbr_MR = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_Abbr_MR_Perc = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_Abbr_MR_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WISC_Abbr_FW = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_Abbr_FW_Perc = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_Abbr_FW_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WISC_Abbr_BD = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_Abbr_BD_Perc = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_Abbr_BD_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WISC_Abbr_DS = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_Abbr_DS_Perc = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_Abbr_DS_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WISC_Abbr_Coding = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_Abbr_Coding_Perc = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WISC_Abbr_Coding_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)

    # WIAT Abbreviated scores
    WIAT_Abbr_Word = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_Abbr_Word_Perc = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_Abbr_Word_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_Abbr_PW = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_Abbr_PW_Perc = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_Abbr_PW_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_Abbr_Spelling = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_Abbr_Spelling_Perc = orm.mapped_column(
        sqlalchemy.DECIMAL(16, 6),
        nullable=True,
    )
    WIAT_Abbr_Spelling_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_Abbr_Num = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_Abbr_Num_Perc = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_Abbr_Num_range = orm.mapped_column(sqlalchemy.String(50), nullable=True)

    # Visit flags
    TOWRE_Visit = orm.mapped_column(sqlalchemy.Integer, nullable=False)
    TOWRE_Visit_GradeNorm = orm.mapped_column(sqlalchemy.Integer, nullable=False)
    CELF_Visit = orm.mapped_column(sqlalchemy.Integer, nullable=False)

    # WIAT Abbreviated Grade Norm scores
    WIAT_Abbr_Word_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_Abbr_Word_Perc_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_Abbr_Word_range_GN = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_Abbr_PW_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_Abbr_PW_Perc_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_Abbr_PW_range_GN = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_Abbr_Spelling_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_Abbr_Spelling_Perc_GN = orm.mapped_column(
        sqlalchemy.DECIMAL(16, 6),
        nullable=True,
    )
    WIAT_Abbr_Spelling_range_GN = orm.mapped_column(
        sqlalchemy.String(50),
        nullable=True,
    )
    WIAT_Abrr_Num_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_Abbr_Num_Perc_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_Abbr_Num_range_GN = orm.mapped_column(sqlalchemy.String(50), nullable=True)

    # WIAT version and test status
    WIAT_Test_Number = orm.mapped_column(sqlalchemy.String(10), nullable=False)
    Full_WIAT = orm.mapped_column(sqlalchemy.Integer, nullable=False)
    WIAT_Screener = orm.mapped_column(sqlalchemy.Integer, nullable=False)
    WIAT_GN_Screener = orm.mapped_column(sqlalchemy.Integer, nullable=False)
    WIAT_Extended = orm.mapped_column(sqlalchemy.Integer, nullable=False)
    WIAT_GN_Extended = orm.mapped_column(sqlalchemy.Integer, nullable=False)

    # WIAT-4 scores
    WIAT_4_WR_Raw = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WIAT_4_WR_Std = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_4_WR_Perc = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_4_WR_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_4_Pseudo_Raw = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WIAT_4_Pseudo_Std = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_4_Pseudo_Perc = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_4_Pseudo_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_4_NO_Raw = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WIAT_4_NO_Std = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_4_NO_Perc = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_4_NO_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_4_Spell_Raw = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WIAT_4_Spell_Std = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_4_Spell_Perc = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_4_Spell_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_4_LC_Std = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_4_LC_Perc = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_4_LC_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_4_LC_ODC_Raw = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_4_LC_ODC_Std = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WIAT_4_LC_ODC_Perc = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_4_LC_ODC_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_4_LC_RV_Raw = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_4_LC_RV_Std = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WIAT_4_LC_RV_Perc = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_4_LC_RV_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_4_RC_Raw = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_4_RC_Std = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_4_RC_Perc = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_4_RC_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_4_MP_Raw = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_4_MP_Std = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_4_MP_Perc = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_4_MP_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_4_MF_Std = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_4_MF_Perc = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_4_MF_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_4_MF_Add_Raw = orm.mapped_column(sqlalchemy.DECIMAL(16, 5), nullable=True)
    WIAT_4_MF_Add_Std = orm.mapped_column(sqlalchemy.DECIMAL(16, 5), nullable=True)
    WIAT_4_MF_Add_Perc = orm.mapped_column(sqlalchemy.DECIMAL(16, 5), nullable=True)
    WIAT_4_MF_Add_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_4_MF_Sub_Raw = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_4_MF_Sub_Std = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_4_MF_Sub_Perc = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_4_MF_Sub_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_4_MF_Mult_Raw = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_4_MF_Mult_Std = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_4_MF_Mult_Perc = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_4_MF_Mult_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)

    # WIAT-4 Grade Norm scores
    WIAT_4_WR_Raw_GN = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WIAT_4_WR_Std_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_4_WR_Perc_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_4_WR_Range_GN = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_4_Pseudo_Raw_GN = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WIAT_4_Pseudo_Std_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_4_Pseudo_Perc_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_4_Pseudo_Range_GN = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_4_NO_Raw_GN = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WIAT_4_NO_Std_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_4_NO_Perc_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_4_NO_Range_GN = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_4_Spell_Raw_GN = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WIAT_4_Spell_Std_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_4_Spell_Perc_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_4_Spell_Range_GN = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_4_LC_Std_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_4_LC_Perc_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_4_LC_Range_GN = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_4_LC_ODC_Raw_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_4_LC_ODC_Std_GN = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WIAT_4_LC_ODC_Perc_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_4_LC_ODC_Range_GN = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_4_LC_RV_Raw_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_4_LC_RV_Std_GN = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WIAT_4_LC_RV_Perc_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_4_LC_RV_Range_GN = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_4_RC_Raw_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_4_RC_Std_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_4_RC_Perc_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_4_RC_Range_GN = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_4_MP_Raw_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_4_MP_Std_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_4_MP_Perc_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_4_MP_Range_GN = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_4_MF_Std_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_4_MF_Perc_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_4_MF_Range_GN = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_4_MF_Add_Raw_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_4_MF_Add_Std_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_4_MF_Add_Perc_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_4_MF_Add_Range_GN = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_4_MF_Sub_Raw_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_4_MF_Sub_Std_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_4_MF_Sub_Perc_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_4_MF_Sub_Range_GN = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_4_MF_Mult_Raw_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_4_MF_Mult_Std_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_4_MF_Mult_Perc_GN = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_4_MF_Mult_Range_GN = orm.mapped_column(sqlalchemy.String(50), nullable=True)

    # WIAT-3 scores
    WIAT_3_WR_Std = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_3_WR_Perc = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_3_WR_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_3_LC_Std = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_3_LC_Perc = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_3_LC_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_3_LC_ODC_Std = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WIAT_3_LC_ODC_Perc = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_3_LC_ODC_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_3_LC_RV_Std = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WIAT_3_LC_RV_Perc = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_3_LC_RV_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_3_RC_Std = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_3_RC_Perc = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_3_RC_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_3_Pseudo_Std = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_3_Pseudo_Perc = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_3_Pseudo_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_3_Spell_Std = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_3_Spell_Perc = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_3_Spell_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_3_NO_Std = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_3_NO_Perc = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_3_NO_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_3_MP_Std = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_3_MP_Perc = orm.mapped_column(sqlalchemy.DECIMAL(16, 2), nullable=True)
    WIAT_3_MP_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_3_MF_Std = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_3_MF_Perc = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_3_MF_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_3_MF_Add_Std = orm.mapped_column(sqlalchemy.DECIMAL(16, 5), nullable=True)
    WIAT_3_MF_Add_Perc = orm.mapped_column(sqlalchemy.DECIMAL(16, 5), nullable=True)
    WIAT_3_MF_Add_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_3_MF_Sub_Std = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_3_MF_Sub_Perc = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_3_MF_Sub_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_3_MF_Mult_Std = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_3_MF_Mult_Perc = orm.mapped_column(sqlalchemy.DECIMAL(16, 6), nullable=True)
    WIAT_3_MF_Mult_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)

    # WIAT Writing scores
    WIAT_EC_Std = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WIAT_EC_Perc = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WIAT_EC_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_SB_Std = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WIAT_SB_Perc = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WIAT_SB_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_SC_Std = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WIAT_SC_Perc = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WIAT_SC_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_SComp_Std = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WIAT_SComp_Perc = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WIAT_SComp_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)

    # WIAT Writing Grade Norm scores
    WIAT_GN_EC_Std = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WIAT_GN_EC_Perc = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WIAT_GN_EC_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_GN_SB_Std = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WIAT_GN_SB_Perc = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WIAT_GN_SB_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_GN_SC_Std = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WIAT_GN_SC_Perc = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WIAT_GN_SC_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)
    WIAT_GN_SComp_Std = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WIAT_GN_SComp_Perc = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    WIAT_GN_SComp_Range = orm.mapped_column(sqlalchemy.String(50), nullable=True)

    # Enrollment date
    Enroll_Date = orm.mapped_column(sqlalchemy.Date, nullable=True)


class Swan(Base):
    """SQLAlchemy model representing the I2B2_Export_SWAN_t table in the nextgen schema.

    This table stores the Strengths and Weaknesses of ADHD Symptoms and Normal Behavior
    (SWAN) assessment data.
    """

    __tablename__ = "I2B2_Export_SWAN_T"
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


class Trf(Base):
    """SQLAlchemy model representing the I2B2_Export_TRF table."""

    __tablename__ = "I2B2_Export_TRF_T"
    __table_args__ = {"schema": "nextgen"}  # noqa: RUF012

    URSI = orm.mapped_column(sqlalchemy.String(10), nullable=True)
    SiteID = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    RaterID = orm.mapped_column(sqlalchemy.String(4), nullable=True)
    SourceType = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    AssessmentStartDate = orm.mapped_column(sqlalchemy.String(10), nullable=True)
    AssessmentStartTime = orm.mapped_column(sqlalchemy.String(5), nullable=True)
    Successful = orm.mapped_column(sqlalchemy.String(1), nullable=True)
    EID = orm.mapped_column(sqlalchemy.String(15), nullable=True)
    START_DATE = orm.mapped_column(
        sqlalchemy.String(20), nullable=False, primary_key=True
    )
    Study = orm.mapped_column(sqlalchemy.String(3), nullable=True)
    Site = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Days_Baseline = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Year = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    Season = orm.mapped_column(sqlalchemy.String(6), nullable=False)

    # TRF items 1-55
    TRF_01 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_02 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_03 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_04 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_05 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_06 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_07 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_08 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_09 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_10 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_11 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_12 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_13 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_14 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_15 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_16 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_17 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_18 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_19 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_20 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_21 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_22 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_23 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_24 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_25 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_26 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_27 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_28 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_29 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_30 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_31 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_32 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_33 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_34 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_35 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_36 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_37 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_38 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_39 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_40 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_41 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_42 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_43 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_44 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_45 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_46 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_47 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_48 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_49 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_50 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_51 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_52 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_53 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_54 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_55 = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # TRF item 56 a-h
    TRF_56a = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_56b = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_56c = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_56d = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_56e = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_56f = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_56g = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_56h = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # TRF items 57-112
    TRF_57 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_58 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_59 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_60 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_61 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_62 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_63 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_64 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_65 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_66 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_67 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_68 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_69 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_70 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_71 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_72 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_73 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_74 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_75 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_76 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_77 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_78 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_79 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_80 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_81 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_82 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_83 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_84 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_85 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_86 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_87 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_88 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_89 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_90 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_91 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_92 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_93 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_94 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_95 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_96 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_97 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_98 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_99 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_100 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_101 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_102 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_103 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_104 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_105 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_106 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_107 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_108 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_109 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_110 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_111 = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_112 = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # TRF item 113 a-c
    TRF_113a = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_113b = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_113c = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # TRF syndrome scales and T scores
    TRF_AB = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_AB_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_AD = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_AD_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_AP = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_AP_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_RBB = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_RBB_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_SC = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_SC_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_SP = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_SP_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_TP = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_TP_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_WD = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_WD_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # TRF broad-band scales
    TRF_Ext = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_Ext_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_Int = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_Int_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_OP = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_Total = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_Total_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # TRF DSM-oriented scales
    TRF_DSM_ADHD = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_DSM_ADHD_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_DSM_DP = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_DSM_DP_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_DSM_AN = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_DSM_AN_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_DSM_CP = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_DSM_CP_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_DSM_OD = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_DSM_OD_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_DSM_SP = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_DSM_SP_T = orm.mapped_column(sqlalchemy.Integer, nullable=True)

    # Additional scales
    TRF_SCT = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_OCP = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    TRF_PTS = orm.mapped_column(sqlalchemy.Integer, nullable=True)
    row_id_by_person = orm.mapped_column(sqlalchemy.BigInteger, nullable=True)


class Wisc5(Base):
    """SQLAlchemy model representing I2B2_Export_WISC_V_t in the nextgen schema.

    This table stores Wechsler Intelligence Scale for Children (WISC-V) assessment data,
    including raw scores, scaled scores, indexes, and percentiles.
    """

    __tablename__ = "I2B2_Export_WISC_V_T"
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

    __tablename__ = "I2B2_Export_YSR_T"
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
