from aiogram import Router, F
from aiogram.types import Message, PreCheckoutQuery
from datetime import datetime, timedelta
from data.sql.request import set_subscription, is_vip

payment_router = Router()

@payment_router.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
    vip = await is_vip(pre_checkout_query.from_user.id)
    if vip:
        await pre_checkout_query.answer(ok=False)
    else:
        await pre_checkout_query.answer(ok=True)

@payment_router.message(F.successful_payment)
async def successful_payment_handler(message: Message):
    payment = message.successful_payment
    data = payment.invoice_payload.split(':')

    current_time = datetime.now()
    end_time = current_time + timedelta(days=30)
    
    end_date = end_time.strftime("%d.%m.%Y")
    unix_timestamp = int(end_time.timestamp())

    await set_subscription(tg_id=message.from_user.id, vip_type=data[1], end_time=unix_timestamp, day_limit=data[2])
    await message.answer(f"Вы успешно оплатили подписку {data[1].capitalize()}.\nПодписка закончится {end_date}.")