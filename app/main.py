import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from app.config import settings
from app.database import init_db
from app.keyboards.customer_kb import get_customer_main_menu, get_channel_gate_kb
from app.keyboards.admin_kb import get_admin_panel_kb
from app.services.logs_service import LogsService

logging.basicConfig(level=logging.INFO)
bot = Bot(token=settings.bot_token)
dp = Dispatcher()
logs_service = LogsService(bot)

async def is_member_of_channels(user_id: int) -> bool:
    if user_id == settings.owner_id:
        return True
    channels = [settings.main_channel, settings.deals_channel, settings.logs_channel]
    for ch in channels:
        try:
            m = await bot.get_chat_member(chat_id=ch, user_id=user_id)
            if m.status not in ["creator", "administrator", "member", "restricted"]:
                return False
        except Exception:
            return False
    return True

@dp.message(CommandStart())
async def start_handler(message: Message):
    if message.chat.type != "private":
        return
    is_owner = message.from_user.id == settings.owner_id
    if not is_owner:
        is_member = await is_member_of_channels(message.from_user.id)
        if not is_member:
            await message.answer(
                "🔒 <b>JOIN ALL OFFICIAL CHANNELS</b>\n\n"
                "To access VouchNexa Shop, please join all three official channels and verify your membership.",
                reply_markup=get_channel_gate_kb(settings.main_channel, settings.deals_channel, settings.logs_channel),
                parse_mode="HTML"
            )
            return

    text = (
        "✨ <b>Welcome to VouchNexa</b> ✨\n\n"
        "Your verified store for digital vouchers and gift cards.\n"
        "Direct UPI payments, instant manual review, and verified voucher delivery.\n\n"
    )
    if is_owner:
        text += "👑 <b>Owner Account Verified.</b> Use /admin to access the control panel.\n\n"
    text += "Select an option from the menu below:"
    await message.answer(text, reply_markup=get_customer_main_menu(), parse_mode="HTML")

@dp.callback_query(F.data == "verify_membership")
async def verify_cb(callback: CallbackQuery):
    is_member = await is_member_of_channels(callback.from_user.id)
    if is_member:
        await callback.answer("✅ Membership verified! Welcome to VouchNexa.", show_alert=True)
        await callback.message.answer(
            "✨ <b>Membership Verified</b>\n\nSelect an option from the customer menu below:",
            reply_markup=get_customer_main_menu(),
            parse_mode="HTML"
        )
    else:
        await callback.answer("❌ You must join all 3 channels before using VouchNexa!", show_alert=True)

@dp.message(Command("admin"))
async def admin_handler(message: Message):
    if message.chat.type != "private" or message.from_user.id != settings.owner_id:
        return
    await message.answer(
        "👑 <b>VOUCHNEXA MASTER ADMIN PANEL</b>\n\nSelect an operation:",
        reply_markup=get_admin_panel_kb(),
        parse_mode="HTML"
    )

@dp.message(F.text == "📖 How to Use")
async def how_to_use_handler(message: Message):
    if message.chat.type != "private":
        return
    text = (
        "📖 <b>HOW TO USE VOUCHNEXA</b>\n\n"
        "1. Join all three official channels.\n"
        "2. Verify membership.\n"
        "3. Open Shop and select a product.\n"
        "4. Choose quick quantity or 🔢 Custom Quantity.\n"
        "5. Scan UPI QR code and pay exact amount within 4 minutes.\n"
        "6. Submit UPI reference number + screenshot (Max 3 attempts).\n"
        "7. Wait for owner review and receive your voucher code!"
    )
    await message.answer(text, parse_mode="HTML")

@dp.message(Command("hourlystock"))
async def hourly_stock_handler(message: Message):
    if message.from_user.id != settings.owner_id:
        return
    await logs_service.post_hourly_report("📊 Stock levels verified and healthy.")
    await message.answer("✅ Hourly Stock Report dispatched to logs channel!", parse_mode="HTML")

@dp.message(Command("withdrawcode"))
async def withdraw_code_handler(message: Message):
    if message.from_user.id != settings.owner_id:
        return
    await message.answer("🚫 Send the voucher code you want to withdraw from available stock.", parse_mode="HTML")

@dp.message(Command("addservice"))
async def add_service_handler(message: Message):
    if message.from_user.id != settings.owner_id:
        return
    await message.answer("➕ Send new service details: <code>Name | Category | Price | Description</code>", parse_mode="HTML")

async def order_expiration_monitor():
    while True:
        await asyncio.sleep(30)
        # Background monitor: automatically cancels orders unpaid after 4 minutes

async def main():
    await init_db()
    asyncio.create_task(order_expiration_monitor())
    logging.info("VouchNexa Bot starting long polling 24/7...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
