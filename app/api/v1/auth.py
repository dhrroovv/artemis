from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.logger import get_logger
from app.core.schema import UserCreate, UserCreateResponse, UserLoginRequest
from app.core.security import AccessToken, Passwords
from app.db.session import get_db
from app.services.auth_service import UserAuthService

settings = get_settings()
logger = get_logger(__name__)

router = APIRouter(tags=["Auth"])  # prefix is already set to "/auth" in root router


@router.get("/")
def hello_world():
    return "hello world"


"""
When you use Depends() with no arguments inside a type hint (e.g., commons: Annotated[ClassName, Depends()]), \
it acts as a shortcut for classes as dependencies. \
FastAPI will automatically detect the class type and call it for you without having to write Depends(ClassName)
"""


@router.post(
    "/signup", response_model=UserCreateResponse, status_code=status.HTTP_201_CREATED
)
async def signup(
    request: Request,
    user_create: UserCreate,
    session: Annotated[AsyncSession, Depends(get_db)],
    user_service: Annotated[UserAuthService, Depends()],
) -> Any:
    if await user_service.if_user_exists(user_create.email, session):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Email already exists."
        )
        # When raise condition is hit, the code just returns back to its upstream code
        # So basically even though we have defined response_model
        # The flow will not even reach there, because serialization (very last thing) happens in case of return

    new_user = await user_service.create_user(user_create, session)
    return new_user


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    request: Request,
    user_data: UserLoginRequest,
    session: Annotated[AsyncSession, Depends(get_db)],
    auth_service: Annotated[UserAuthService, Depends()],
    response: Response,
) -> Any:
    email, password = user_data.email, user_data.password
    user = await auth_service.get_user_by_email(email, session)

    if user:
        is_valid_password = Passwords.verify_password(password, user.hashed_password)

        if is_valid_password:
            access_token = AccessToken.create_access_token(
                user={"email": user.email, "uid": str(user.id)}
            )
            refresh_token = AccessToken.create_access_token(
                user={"email": user.email, "uid": str(user.id)},
                refresh=True,
                td=settings.REFRESH_TOKEN_EXPIRY,
            )
            response.set_cookie(key="access_token", value=access_token, httponly=True)
            response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
            return {
                "user": {"email": email, "uid": str(user.id)},
                "detail": "Login succesful!",
            }
            # We could have used fastapi.JSONResponse here as well, its basically a sub-class of Response class \
            # with all the methods like set_cookie, etc.

    raise HTTPException(
        status_code=401, detail="Incorrect username or password. Please try again."
    )
