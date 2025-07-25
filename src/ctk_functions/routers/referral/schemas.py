"""Schemas for the referral endpoints."""

import pydantic


class PostReferralTableSection(pydantic.BaseModel):
    """POST schema for referral documents."""

    model_config = pydantic.ConfigDict(frozen=True)

    title: str
    table: dict[str, tuple[str, ...]]


class PostReferralRequest(pydantic.BaseModel):
    """POST schema for referral documents."""

    model_config = pydantic.ConfigDict(frozen=True)

    tables: tuple[PostReferralTableSection, ...]
