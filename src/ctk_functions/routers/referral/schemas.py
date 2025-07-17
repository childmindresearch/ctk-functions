"""Schemas for the referral endpoints."""

import pydantic


class PostReferralTable(pydantic.BaseModel):
    """Represents a table in the referral document.

    Property names are the header strings; capital letters are
    intentional.

    """

    model_config = pydantic.ConfigDict(frozen=True)

    Name: tuple[str, ...]
    Addresses: tuple[str, ...]
    Insurance: tuple[str, ...]


class PostReferralTableSection(pydantic.BaseModel):
    """POST schema for referral documents."""

    model_config = pydantic.ConfigDict(frozen=True)

    title: str
    table: PostReferralTable


class PostReferralRequest(pydantic.BaseModel):
    """POST schema for referral documents."""

    model_config = pydantic.ConfigDict(frozen=True)

    tables: tuple[PostReferralTableSection, ...]
