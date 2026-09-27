from aiogram import Bot
from aiogram import Dispatcher

from app.core.config import settings
from app.telegram.handlers import router

bot = Bot(
    token=settings.telegram_bot_token
)

dp = Dispatcher()

dp.include_router(router)