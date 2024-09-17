import os
from dotenv import load_dotenv
from telethon import TelegramClient, events

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
LISTENING_CHANNEL_ID = os.getenv("LISTENING_CHANNEL_ID")
SEND_CHANNEL_ID = os.getenv("SEND_CHANNEL_ID")
SEARCH_WORDS = os.getenv("SEARCH_WORDS")

client = TelegramClient('spainbotsecure', int(API_ID), API_HASH)

# Ищет конкретные сообщения в чате и переотправляет их в другой чат.
@client.on(events.NewMessage(chats=[int(LISTENING_CHANNEL_ID)]))
async def search_new_message(event):
    for word in SEARCH_WORDS.split(","):
        if word in event.raw_text:
            await client.send_message(int(SEND_CHANNEL_ID), event.raw_text)


# Проверка работоспособности.
# Ожидает сообщение "/check" в чате указанного для отправки сообщений.
@client.on(events.NewMessage(chats=[int(SEND_CHANNEL_ID)], pattern='/check'))
async def check(event):
    await client.send_message(int(SEND_CHANNEL_ID), 'ACTIVE')


client.start()
print("Service started")

client.run_until_disconnected()
