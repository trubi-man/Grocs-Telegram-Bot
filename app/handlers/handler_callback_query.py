from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery
from app.keyboard import back_to_menu, start_menu, select_pay, select_model_keyboard, subscriptions, payment_card
from app.pay.star_pay import create_star_payment
from data.sql.request import is_vip, get_model, set_model, get_user, get_vip_type, get_end_subscriptions
from app.handlers.texts import INFO_TEXT
from app.pay.card_pay import create_pay_link
from datetime import datetime

callback_query_router = Router()

@callback_query_router.callback_query(F.data == "profile")
async def profile_callback(callback: CallbackQuery):
    id = callback.from_user.id
    user = await get_user(id)

    if user.vip:
        vip_type = await get_vip_type(id)
        end_subscriptions = await get_end_subscriptions(id)

        await callback.message.edit_text(f"""ID: {id}
Токены: {user.balance}/{user.day_limit} (пополнение в 0:00 по МСК)
Подписка: {vip_type.capitalize()}
Текущая модель: {model_dict.get(user.model)}
Конец подписки: {datetime.fromtimestamp(end_subscriptions).strftime("%d.%m.%Y") if end_subscriptions else None}
""")
    else:
        await callback.message.edit_text(
    f"""ID: {id}
Подписка: Отсутствует
Токены: {user.balance}/{user.day_limit} (пополнение в 0:00 по МСК)
Текущая модель: {model_dict.get(user.model)}""", reply_markup=back_to_menu
)

@callback_query_router.callback_query(F.data == "back")
async def go_to_menu_callback(callback: CallbackQuery):
    vip = await is_vip(callback.from_user.id)
    await callback.message.edit_text(text=INFO_TEXT, parse_mode='HTML', reply_markup=start_menu(vip))

@callback_query_router.callback_query(F.data == "buy_vip")
async def select_pay_callback(callback: CallbackQuery):
    await callback.message.edit_text("""
💎 <b>STANDARD</b>
┌ 130 токенов в день
├ 3 900 токенов в месяц
└ <b>99 (руб/stars)/месяц</b>

🚀 <b>PRO</b>  
┌ 400 токенов в день
├ 12 000 токенов в месяц
└ <b>299 (руб/stars)/месяц</b>

👑 <b>PREMIUM</b>
┌ 1 000 токенов в день
├ 30 000 токенов в месяц
└ <b>599 (руб/stars)/месяц</b>
""", reply_markup=subscriptions, parse_mode='HTML')

@callback_query_router.callback_query(F.data.startswith("sub_"))
async def select_payment_method(callback: CallbackQuery):
    subscription = callback.data.split('_', maxsplit=1)[1]
    await callback.message.edit_text("Какой способ оплаты будем использовать?", reply_markup=select_pay(subscription)) 

@callback_query_router.callback_query(F.data.startswith("stars_"))
async def buy_vip_for_stars(callback: CallbackQuery):
    subscription = callback.data.split('_', maxsplit=1)[1]
    await create_star_payment(message=callback.message, subscription=subscription)
    await callback.answer()

@callback_query_router.callback_query(F.data.startswith("card_"))
async def buy_vip_for_card(callback: CallbackQuery, bot: Bot):
    subscription = callback.data.split('_', maxsplit=1)[1]
    bot_info = await bot.get_me()
    link = await create_pay_link(
        tg_id=callback.from_user.id,
        subscription=subscription,
        username_bot=bot_info.username
    )
    await callback.message.edit_text(
        "Ссылка на оплату создана.\nДля оплаты подписки нажмите на кнопку ниже ⬇️",
        reply_markup=payment_card(link)
        )

@callback_query_router.callback_query(F.data == "select_model")
async def select_model(callback: CallbackQuery):
    model = await get_model(callback.from_user.id)
    await callback.message.edit_text(f"""В данный момент у вас модель {model_dict.get(model)}.\n
Выберите новую модель(в скобках указана цена за 1 токен):\n
1. OpenAI GPT OSS 120B(2) - Открытая модель от OpenAI, подходит для разных задач.\n
2. Gemma 3 27B(2) - Модель от Google, хороша для программирования и анализа.\n
3. Venice Small(1) - Экономный вариант для простых задач. Под капотом qwen3-4b.\n
4. Venice Uncensored(6) - Модель без цензуры. Подходит для нестандартных задач.\n
5. Venice Medium(13) - Сбалансированная модель на Mistral 3.1 для большинства задач.\n
6. Venice Large(23) - Мощная модель на qwen3-235b, подходит для сложных вычислений и анализа.\n
7. GLM 4.6(18) - Китайская модель, специализируется на математике и логике.\n
8. Llama 3.3(19) - Модель от Meta для комплексных задач.\n
""", reply_markup=select_model_keyboard)

@callback_query_router.callback_query(F.data.startswith("ai_"))
async def change_model(callback: CallbackQuery):
    model = callback.data.split('_', maxsplit=1)[1]
    await callback.message.edit_text(f"Вы успешно сменили модель на {model_dict.get(model)}.", reply_markup=back_to_menu)
    await set_model(callback.from_user.id, model)

model_dict = {
    'qwen3-4b': 'Venice Small',
    'venice-uncensored': 'Venice Uncensored',
    'mistral-31-24b': 'Venice Medium',
    'qwen3-235b': 'Venice Large',
    'openai-gpt-oss-120b': 'OpenAI GPT OSS 120B',
    'google-gemma-3-27b-it': 'Gemma 3 27B',
    'zai-org-glm-4.6': 'GLM 4.6',
    'llama-3.3-70b': 'Llama 3.3'
}