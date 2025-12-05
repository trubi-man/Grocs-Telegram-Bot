from app.handlers.texts import INFO_TEXT
from data.sql.request import is_register_user, is_vip
from data.redis.redis_manager import redis_manager
from app.keyboard import start_menu
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
from aiogram import Router, Bot

command_router = Router()

@command_router.message(CommandStart())
async def command_start_handler(message: Message):
    is_new_user = await is_register_user(message.from_user.id)
    if is_new_user:
        await message.answer(text="Привет, прочтите о возможностях бота.\n" + INFO_TEXT, parse_mode='HTML', reply_markup=start_menu(False))
        # await message.answer(text="Наш канал:", reply_markup=channel_link)
    else:
        vip = await is_vip(message.from_user.id)
        await message.answer(text=INFO_TEXT, parse_mode='HTML', reply_markup=start_menu(vip))

@command_router.message(Command("reset_history"))
async def reset_history(message: Message):
    await message.answer("История с ботом очищена.")
    await redis_manager.clear_history(message.from_user.id)

@command_router.message(Command("returnPay"))
async def return_pay(message: Message, bot: Bot, command: CommandObject):
    if not command.args:
        await message.answer("Так нельзя!")
        return
    args = command.args.split(maxsplit=2)

    if len(args) == 2:
        try:
            await bot.refund_star_payment(user_id=int(args[0]), telegram_payment_charge_id=args[1])
            await message.answer("Успешно!")
        except Exception:
            await message.answer("Что-то пошло не так.")
    else:
        await message.answer("Не верный ввод комманды!")