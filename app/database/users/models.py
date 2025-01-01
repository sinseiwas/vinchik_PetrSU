from sqlalchemy import (
    BigInteger,
    String,
    ForeignKey,
    Integer,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship
)
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    async_sessionmaker,
    create_async_engine
)

engine = create_async_engine(url='sqlite+aiosqlite:///vinchik.sqlite3')
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


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
    is_form: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    forms: Mapped[list["Form"]] = relationship(
        "Form",
        back_populates="user"
        )


class Form(Base):
    __tablename__ = 'forms'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
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

    user: Mapped["User"] = relationship("User", back_populates="forms")


class Like(Base):
    __tablename__ = 'likes'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
        )
    liked_user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
        )
    liked_user: Mapped["User"] = relationship(
        "User",
        foreign_keys=[liked_user_id]
        )


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
