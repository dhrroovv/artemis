import re

from pydantic import BaseModel, EmailStr, Field, field_validator

"""
Ideally all the pydantic models should be kept in \
a separate subdirectory app/schemas \
But since we would not be applying versioning and will try to not make \
many schemas, as that would only create fuss, I am keeping all the \
models inside app/core.
"""


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=12)
    email: EmailStr
    password: str = Field(min_length=8)  # If not met, will raise 422 error

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        if not re.fullmatch(r"[a-zA-Z0-9_]+", value):
            raise ValueError(
                "Username not allowed. Username can only contain letter and underscore."
            )
        return value
