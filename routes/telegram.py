from fastapi import APIRouter
from aiogram.types import Update
from aiogram import Bot

from config import BOT_SECRET, BOT_TOKEN
from tgbot import dp

router = APIRouter()
bot = Bot(BOT_TOKEN)

@router.post(f"/webhook/{BOT_SECRET}")
async def webhook(update: Update):
    await dp.feed_update(bot, update)


