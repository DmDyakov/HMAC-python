"""Module with models."""

from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints

MsgField = Annotated[
    str,
    StringConstraints(min_length=1),
    Field(description='Message to sign'),
]

SignatureField = Annotated[
    str,
    StringConstraints(min_length=1),
    Field(description='Base64url-encoded signature'),
]


class SignRequest(BaseModel):
    """Model for /sign request."""

    msg: MsgField


class VerifyRequest(BaseModel):
    """Model for /verify request."""

    msg: MsgField
    signature: SignatureField


class SignResponse(BaseModel):
    """Model for /sign response."""

    signature: str


class VerifyResponse(BaseModel):
    """Model for /verify response."""

    ok: bool
