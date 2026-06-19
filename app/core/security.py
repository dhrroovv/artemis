from datetime import datetime, timedelta

import jwt
from pwdlib import PasswordHash

from app.core.config import get_settings

settings = get_settings()


class Passwords:
    password_hash = PasswordHash.recommended()

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return cls.password_hash.hash(password)

    @classmethod
    def verify_password(cls, password: str, hashed_password: str) -> bool:
        return cls.password_hash.verify(password, hashed_password)


class AccessToken:
    @classmethod
    def create_access_token(cls, user: dict[str, str], expiry: str | None = None):
        pass
