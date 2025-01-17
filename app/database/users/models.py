from sqlalchemy import (
    BigInteger,
    String,
    ForeignKey,
    Integer,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from typing import Optional
from database.base import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True
        )
    username: Mapped[str] = mapped_column(
        String(32),
        nullable=True
        )
    first_name: Mapped[str] = mapped_column(
        String(32),
        nullable=True
        )
    last_name: Mapped[str] = mapped_column(
        String(32),
        nullable=True
        )
    is_active: Mapped[bool] = mapped_column(default=True)

    form: Mapped[Optional["Form"]] = relationship(back_populates="user")


class Form(Base):
    __tablename__ = 'forms'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    name: Mapped[str] = mapped_column(
        String(64),
        nullable=True
    )
    age: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    form_text: Mapped[str] = mapped_column(String)
    photo_path: Mapped[str] = mapped_column(
        String,
        nullable=True
    )

    user: Mapped[Optional["User"]] = relationship(back_populates="forms")


class Like(Base):
    __tablename__ = 'likes'

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True,
    )
    liked_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True,
    )
    # TODO User relationship
    liked_user: Mapped["User"] = relationship(
        "User",
        foreign_keys=[liked_user_id]
        )
