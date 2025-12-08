from aiogram.types import LabeledPrice, Message
from app.pay.subcription_data import Subscription
from app.keyboard import payment_keyboard
from config import PROVIDER_TOKEN

async def create_card_payment(message: Message, subscription: str):
    for sub in Subscription:
        sub_data = sub.value
        if sub_data.type_sub == subscription:
            price = sub_data.price
            daily_limit = sub_data.daily_limit
            break

    if not price:
        raise Exception("Price cannot be None")
    
    prices = [LabeledPrice(label="RUB", amount=price * 100)]

    await message.answer_invoice(
        title=f"Подписка {subscription.capitalize()}",
        description=f"Подписка {subscription.capitalize()} на 30 дней за {price} \u20BD",
        provider_token=PROVIDER_TOKEN,
        currency="RUB",
        prices=prices,
        payload=f"subscription:{subscription}:{daily_limit}",
        reply_markup=payment_keyboard(amount=price, is_star=False)
    )