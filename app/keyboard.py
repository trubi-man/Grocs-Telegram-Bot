from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def start_menu(vip: bool):
    keyboard = [
        [InlineKeyboardButton(text="Профиль", callback_data="profile"), 
         InlineKeyboardButton(text="Модели", callback_data="select_model")]
    ]
    
    if not vip:
        keyboard.append([InlineKeyboardButton(text="Подписки", callback_data="buy_vip")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

back_to_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔙 Назад", callback_data="back")]
])

def select_pay(subscription: str):
    return InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Карта", callback_data=f"card_{subscription}")],
    [InlineKeyboardButton(text="Звезды", callback_data=f"stars_{subscription}")],
    [InlineKeyboardButton(text="🔙 Назад", callback_data="back")]
])

select_model_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="OpenAI GPT OSS 120B", callback_data="ai_openai-gpt-oss-120b"),
     InlineKeyboardButton(text="Gemma 3 27B", callback_data="ai_google-gemma-3-27b-it")],
    [InlineKeyboardButton(text="Venice Small", callback_data="ai_qwen3-4b"),
     InlineKeyboardButton(text="Venice Uncensored", callback_data="ai_venice-uncensored")],
    [InlineKeyboardButton(text="Venice Medium", callback_data="ai_mistral-31-24b"),
     InlineKeyboardButton(text="Venice Large", callback_data="ai_qwen3-235b")],
    [InlineKeyboardButton(text="GLM 4.6", callback_data="ai_zai-org-glm-4.6"),
     InlineKeyboardButton(text="Llama 3.3", callback_data="ai_llama-3.3-70b")],
    [InlineKeyboardButton(text="🔙 Назад", callback_data="back")]
])

subscriptions = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Standard", callback_data="sub_standard")],
    [InlineKeyboardButton(text="Pro", callback_data="sub_pro")],
    [InlineKeyboardButton(text="Premium", callback_data="sub_premium")],
    [InlineKeyboardButton(text="🔙 Назад", callback_data="back")]
])

def payment_keyboard(amount: str | int, is_star: bool = True):
    return InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=f"Оплатить {amount} {'⭐' if is_star else '\u20BD'}", pay=True)]
])

def payment_card(link: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Оплатить", url=link)],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="back")]
    ])

def inline_query_keyboard(tg_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Запустить", callback_data=f"generate_{tg_id}")]
    ])

# channel_link = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text="💬 Канал", url="https://t.me/grocsneiro")]
# ])