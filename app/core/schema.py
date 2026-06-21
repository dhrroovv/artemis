import re
import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator

"""
Ideally all the pydantic models should be kept in \
a separate subdirectory app/schemas \
But since we would not be applying versioning and will try to not make \
many schemas, as that would only create fuss, I am keeping all the \
models inside app/core.
"""


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8)  # If not met, will raise 422 error
    """
    Status code 422 means Unprocessable entity \
    Server understands the payload and is structurally correct, \
    but may be due to validation error / business logic, cant be processed
    """

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        if not re.fullmatch(r"[a-zA-Z0-9_]+", value):
            raise ValueError(
                "Username not allowed. Username can only contain letter and underscore."
            )
        return value


class UserCreateResponse(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    created_at: datetime
    updated_at: datetime


class UserAuthenticatedResponse(BaseModel):
    id: uuid.UUID
    username: str
    email: EmailStr


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str
