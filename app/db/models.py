import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    username: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), index=True, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),  # timezone awareness (always preferred)
        server_default=func.now(),
        onupdate=func.now(),
    )


"""
Note: default vs server_default - 
    Use default for applicate-side values \
    Use server_default for db-side values (basically when you want the db to be source of truth) \
    For eg. uuid (app side) vs datetime (db side) \
    Even for DateTime we could have used default=datetime.datetime.now (which would have made it app side)
"""
