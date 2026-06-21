import uuid

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.schema import UserCreate
from app.core.security import Passwords
from app.db.models import User


class UserAuthService:
    async def get_user_by_email(self, email: str, session: AsyncSession) -> User | None:
        s = select(User).where(User.email == email)
        result = await session.execute(s)
        return result.scalar_one_or_none()

    async def get_user_by_id(self, id: uuid.UUID, session: AsyncSession) -> User | None:
        s = select(User).where(User.id == id)
        result = await session.execute(s)
        return result.scalar_one_or_none()

    async def if_user_exists(self, email: str, session: AsyncSession) -> bool:
        return True if (await self.get_user_by_email(email, session)) else False

    async def create_user(self, user: UserCreate, session: AsyncSession) -> User | None:
        if await self.if_user_exists(user.email, session):
            raise HTTPException(
                status_code=409,
                detail="Email already exists. Please try with another email.",
            )
        new_user = User(
            username=user.username,
            email=user.email,
            hashed_password=Passwords.get_password_hash(user.password),
        )

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return new_user
