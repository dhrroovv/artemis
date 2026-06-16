from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schema import UserCreate, UserCreateResponse
from app.db.session import get_db
from app.services.auth_service import UserService

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
    user_service: Annotated[UserService, Depends()],
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
