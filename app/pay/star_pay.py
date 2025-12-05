from aiogram.types import LabeledPrice, Message
from app.pay.subcription_data import Subscription
from app.keyboard import payment_keyboard

async def create_star_payment(message: Message, subscription: str):
    for sub in Subscription:
        sub_data = sub.value
        if sub_data.type_sub == subscription:
            price = sub_data.price
            daily_limit = sub_data.daily_limit
            break

    if not price:
        raise Exception("Price cannot be None")
    
    prices = [LabeledPrice(label="XTR", amount=price)]
    
    await message.answer_invoice(
        title=f"Подписка {subscription.capitalize()}",
        description=f"Подписка {subscription.capitalize()} на 30 дней за {price} ⭐️",
        provider_token="",
        currency="XTR",
        prices=prices,
        payload=f"subscription:{subscription}:{daily_limit}",
        reply_markup=payment_keyboard(price)
    )
