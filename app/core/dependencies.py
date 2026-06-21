import uuid
from typing import Annotated, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import AccessToken
from app.db.session import get_db
from app.services.auth_service import UserAuthService

bearer_scheme = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
    session: Annotated[AsyncSession, Depends(get_db)],
    auth_service: Annotated[UserAuthService, Depends()],
) -> Any:
    token = credentials.credentials

    try:
        jwt_data = AccessToken.decode_token(token)
        if jwt_data.get("refresh"):
            raise
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
