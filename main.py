from aiogram import Bot, Dispatcher
from app.handlers.handler_command import command_router
from app.handlers.handler_callback_query import callback_query_router
from app.handlers.handler_payment import payment_router
from app.handlers.handler_ai import ai_router
from data.sql.models import async_main
from data.sql.request import check_and_clean_subscriptions, update_all_limit
from config import BOT_TG
import asyncio
import datetime
import logging

logging.basicConfig(level=logging.INFO)

async def daily_limit_update():
    while True:
        now = datetime.datetime.now()
        if now.hour == 0 and now.minute == 0:
            await update_all_limit()
            await check_and_clean_subscriptions()
            print("успех")
            await asyncio.sleep(61)
        else:
            await asyncio.sleep(58)


async def main():
    await async_main()
    asyncio.create_task(daily_limit_update())

    dp = Dispatcher()
    bot = Bot(token=BOT_TG)
    dp.include_routers(command_router, callback_query_router, payment_router, ai_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())