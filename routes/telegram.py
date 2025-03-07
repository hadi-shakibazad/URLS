from fastapi import APIRouter
from aiogram.types import Update
from aiogram import Bot

from config import BOT_SECRET, BOT_TOKEN, WEBHOOK_ENDPOINT
from tgbot import dp

router = APIRouter()
bot = Bot(BOT_TOKEN)


@router.post(WEBHOOK_ENDPOINT)
async def webhook(update: Update):
    await dp.feed_update(bot, update)


