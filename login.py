# file: login.py
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from config import (API_ID, API_HASH)

# Авторизация и печать ключа сессии
with TelegramClient(StringSession(), API_ID, API_HASH) as client:
    print(client.session.save())