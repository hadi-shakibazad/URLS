import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_SECRET = os.getenv("BOT_SECRET")
WEBHOOK_ENDPOINT = f"/webhook/{BOT_SECRET}"