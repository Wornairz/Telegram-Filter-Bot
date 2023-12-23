from telethon.sync import TelegramClient, events
from settings import *

# client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=TOKEN)
client = TelegramClient("prova", API_ID, API_HASH).start(phone=PHONE_NUMBER)


async def get_channel_messages():
    channel_entity = await client.get_entity(CHANNELS[0])

    # Ottieni gli ultimi 10 messaggi dal canale
    messages = await client.get_messages(channel_entity, limit=10)

    for message in messages:
        print(message.text)


@client.on(events.NewMessage(chats=CHANNELS))
async def handle_new_message(event):
    print(event.message.text)


if __name__ == "__main__":
    client.run_until_disconnected()
