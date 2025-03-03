from aiogram import Dispatcher

from .commands import router as command_router

dp = Dispatcher()
dp.include_router(command_router)