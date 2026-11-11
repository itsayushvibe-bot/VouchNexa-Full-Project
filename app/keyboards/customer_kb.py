from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_customer_main_menu() -> ReplyKeyboardMarkup:
    """
    EXACTLY FIVE BUTTONS:
    Row 1: 🛍️ Shop, 📦 My Orders
    Row 2: 🔄 Recovery, 🎧 Support
    Row 3: 📖 How to Use
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛍️ Shop"), KeyboardButton(text="📦 My Orders")],
            [KeyboardButton(text="🔄 Recovery"), KeyboardButton(text="🎧 Support")],
            [KeyboardButton(text="📖 How to Use")],
        ],
        resize_keyboard=True
    )

def get_channel_gate_kb(main: str, deals: str, logs: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📢 Join Main Channel", url=f"https://t.me/{main.replace('@', '')}")],
            [InlineKeyboardButton(text="🔥 Join Deals Channel", url=f"https://t.me/{deals.replace('@', '')}")],
            [InlineKeyboardButton(text="📋 Join Logs Channel", url=f"https://t.me/{logs.replace('@', '')}")],
            [InlineKeyboardButton(text="✅ Verify Membership", callback_data="verify_membership")],
        ]
    )
