import os
from dotenv import load_dotenv
from telethon import TelegramClient, events

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
LISTENING_CHANNEL_NAME = os.getenv("LISTENING_CHANNEL_NAME")
SEND_CHANNEL_NAME = os.getenv("SEND_CHANNEL_NAME")
SEARCH_WORDS = os.getenv("SEARCH_WORDS")
ADDITIONAL_TEXT_TO_MESSAGE = os.getenv("ADDITIONAL_TEXT_TO_MESSAGE")

client = TelegramClient('bot', int(API_ID), API_HASH)


# Ищет конкретные сообщения в чате и переотправляет их в другой чат.
@client.on(events.NewMessage(chats=[LISTENING_CHANNEL_NAME]))
async def search_new_message(event):
    for word in SEARCH_WORDS.split(","):
        if word in event.raw_text:
            await client.send_message(
                SEND_CHANNEL_NAME,
                f"{event.raw_text}\n{ADDITIONAL_TEXT_TO_MESSAGE}"
                if len(ADDITIONAL_TEXT_TO_MESSAGE)
                else event.raw_text
            )


# Проверка работоспособности.
# Ожидает сообщение "/check" в чате указанного для отправки сообщений.
@client.on(events.NewMessage(chats=[SEND_CHANNEL_NAME], pattern='/check'))
async def check(event):
    await client.send_message(SEND_CHANNEL_NAME, 'ACTIVE')


client.start()
print("Service started")

client.run_until_disconnected()
