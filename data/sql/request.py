from sqlalchemy import delete, select, update
from data.sql.models import User, Subscription, async_session
import time

async def get_balance(tg_id: int) -> int:
    async with async_session() as session:
        balance = await session.execute(
            select(User.balance)
            .where(User.tg_id == tg_id)
        )
        return balance.scalar_one()
    
async def is_register_user(tg_id: int): # True if new user
    async with async_session() as session:
        is_new_user = await session.execute(
            select(User).where(User.tg_id == tg_id)
        )
        user = is_new_user.scalar_one_or_none()

        if user:
            return False
        else:
            new_user = User(
                tg_id = tg_id
            )
            session.add(new_user)
            await session.commit()
            return True

async def is_vip(tg_id: int):
    async with async_session() as session:
        vip = await session.execute(
            select(User.vip).where(User.tg_id == tg_id)
        )
        return vip.scalar_one()
    
async def set_model(tg_id: int, model: str):
    async with async_session() as session:
        await session.execute(update(User)
            .where(User.tg_id == tg_id)
            .values(model=model)
        )
        await session.commit()

async def set_day_limit(tg_id: int, day_limit: int):
    async with async_session() as session:
        user = await session.execute(
            select(User).where(User.tg_id == tg_id)
        )
        user = user.scalar_one()
        user.day_limit = day_limit
        user.balance = day_limit
        await session.commit()

async def get_model(tg_id: int):
    async with async_session() as session:
        model = await session.execute(
            select(User.model).where(User.tg_id == tg_id)
        )
        return model.scalar_one()

async def get_user(tg_id: int):
    async with async_session() as session:
        user = await session.execute(
            select(User).where(User.tg_id == tg_id)
        )
        return user.scalar_one_or_none()
    
async def reduce_balance(tg_id: int, reduce: int):
    async with async_session() as session:
        await session.execute(
            update(User)
                .where(User.tg_id == tg_id)
                .values(balance=User.balance - reduce)
            )
        await session.commit()

async def update_all_limit():
    async with async_session() as session:
        await session.execute(
            update(User)
            .values(balance = User.day_limit)
        )
        await session.commit()

async def set_subscription(tg_id: int, vip_type: str, end_time: int, day_limit: int):
    async with async_session() as session:
        session.add(
            Subscription(
                tg_id=tg_id,
                vip_type=vip_type.lower(),
                end_time=end_time
            )
        )
        await session.execute(
            update(User)
            .where(User.tg_id == tg_id)
            .values(
                day_limit=day_limit,
                balance=day_limit,
                vip=True
            )
        )
        await session.commit()

async def get_vip_type(tg_id: int) -> str | None:
    async with async_session() as session:
        vip_type = await session.execute(
            select(Subscription.vip_type)
            .where(Subscription.tg_id == tg_id)
        )
        return vip_type.scalar_one_or_none()

async def get_end_subscriptions(tg_id: int) -> int | None:
    async with async_session() as session:
        unix_time = await session.execute(
            select(Subscription.end_time)
            .where(Subscription.tg_id == tg_id)
        )
        return unix_time.scalar_one_or_none()

async def check_and_clean_subscriptions():
    async with async_session() as session:
        current_time = int(time.time())

        expired_subscriptions = await session.execute(
            select(Subscription.tg_id)
            .where(Subscription.end_time < current_time)
        )

        expired_users: list[int] = expired_subscriptions.scalars().all()

        if expired_users:
            await session.execute(
                delete(Subscription)
                .where(Subscription.tg_id.in_(expired_users))
            )
            await session.execute(
                update(User)
                .where(User.tg_id.in_(expired_users))
                .values(
                    day_limit=15,
                    vip=False
                )
            )
            await session.commit()

# async def get_all_tg_id() -> list[int]:
#     async with async_session() as session:
#         list_users = await session.execute(
#             select(User.tg_id)
#         )
#         list_users_scalars: list[int] = list_users.scalars().all()
#         return list_users_scalars