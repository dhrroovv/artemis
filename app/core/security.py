import uuid
from datetime import datetime, timedelta
from typing import Any

import jwt
from pwdlib import PasswordHash

from app.core.config import get_settings
from app.core.logger import get_logger

settings = get_settings()
logger = get_logger(__name__)


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
    def create_access_token(
        cls,
        user: dict[str, str],
        td: timedelta = settings.ACCESS_TOKEN_EXPIRY,
        refresh: bool = False,
    ) -> str:
        payload = {}
        payload["user"] = user
        payload["exp"] = datetime.now() + td
        payload["jti"] = str(uuid.uuid4())  # JWT Id
        payload["refresh"] = refresh  # whether access/session token
        token = jwt.encode(
            payload=payload,
            algorithm=settings.JWT_ALGORITHM,
            key=settings.JWT_SECRET_KEY,
        )
        return token

    @classmethod
    def decode_token(cls, token: str) -> dict[str, Any]:
        try:
            token_data = jwt.decode(
                jwt=token,
                key=settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
            return token_data
        except jwt.PyJWTError as e:
            logger.warning(f"JWT decode failed: {e}")
            raise
