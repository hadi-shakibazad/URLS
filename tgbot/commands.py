from aiogram import Bot, Router, F
from aiogram.types import Message

from config import BOT_TOKEN


router = Router()
bot = Bot(BOT_TOKEN)


@router.message(F.text == "/start")
async def start(message: Message):
    text = """سلام خوش اومدی 👋
    اگر لینکی هست که بخوای کوتاهش کنی میتونم کمکت کنم"""
    await bot.send_message(message.chat.id, text)


@router.message(F.text == "/add-urls")
async def add_url(message: Message):
    pass

@router.message(F.text == "/list-urls")
async def list_url(message: Message):
    pass

@router.message(F.text == "/list-urls")
async def list_url(message: Message):
    pass

