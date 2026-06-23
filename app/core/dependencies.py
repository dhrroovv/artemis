import uuid
from typing import Annotated, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyCookie, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.logger import get_logger
from app.core.security import AccessToken
from app.db.session import get_db
from app.services.auth_service import UserAuthService

settings = get_settings()
logger = get_logger(__name__)

bearer_scheme = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
    session: Annotated[AsyncSession, Depends(get_db)],
    auth_service: Annotated[UserAuthService, Depends()],
) -> Any:
    token = credentials.credentials  # Actual JWT string
    """
    scheme = credentials.scheme
    This would return `Bearer`
    """

    try:
        jwt_data = AccessToken.decode_token(token)
        if jwt_data.get("refresh") is True:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token"
            )
        """
        pyjwt's decode itself handles expiry claim as well
        """
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    user_data = jwt_data.get("user")
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload"
        )

    uid = user_data.get("uid")
    user = await auth_service.get_user_by_id(uuid.UUID(uid), session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return user


cookie_scheme = APIKeyCookie(name="refresh_token")


async def refresh_current_token(
    refresh_token: Annotated[str, Depends(cookie_scheme)],
    session: Annotated[AsyncSession, Depends(get_db)],
    auth_service: Annotated[UserAuthService, Depends()],
) -> str:
    try:
        token_data = AccessToken.decode_token(refresh_token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    if not token_data.get("refresh"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    user_data = token_data.get("user")
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload"
        )
    uid = user_data.get("uid")
    user = await auth_service.get_user_by_id(uuid.UUID(uid), session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    return AccessToken.create_access_token(
        user={"email": user.email, "uid": str(user.id)},
        td=settings.ACCESS_TOKEN_EXPIRY,
        refresh=False,
    )
