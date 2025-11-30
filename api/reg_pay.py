from functools import cache
from config import YOOMONEY_AUTHENICITY, BOT_TG
from datetime import timedelta
from pydantic import BaseModel
from fastapi import FastAPI, Request, HTTPException
from aiogram import Bot
from data.sql.request import set_subscription
import hashlib
import hmac

fastapi_app = FastAPI()

class YooMoneyNotification(BaseModel):
    notification_type: str
    operation_id: str
    amount: str
    datetime: str
    sender: str
    label: str
    sha1_hash: str

supported_elements: list[str] = ['notification_type', 'operation_id', 'amount', 'datetime', 'sender', 'label', 'sha1_hash']

@cache
def get_bot() -> Bot:
    return Bot(token=BOT_TG)

@fastapi_app.get("/")
async def read_root():
    return "Russia will be free"

@fastapi_app.post("/payment")
async def subscription_payment(request: Request, bot: Bot = get_bot()):
    form_data = await request.form()
    
    # Извлекаем ВСЕ нужные поля, включая обязательные для хеша
    raw = dict(form_data)
    
    # Обязательные поля для хеша (даже если не нужны в модели)
    try:
        notification_type = raw["notification_type"]
        operation_id = raw["operation_id"]
        amount = raw["amount"]
        currency = raw.get("currency", "643")
        datetime = raw["datetime"]
        sender = raw["sender"]
        codepro = raw.get("codepro", "false")
        label = raw.get("label", "")
        received_hash = raw["sha1_hash"]
    except KeyError as e:
        print(e)
        raise HTTPException(400, f"Missing required field: {e}")

    hash_str = (
        f"{notification_type}&"
        f"{operation_id}&"
        f"{amount}&"
        f"{currency}&"
        f"{datetime}&"
        f"{sender}&"
        f"{codepro}&"
        f"{YOOMONEY_AUTHENICITY}&"
        f"{label}"
    )
    
    calculated_hash = hashlib.sha1(hash_str.encode("utf-8")).hexdigest()
    
    if not hmac.compare_digest(calculated_hash, received_hash):
        raise HTTPException(400, "Invalid sha1_hash")
    
    form_dict = {key: value for key, value in raw.items() if key in supported_elements}
    yoo_money_notification = YooMoneyNotification(**form_dict)

    if yoo_money_notification.label:
        label_split: list[str] = yoo_money_notification.label.split(sep=':', maxsplit=3)

        if len(label_split) < 3:
            raise HTTPException(400, "Invalid label format")

        current_time = datetime.now()
        end_time = current_time + timedelta(days=30)
    
        unix_timestamp = int(end_time.timestamp())
        end_date = end_time.strftime("%d.%m.%Y")

        tg_id = int(label_split[2])

        await set_subscription(tg_id=tg_id, vip_type=label_split[0], end_time=unix_timestamp, day_limit=label_split[1])
        await bot.send_message(
            chat_id=tg_id,
            text=f"✅ Вы успешно оплатили подписку {label_split[0].capitalize()}.\nПодписка активна до {end_date}."
        )
        return {"status": "ok"}
    else:
        raise HTTPException(422, "Label is missing or empty")
    