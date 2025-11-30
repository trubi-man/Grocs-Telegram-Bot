from aiomoney import YooMoney
from aiomoney.schemas import InvoiceSource
from app.pay.subcription_data import Subscription
from config import YOOMONEY_SECRET

yoo_money = YooMoney(access_token=YOOMONEY_SECRET)

async def create_pay_link(subscription: str, username_bot: str, tg_id: int):
    for sub in Subscription:
        sub_data = sub.value
        if sub_data.type_sub == subscription:
            price = sub_data.price
            daily_limit = sub_data.daily_limit
            break

    if not price:
        raise Exception("Price cannot be None")

    pay_form = await yoo_money.create_invoice(
        amount_rub=price,
        label=f"{subscription}:{daily_limit}:{tg_id}",
        payment_source=InvoiceSource.YOOMONEY_WALLET,
        success_redirect_url=f"https://t.me/{username_bot}"
    )
    return pay_form.url