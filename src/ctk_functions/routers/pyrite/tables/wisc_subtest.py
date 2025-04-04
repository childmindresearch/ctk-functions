"""Module for the WISC subtest table."""

import dataclasses
import functools

import cmi_docx
import fastapi
from docx import shared
from starlette import status

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import base, utils


@dataclasses.dataclass
class _WiscSubtestRowLabels:
    """Class definition for subtest rows.

    Attributes:
        scale: Name of the scale, used in first column.
        subtest: Name of the subtest, used in second column.
        score_column: The column in the SQL database.
    """

    scale: str
    subtest: str
    score_column: str


WISC_SUBTEST_ROW_LABELS = (
    _WiscSubtestRowLabels(
        scale="Verbal Comprehension",
        subtest="Similarities*",
        score_column="WISC_Similarities_Scaled",
    ),
    _WiscSubtestRowLabels(
        scale="Verbal Comprehension",
        subtest="Vocabulary*",
        score_column="WISC_Vocab_Scaled",
    ),
    _WiscSubtestRowLabels(
        scale="Visual Spatial",
        subtest="Block Design*",
        score_column="WISC_BD_Scaled",
    ),
    _WiscSubtestRowLabels(
        scale="Visual Spatial",
        subtest="Visual Puzzles",
        score_column="WISC_VP_Scaled",
    ),
    _WiscSubtestRowLabels(
        scale="Fluid Reasoning",
        subtest="Matrix Reasoning*",
        score_column="WISC_MR_Scaled",
    ),
    _WiscSubtestRowLabels(
        scale="Fluid Reasoning",
        subtest="Figure Weights*",
        score_column="WISC_FW_Scaled",
    ),
    _WiscSubtestRowLabels(
        scale="Working Memory",
        subtest="Digit Span*",
        score_column="WISC_DS_Scaled",
    ),
    _WiscSubtestRowLabels(
        scale="Working Memory",
        subtest="Picture Span",
        score_column="WISC_PS_Scaled",
    ),
    _WiscSubtestRowLabels(
        scale="Processing Speed",
        subtest="Coding*",
        score_column="WISC_Coding_Scaled",
    ),
    _WiscSubtestRowLabels(
        scale="Processing Speed",
        subtest="Symbol Search",
        score_column="WISC_SS_Scaled",
    ),
)


class _WiscSubtestDataSource(base.DataProducer):
    """Fetches the data for the WISC table."""

    @classmethod
    @functools.lru_cache
    def fetch(cls, mrn: str) -> base.WordTableMarkup:
        """Fetches the WISC data for a given mrn.

        Args:
            mrn: The participant's unique identifier.

        Returns:
            The markup for the Word table.
        """
        data = utils.fetch_participant_row("EID", mrn, models.Wisc5)
        column_widths = (
            shared.Cm(4.42),
            shared.Cm(3.58),
            shared.Cm(3),
            shared.Cm(2.3),
            shared.Cm(3.21),
        )
        header_formatters = [base.Formatter(width=width) for width in column_widths]

        header = [
            base.WordTableCell(content="Scale", formatter=header_formatters[0]),
            base.WordTableCell(content="Subtest", formatter=header_formatters[1]),
            base.WordTableCell(content="Scaled Score", formatter=header_formatters[2]),
            base.WordTableCell(content="Percentile", formatter=header_formatters[3]),
            base.WordTableCell(content="Range", formatter=header_formatters[4]),
        ]

        body_formatters = [base.Formatter(width=width) for width in column_widths]
        body_formatters[0].merge_top = True
        content_rows = [
            [
                base.WordTableCell(content=label.scale, formatter=body_formatters[0]),
                base.WordTableCell(content=label.subtest, formatter=body_formatters[1]),
                base.WordTableCell(
                    content=getattr(data, label.score_column),
                    formatter=body_formatters[2],
                ),
                base.WordTableCell(
                    content=str(
                        _wisc_subtest_scaled_score_to_percentile(
                            getattr(data, label.score_column),
                        ),
                    ),
                    formatter=body_formatters[3],
                ),
                base.WordTableCell(
                    content=str(
                        _wisc_subtest_scaled_score_to_qualifier(
                            getattr(data, label.score_column),
                        ),
                    ),
                    formatter=body_formatters[4],
                ),
            ]
            for label in WISC_SUBTEST_ROW_LABELS
        ]
        return base.WordTableMarkup(rows=[header, *content_rows])


class WiscSubtestTable(base.WordTableSectionAddToMixin, base.WordTableSection):
    """Renderer for the WISC subtest table."""

    def __init__(self, mrn: str) -> None:
        """Initializes the WISC subtest renderer.

        Args:
            mrn: The participant's unique identifier.'
        """
        self.mrn = mrn
        self.postamble = [
            base.ParagraphBlock(
                content="*Subtests used to derive the Full Scale IQ (FSIQ)",
                style=cmi_docx.ParagraphStyle(italic=True),
            ),
        ]
        self.data_source = _WiscSubtestDataSource


def _wisc_subtest_scaled_score_to_qualifier(scaled: int) -> str:
    if scaled <= 1:
        return "extremely low"
    if scaled >= 18:  # noqa: PLR2004
        return "extremely high"

    mapping = {
        1: "extremely low",
        2: "very low",
        3: "very low",
        4: "low",
        5: "low",
        6: "low average",
        7: "low average",
        8: "average",
        9: "average",
        10: "average",
        11: "average",
        12: "high average",
        13: "high average",
        14: "high",
        15: "high",
        16: "very high",
        17: "very high",
    }

    if scaled in mapping:
        return mapping[scaled]
    raise fastapi.HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Unknown WISC subtest score.",
    )


def _wisc_subtest_scaled_score_to_percentile(scale: int) -> int:
    """Converts WISC subtest scores to percentiles."""
    if scale > 16:  # noqa: PLR2004
        return 99
    mapping = {
        1: 1,
        2: 1,
        3: 1,
        4: 2,
        5: 5,
        6: 9,
        7: 16,
        8: 25,
        9: 37,
        10: 50,
        11: 63,
        12: 75,
        13: 84,
        14: 91,
        15: 95,
        16: 98,
    }
    if scale in mapping:
        return mapping[scale]

    raise fastapi.HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Unknown WISC subtest score.",
    )
