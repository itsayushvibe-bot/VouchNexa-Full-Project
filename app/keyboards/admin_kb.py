from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_admin_panel_kb() -> InlineKeyboardMarkup:
    """
    EXACTLY EIGHT MAIN BUTTONS:
    Row 1: 📊 Dashboard, 🛍️ Shop Management
    Row 2: 📦 Stock Manager, 🧾 Orders & Payments
    Row 3: 🔄 Recovery, 👥 Users & Support
    Row 4: 📈 Reports & Logs, ⚙️ Settings
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📊 Dashboard", callback_data="admin_dashboard"),
                InlineKeyboardButton(text="🛍️ Shop Management", callback_data="admin_shop"),
            ],
            [
                InlineKeyboardButton(text="📦 Stock Manager", callback_data="admin_stock"),
                InlineKeyboardButton(text="🧾 Orders & Payments", callback_data="admin_orders"),
            ],
            [
                InlineKeyboardButton(text="🔄 Recovery", callback_data="admin_recovery"),
                InlineKeyboardButton(text="👥 Users & Support", callback_data="admin_users"),
            ],
            [
                InlineKeyboardButton(text="📈 Reports & Logs", callback_data="admin_reports"),
                InlineKeyboardButton(text="⚙️ Settings", callback_data="admin_settings"),
            ],
        ]
    )
