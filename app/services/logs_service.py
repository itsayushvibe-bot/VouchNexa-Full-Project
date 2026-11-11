from datetime import datetime
import pytz
from aiogram import Bot
from app.config import settings

class LogsService:
    """
    Strict 5 allowed event types to logs channel:
    1. New Purchase
    2. Stock Added
    3. Hourly Stock Report
    4. Low Stock Alert
    5. Out of Stock Alert
    """
    def __init__(self, bot: Bot):
        self.bot = bot
        self.logs_channel = settings.logs_channel
        self.tz = pytz.timezone("Asia/Kolkata")

    def _get_ist_time(self) -> str:
        return datetime.now(self.tz).strftime("%d %b %Y, %I:%M %p IST")

    async def post_new_purchase(self, order_id: str, product_name: str, quantity: int, amount_rupees: str):
        text = (
            f"🛍️ <b>NEW PURCHASE</b>\n\n"
            f"Order ID: <b>#{order_id}</b>\n"
            f"Product: <b>{product_name}</b>\n"
            f"Quantity: <b>{quantity}</b>\n"
            f"Amount: <b>₹{amount_rupees}</b>\n"
            f"Date: <i>{self._get_ist_time()}</i>\n\n"
            f"#VouchNexaOfficialLogs"
        )
        await self.bot.send_message(self.logs_channel, text, parse_mode="HTML")

    async def post_stock_added(self, product_name: str, added_count: int, new_stock: int):
        text = (
            f"📦 <b>STOCK ADDED</b>\n\n"
            f"Product: <b>{product_name}</b>\n"
            f"Quantity Added: <b>+{added_count}</b>\n"
            f"New Available Stock: <b>{new_stock}</b>\n"
            f"Date: <i>{self._get_ist_time()}</i>"
        )
        await self.bot.send_message(self.logs_channel, text, parse_mode="HTML")

    async def post_hourly_report(self, report_body: str):
        text = (
            f"📊 <b>HOURLY INVENTORY REPORT</b>\n\n"
            f"{report_body}\n\n"
            f"<i>🕒 {self._get_ist_time()}</i>"
        )
        await self.bot.send_message(self.logs_channel, text, parse_mode="HTML")

    async def post_low_stock(self, product_name: str, available: int, threshold: int):
        text = (
            f"⚠️ <b>LOW STOCK ALERT</b>\n\n"
            f"Product <b>{product_name}</b> is running low!\n"
            f"Available: <b>{available}</b>\n"
            f"Threshold: <b>{threshold}</b>\n"
            f"<i>🕒 {self._get_ist_time()}</i>"
        )
        await self.bot.send_message(self.logs_channel, text, parse_mode="HTML")

    async def post_out_of_stock(self, product_name: str):
        text = (
            f"🔴 <b>OUT OF STOCK ALERT</b>\n\n"
            f"Product <b>{product_name}</b> is now completely out of stock.\n"
            f"<i>🕒 {self._get_ist_time()}</i>"
        )
        await self.bot.send_message(self.logs_channel, text, parse_mode="HTML")
