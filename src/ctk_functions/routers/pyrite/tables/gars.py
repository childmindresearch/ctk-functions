"""Module for inserting the Gilliam Autism Rating Scale table."""

import cmi_docx

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import base, utils

CLINICAL_RELEVANCE = [
    base.ClinicalRelevance(
        low=None,
        high=60,
        high_inclusive=False,
        label="typical range",
        style=cmi_docx.TableStyle(),
    ),
    base.ClinicalRelevance(
        low=60,
        high=75,
        low_inclusive=True,
        label="borderline range",
        style=cmi_docx.TableStyle(cmi_docx.ParagraphStyle(bold=True)),
    ),
    base.ClinicalRelevance(
        low=75,
        high=None,
        label="clinically relevant impairment",
        style=cmi_docx.TableStyle(
            cmi_docx.ParagraphStyle(font_rgb=(255, 0, 0)),
        ),
    ),
]


class GarsDataSource(base.DataProducer):
    """Fetches the GARS table data."""

    def fetch(self, mrn: str) -> base.WordTableMarkup:
        """Fetches the GARS data for a given mrn.

        Args:
            mrn: The participant's unique identifier.

        Returns:
            The markup for the Word table.
        """
        data = utils.fetch_participant_row(mrn, models.Gars)

        formatter = base.Formatter(
            conditional_styles=[
                base.ConditionalStyle(
                    condition=rele.in_range,
                    style=rele.style,
                )
                for rele in CLINICAL_RELEVANCE
            ],
        )
        header = [
            base.WordTableCell(content="Autism Index Score"),
            base.WordTableCell(content="Percentile Rank"),
            base.WordTableCell(content="Autism Index Interpretation"),
        ]
        content_row = [
            base.WordTableCell(content=str(data.GARS_AI), formatter=formatter),
            base.WordTableCell(content=str(data.GARS_AI_Perc)),
            base.WordTableCell(
                content="\n".join(str(rele) for rele in CLINICAL_RELEVANCE),
            ),
        ]

        return base.WordTableMarkup(rows=[header, content_row])
