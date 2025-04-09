"""Module for inserting the Gilliam Autism Rating Scale table."""

import functools

import cmi_docx
from docx import shared

from ctk_functions.microservices.sql import models
from ctk_functions.routers.pyrite.tables import base, utils

COLUMN_WIDTHS = (shared.Cm(4.74), shared.Cm(5), shared.Cm(6.75))


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


class _GarsDataSource(base.DataProducer):
    """Fetches the GARS table data."""

    @classmethod
    @functools.lru_cache
    def fetch(cls, mrn: str) -> base.WordTableMarkup:
        """Fetches the GARS data for a given mrn.

        Args:
            mrn: The participant's unique identifier.

        Returns:
            The markup for the Word table.
        """
        data = utils.fetch_participant_row("EID", mrn, models.Gars)

        formatters = [base.Formatter(width=width) for width in COLUMN_WIDTHS]
        formatters[0].conditional_styles.extend(
            [
                base.ConditionalStyle(
                    condition=rele.in_range,
                    style=rele.style,
                )
                for rele in CLINICAL_RELEVANCE
            ],
        )
        header = [
            base.WordTableCell(content="Autism Index Score", formatter=formatters[0]),
            base.WordTableCell(content="Percentile Rank", formatter=formatters[1]),
            base.WordTableCell(
                content="Autism Index Interpretation", formatter=formatters[2]
            ),
        ]
        content_row = [
            base.WordTableCell(content=str(data.GARS_AI), formatter=formatters[0]),
            base.WordTableCell(content=str(data.GARS_AI_Perc), formatter=formatters[1]),
            base.WordTableCell(
                content="\n".join(str(rele) for rele in CLINICAL_RELEVANCE),
                formatter=formatters[2],
            ),
        ]

        return base.WordTableMarkup(rows=[header, content_row])


class GarsTable(base.WordTableSectionAddToMixin, base.WordTableSection):
    """Renderer for the Gars table."""

    def __init__(self, mrn: str) -> None:
        """Initializes the Gars renderer.

        Args:
            mrn: The participant's unique identifier.'
        """
        postamble = (
            "*Caution is advised in interpretation of the Autism Index "
            "score, because individuals with other diagnoses including ADHD, "
            "ODD, anxiety, language disorder, and intellectual disability, "
            "may demonstrate behaviors typical of individuals diagnosed with "
            "autism. Thus, clinically elevated scores on this assessment are not "
            "necessarily indicative of an autism diagnosis."
        )
        self.mrn = mrn
        self.postamble = [base.ParagraphBlock(content=postamble)]
        self.data_source = _GarsDataSource
