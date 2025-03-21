import sqlalchemy
from sqlalchemy import orm


class Base(orm.DeclarativeBase):
    pass


class Wisc_5(Base):
    """SQLAlchemy model representing the I2B2_Export_WISC_V_t table in the nextgen schema.

    This table stores Wechsler Intelligence Scale for Children (WISC-V) assessment data,
    including raw scores, scaled scores, indexes, and percentiles.
    """

    __tablename__ = "I2B2_Export_WISC_V_t"
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
