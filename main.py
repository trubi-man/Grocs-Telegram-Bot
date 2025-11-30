from aiogram import Bot, Dispatcher
from app.handlers.handler_command import command_router
from app.handlers.handler_callback_query import callback_query_router
from app.handlers.handler_payment_star import payment_router
from app.handlers.handler_ai import ai_router
from data.sql.models import async_main
from data.sql.request import check_and_clean_subscriptions, update_all_limit
from api.reg_pay import fastapi_app
from config import BOT_TG
import asyncio
import datetime
import uvicorn
import logging

logging.basicConfig(level=logging.INFO)

async def daily_limit_update():
    while True:
        now = datetime.datetime.now()
        if now.hour == 0 and now.minute == 0:
            await check_and_clean_subscriptions()
            await update_all_limit()
            print("успех")
            await asyncio.sleep(61)
        else:
            await asyncio.sleep(58)

async def run_fastapi():
    config_api = uvicorn.Config(app=fastapi_app, log_level="info")
    server_api = uvicorn.Server(config_api)
    await server_api.serve()

async def main():
    await async_main()
    asyncio.create_task(daily_limit_update())
    asyncio.create_task(run_fastapi())

    dp = Dispatcher()
    bot = Bot(token=BOT_TG)
    dp.include_routers(command_router, callback_query_router, payment_router, ai_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())