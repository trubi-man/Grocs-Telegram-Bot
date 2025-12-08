from sqlalchemy import BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, async_sessionmaker
from config import SQL_PASSWORD

engine = create_async_engine(
    url=f"postgresql+asyncpg://grocs:{SQL_PASSWORD}@localhost/grocs_db",
    echo=False
)

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    model: Mapped[str] = mapped_column(default="qwen3-4b")
    vip: Mapped[bool] = mapped_column(default=False)
    balance: Mapped[int] = mapped_column(default=15)
    day_limit: Mapped[int] = mapped_column(default=15)

class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    vip_type: Mapped[str] = mapped_column(nullable=False)
    end_time: Mapped[int] = mapped_column(BigInteger)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)