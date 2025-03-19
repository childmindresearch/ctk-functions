"""Module for the WISC subtest table."""

import dataclasses
from typing import Any

import cmi_docx
import fastapi
import sqlalchemy
from docx import document
from starlette import status

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import base, utils


@dataclasses.dataclass
class SubTestRowLabels:
    """Class definition for subtest rows.

    Attributes:
        scale: Name of the scale, used in first column.
        subtest: Name of the subtest, used in second column.
        label: The label in the SQL database.
    """

    scale: str
    subtest: str
    label: str


SUBTEST_ROW_LABELS = (
    SubTestRowLabels(
        scale="Verbal Comprehension",
        subtest="Similarities*",
        label="Similarities",
    ),
    SubTestRowLabels(
        scale="Verbal Comprehension",
        subtest="Vocabulary*",
        label="Vocab",
    ),
    SubTestRowLabels(scale="Visual Spatial", subtest="Block Design*", label="BD"),
    SubTestRowLabels(scale="Visual Spatial", subtest="Visual Puzzles", label="VP"),
    SubTestRowLabels(
        scale="Fluid Reasoning",
        subtest="Matrix Reasoning*",
        label="MR",
    ),
    SubTestRowLabels(
        scale="Fluid Reasoning",
        subtest="Figure Weights*",
        label="FW",
    ),
    SubTestRowLabels(scale="Working Memory", subtest="Digit Span*", label="DS"),
    SubTestRowLabels(scale="Working Memory", subtest="Picture Span", label="PS"),
    SubTestRowLabels(scale="Processing Speed", subtest="Coding*", label="Coding"),
    SubTestRowLabels(scale="Processing Speed", subtest="Symbol Search", label="SS"),
)


class WiscSubtest(base.BaseTable):
    """Fetches data for and creates the WISC subtest table."""

    _title = None

    @property
    def _statement(self) -> sqlalchemy.Select[tuple[Any, ...]]:
        return sqlalchemy.select(models.t_I2B2_Export_WISC_V_t).where(
            self.eid == models.t_I2B2_Export_WISC_V_t.c.EID,  # type: ignore[arg-type]
        )

    def _add(
        self,
        doc: document.Document,
    ) -> None:
        """Adds the WISC subtest table to the report."""
        header_texts = [
            "Scale",
            "Subtest",
            "Scaled Score",
            "Percentile",
            "Range",
        ]
        table = doc.add_table(len(SUBTEST_ROW_LABELS) + 1, len(header_texts))
        table.style = utils.TABLE_STYLE
        utils.add_header(table, header_texts)
        for index, label in enumerate(SUBTEST_ROW_LABELS):
            prev_row = table.rows[index].cells
            row = table.rows[index + 1].cells
            if prev_row[0].text == label.scale:
                prev_row[0].merge(row[0])
            else:
                row[0].text = label.scale
            row[1].text = label.subtest

            score = getattr(self.data_no_none, f"WISC_{label.label}_Scaled")
            row[2].text = str(score)
            row[3].text = str(_wisc_subtest_scaled_score_to_percentile(score))
            row[4].text = _wisc_subtest_scaled_score_to_qualifier(score)

        para = doc.add_paragraph(
            "*Subtests used to derive the Full Scale IQ (FSIQ).",
        )
        cmi_docx.ExtendParagraph(para).format(cmi_docx.ParagraphStyle(italic=True))


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

    return mapping[scaled]


def _wisc_subtest_scaled_score_to_percentile(scale: int) -> int:
    """Converts WISC subtest scores to percentiles."""
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
        17: 99,
        18: 99,
        19: 99,
        20: 99,
    }
    if scale in mapping:
        return mapping[scale]

    raise fastapi.HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Unknown WISC subtest score.",
    )
