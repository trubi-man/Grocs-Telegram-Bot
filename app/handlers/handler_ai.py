from aiogram import Router, F
from aiogram.types import Message
from app.ai.generate_text import generate_ai_response, prices
from data.sql.request import get_model, reduce_balance, get_balance, is_register_user
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent, CallbackQuery
from app.keyboard import inline_query_keyboard
from data.redis.redis_manager import redis_manager

ai_router = Router()

@ai_router.inline_query(F.query.len() > 3)
async def inline_query_handler(inline_query: InlineQuery):
    query = inline_query.query
    result = InlineQueryResultArticle(
        id="1",
        title="Отправить ответ",
        input_message_content=InputTextMessageContent(
            message_text=f"Нажмите на кнопку ниже для генерации по запросу:\n\n{query}"
        ),
        reply_markup=inline_query_keyboard(tg_id=inline_query.from_user.id),
        description="Нажмите, чтобы отправить этот текст на генерацию"
    )
    await redis_manager.set_query(tg_id=inline_query.from_user.id, query=query)
    await inline_query.answer([result])

@ai_router.callback_query(F.data.startswith("generate_"))
async def update_inline_message_handler(callback_query: CallbackQuery):
    inline_message_id = callback_query.inline_message_id
    owner_query = int(callback_query.data.split('_', maxsplit=1)[1])

    await is_register_user(owner_query)
    model = await get_model(owner_query)
    balance = await get_balance(owner_query)
    price = prices.get(model)

    if balance > price:
        query = await redis_manager.get_query(owner_query)
        if query is None:
            await callback_query.bot.edit_message_text(inline_message_id=inline_message_id, text="Что-то пошло не так.")
        
        await callback_query.bot.edit_message_text(
            inline_message_id=inline_message_id,
            text=f"Начинаем генерацию по модели {model}..."
        )
        await reduce_balance(tg_id=owner_query, reduce=price)
        await callback_query.bot.edit_message_text(
            inline_message_id=inline_message_id,
            text=await generate_ai_response(tg_id=owner_query, query=query, model=model), parse_mode='HTML'
        )
    else:
        await callback_query.bot.edit_message_text(inline_message_id=inline_message_id, text="У вас закончились запросы, вы можете купить подписку в боте.")

@ai_router.message(F.text)
async def generate_message(message: Message):
    tg_id = message.from_user.id
    model = await get_model(tg_id)
    price = prices.get(model)
    balance = await get_balance(tg_id)
    if balance > price:
        answer = await message.answer(text=f"Начинаем генерацию по модели {model}...")
        await reduce_balance(tg_id=tg_id, reduce=price)
        await answer.edit_text(text=await generate_ai_response(tg_id=message.from_user.id, query=message.text, model=model), parse_mode='HTML')
    else:
        await message.answer("У вас закончились запросы, вы можете купить подписку в боте.", parse_mode='HTML')