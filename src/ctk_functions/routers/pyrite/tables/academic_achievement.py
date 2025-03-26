"""Module for inserting the academic achievement table."""

import dataclasses

import sqlalchemy
from docx import document

from ctk_functions.microservices.sql import client, models
from ctk_functions.routers.pyrite.tables import base, utils


@dataclasses.dataclass
class AcademicRowLabels:
    """Class definition for subtest rows.

    Attributes:
        domain: The domain of the WIAT subtest.
        subtest: Name of the subtest, used in second column.
        score_column: The label for standard score in the SQL data.
        percentile: The label for percentile in the SQL data.
    """

    domain: str
    subtest: str
    score_column: str
    percentile: str


# Defines the rows and their order of appearance.
ACADEMIC_ROW_LABELS = (
    AcademicRowLabels(
        domain="Reading",
        subtest="WIAT-4 Word Reading",
        score_column="WIAT_Word_Stnd",
        percentile="WIAT_Word_P",
    ),
    AcademicRowLabels(
        domain="Reading",
        subtest="WIAT-4 Pseudoword Decoding",
        score_column="WIAT_Pseudo_Stnd",
        percentile="WIAT_Pseudo_P",
    ),
    AcademicRowLabels(
        domain="Reading",
        subtest="WIAT-4 Reading Comprehension",
        score_column="WIAT_RC_Stnd",
        percentile="WIAT_RC_P",
    ),
    AcademicRowLabels(
        domain="Reading",
        subtest="TOWRE-II Total Word Reading Efficiency",
        score_column="TOWRE_Total_Scaled",
        percentile="TOWRE_Total_Perc",
    ),
    AcademicRowLabels(
        domain="Reading",
        subtest="TOWRE-II Sight Word Efficiency",
        score_column="TOWRE_SWE_Scaled",
        percentile="TOWRE_SWE_Perc",
    ),
    AcademicRowLabels(
        domain="Reading",
        subtest="TOWRE-II Phonemic Decoding Efficiency",
        score_column="TOWRE_PDE_Scaled",
        percentile="TOWRE_PDE_Perc",
    ),
    AcademicRowLabels(
        domain="Writing",
        subtest="WIAT-4 Sentence Composition",
        score_column="XXX",
        percentile="XXX",
    ),
    AcademicRowLabels(
        domain="Writing",
        subtest="Sentence Building",
        score_column="XXX",
        percentile="XXX",
    ),
    AcademicRowLabels(
        domain="Writing",
        subtest="Sentence Combining",
        score_column="XXX",
        percentile="XXX",
    ),
    AcademicRowLabels(
        domain="Writing",
        subtest="WIAT-4 Essay Composition",
        score_column="XXX",
        percentile="XXX",
    ),
    AcademicRowLabels(
        domain="Writing",
        subtest="WIAT-4 Spelling",
        score_column="WIAT_Spell_Stnd",
        percentile="WIAT_Spell_P",
    ),
    AcademicRowLabels(
        domain="Math",
        subtest="WIAT-4 Numerical Operations",
        score_column="WIAT_Num_Stnd",
        percentile="WIAT_Num_P",
    ),
    AcademicRowLabels(
        domain="Math",
        subtest="WIAT-4 Math Problem Solving",
        score_column="WIAT_MP_Stnd",
        percentile="WIAT_MP_P",
    ),
    AcademicRowLabels(
        domain="Math",
        subtest="WIAT-4 Math Fluency",
        score_column="XXX",
        percentile="XXX",
    ),
    AcademicRowLabels(
        domain="Math",
        subtest="Math Fluency - Addition",
        score_column="XXX",
        percentile="XXX",
    ),
    AcademicRowLabels(
        domain="Math",
        subtest="Math Fluency - Subtraction",
        score_column="XXX",
        percentile="XXX",
    ),
    AcademicRowLabels(
        domain="Math",
        subtest="Math Fluency - Multiplication",
        score_column="XXX",
        percentile="XXX",
    ),
)


class AcademicAchievementDataSource(base.DataProducer):
    """Fetches the data for the academic achievement table."""

    def fetch(self, mrn: str) -> base.WordTableMarkup:
        """Fetches the academic achievement data for a given mrn.

        Args:
            mrn: The participant's unique identifier.

        Returns:
            The markup for the Word table.
        """
        eid = utils.mrn_to_eid(mrn)
        statement = (
            sqlalchemy.select(
                models.Wiat,
                models.Towre,
            )
            .where(
                models.Wiat.EID == eid,
            )
            .outerjoin(
                models.Towre,
                models.Wiat.EID == models.Towre.EID,
            )
        )
        with client.get_session() as session:
            data = session.execute(statement).fetchone()
        if data is None:
            msg = "Data not found."
            raise utils.TableDataNotFoundError(msg)

        header = [
            base.WordTableCell(content="Domain"),
            base.WordTableCell(content="Subtest"),
            base.WordTableCell(content="Standard Score"),
            base.WordTableCell(content="Percentile"),
            base.WordTableCell(content="Range"),
        ]
        content_rows = []
        for label in ACADEMIC_ROW_LABELS:
            domain_cell = base.WordTableCell(content=label.domain, formatter=base.Formatter(merge_top=True))
            subtest_cell = base.WordTableCell(content=label.subtest)
            if label.score_column == "XXX":
                # TODO: Remove once all columns are found.
                score_cell = base.WordTableCell(content="Unknown")
                percentile_cell = base.WordTableCell(content="Unknown")
                range_cell = base.WordTableCell(content="Unknown")
            else:
                data_index = label.score_column.startswith("TOWRE")
                score = float(getattr(data[data_index], label.score_column))
                percentile = utils.normal_score_to_percentile(score, mean=100, std=15)
                qualifier = utils.standard_score_to_qualifier(score)
                score_cell = base.WordTableCell(content=f"{score:.0f}")
                percentile_cell = base.WordTableCell(content=f"{percentile:.0f}")
                range_cell = base.WordTableCell(content=qualifier)
            content_rows.append(
                (domain_cell, subtest_cell, score_cell, percentile_cell, range_cell),
            )

        return base.WordTableMarkup(rows=[header, *content_rows])


class AcademicAchievementTable(base.WordTableSection):
    """Renderer for the Academic Achievement composite table."""

    def __init__(self, mrn: str) -> None:
        """Initializes the Academic Achievement renderer.

        Args:
            mrn: The participant's unique identifier.'
        """
        markup = AcademicAchievementDataSource().fetch(mrn)
        preamble = [
            base.ParagraphBlock(
                content="Academic Achievement",
                level=utils.TABLE_TITLE_LEVEL,
            ),
            base.ParagraphBlock(content="Age Norms:"),
        ]
        table_renderer = base.WordDocumentTableRenderer(markup=markup)
        self.renderer = base.WordDocumentTableSectionRenderer(
            preamble=preamble,
            table_renderer=table_renderer,
        )

    def add_to(self, doc: document.Document) -> None:
        """Adds the Academic Achievement table to the document."""
        self.renderer.add_to(doc)
