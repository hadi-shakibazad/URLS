from aiogram import Bot, Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import BOT_TOKEN, HOST
from services import add_url, owned_urls, url_activation, is_owned

router = Router()
bot = Bot(BOT_TOKEN)

class AddLink(StatesGroup):
    link = State()

@router.message(F.text == "/start")
async def start(message: Message):
    text = """سلام خوش اومدی 👋
اگر لینکی هست که بخوای کوتاهش کنی میتونم کمکت کنم"""
    await bot.send_message(message.chat.id, text)


@router.message(AddLink.link)
async def add2(message: Message, state: FSMContext):
    code = await add_url(message.text, message.from_user.id)
    await bot.send_message(message.chat.id, "لینک کوتاه شده :")
    await bot.send_message(message.chat.id, f"`https://{HOST}/l/{code}`", parse_mode=ParseMode.MARKDOWN)
    await state.clear()


@router.message(F.text == "/add")
async def add1(message: Message, state: FSMContext):
    await bot.send_message(message.chat.id, "لینک مورد نظرت رو بفرست 👇")
    await state.set_state(AddLink.link)


@router.message(F.text == "/list")
async def list_urls(message: Message):
    builder = InlineKeyboardBuilder()
    msg = ""

    links = await owned_urls(message.from_user.id)
    for index, url in enumerate(links):
        url, code, is_active = url

        status_mark = '✅ فعال' if is_active else '🚫 غیر فعال'
        number = str(index + 1)

        url = f"https://{HOST}/l/{code}"
        msg += f"\n{number}. `{url}`"
        msg += f"\n{status_mark}\n\n"
        builder.button(text=f"{number}", url=url)

    builder.adjust(5)
    await bot.send_message(message.chat.id, text=msg, parse_mode=ParseMode.MARKDOWN, reply_markup=builder.as_markup())


@router.callback_query(F.data.contains("on"))
async def activate(callback: CallbackQuery):
    _, target_url, number = callback.data.split()

    if not await is_owned(target_url, callback.from_user.id):
        await bot.send_message(callback.message.chat.id, "شما به این لینک دسترسی ندارید")

    await url_activation(target_url)
    await bot.send_message(callback.message.chat.id, f"شماره {number} فعال سازی شد ✅", disable_notification=True)


@router.callback_query(F.data.contains("off"))
async def deactivate(callback: CallbackQuery):
    _, target_url, number = callback.data.split()

    if not is_owned(target_url, callback.from_user.id):
        await bot.send_message(callback.message.chat.id, "شما به این لینک دسترسی ندارید")

    await url_activation(target_url, activate=False)
    await bot.send_message(callback.message.chat.id, f"شماره {number}غیر فعال سازی شد 🚫", disable_notification=True)


@router.message(F.text == "/activation")
async def activation_status(message: Message):
    builder = InlineKeyboardBuilder()
    links = await owned_urls(message.from_user.id)
    msg = ""

    for index, link in enumerate(links):
        url, code, is_active = link
        number = str(index + 1)
        url = f"https://{HOST}/l/{code}"
        msg += f"\n{number}. {url} \n"
        builder.button(text=f" ✅ فعال سازی {number}", callback_data=f"on {code} {number}")
        builder.button(text=f" 🚫 غیر فعال سازی {number}", callback_data=f"off {code} {number}")
    builder.adjust(2)

    await bot.send_message(message.chat.id, msg, reply_markup=builder.as_markup())
