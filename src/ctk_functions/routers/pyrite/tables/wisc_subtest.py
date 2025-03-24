"""Module for the WISC subtest table."""

import dataclasses
import functools
from typing import TYPE_CHECKING

import fastapi
import sqlalchemy
from docx import document
from starlette import status

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import base

if TYPE_CHECKING:
    from collections.abc import Callable


@dataclasses.dataclass
class WiscSubtestRowLabels:
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
    WiscSubtestRowLabels(
        scale="Verbal Comprehension",
        subtest="Similarities*",
        score_column="WISC_Similarities_Scaled",
    ),
    WiscSubtestRowLabels(
        scale="Verbal Comprehension",
        subtest="Vocabulary*",
        score_column="WISC_Vocab_Scaled",
    ),
    WiscSubtestRowLabels(
        scale="Visual Spatial",
        subtest="Block Design*",
        score_column="WISC_BD_Scaled",
    ),
    WiscSubtestRowLabels(
        scale="Visual Spatial",
        subtest="Visual Puzzles",
        score_column="WISC_VP_Scaled",
    ),
    WiscSubtestRowLabels(
        scale="Fluid Reasoning",
        subtest="Matrix Reasoning*",
        score_column="WISC_MR_Scaled",
    ),
    WiscSubtestRowLabels(
        scale="Fluid Reasoning",
        subtest="Figure Weights*",
        score_column="WISC_FW_Scaled",
    ),
    WiscSubtestRowLabels(
        scale="Working Memory",
        subtest="Digit Span*",
        score_column="WISC_DS_Scaled",
    ),
    WiscSubtestRowLabels(
        scale="Working Memory",
        subtest="Picture Span",
        score_column="WISC_PS_Scaled",
    ),
    WiscSubtestRowLabels(
        scale="Processing Speed",
        subtest="Coding*",
        score_column="WISC_Coding_Scaled",
    ),
    WiscSubtestRowLabels(
        scale="Processing Speed",
        subtest="Symbol Search",
        score_column="WISC_SS_Scaled",
    ),
)


class WiscSubtest(base.PyriteBaseTable):
    """The WISC subtest table."""

    def add(self, doc: document.Document) -> None:
        """Adds the WISC subtest table to the document.

        Args:
            doc: The Word document.
        """
        data_source: base.SqlDataSource[models.Wisc5] = base.SqlDataSource(
            query=sqlalchemy.select(models.Wisc5).where(models.Wisc5.EID == self.eid),
        )
        header: list[base.TableCell[str]] = [
            base.TableCell(content="Scale"),
            base.TableCell(content="Subtest"),
            base.TableCell(content="Scaled Score"),
            base.TableCell(content="Percentile"),
            base.TableCell(content="Range"),
        ]
        content_rows: list[
            list[base.TableCell[str | Callable[[models.Wisc5], str]]]
        ] = [
            [
                base.TableCell(content=label.scale),
                base.TableCell(content=label.subtest),
                base.TableCell(
                    content=functools.partial(
                        lambda row, lbl: getattr(row, lbl.score_column),
                        lbl=label,
                    ),
                ),
                base.TableCell(
                    content=functools.partial(
                        lambda row, lbl: _wisc_subtest_scaled_score_to_percentile(
                            getattr(row, lbl.score_column),
                        ),
                        lbl=label,
                    ),
                ),
                base.TableCell(
                    content=functools.partial(
                        lambda row, lbl: _wisc_subtest_scaled_score_to_qualifier(
                            getattr(row, lbl.score_column),
                        ),
                        lbl=label,
                    ),
                ),
            ]
            for label in WISC_SUBTEST_ROW_LABELS
        ]
        template = [header, *content_rows]
        base.WordDocumentTableRenderer(
            data_source=data_source,
            template_rows=template,
        ).add(doc)


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
