from telethon.sync import TelegramClient, events
from settings import *

#client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=TOKEN)
client = TelegramClient('prova', API_ID, API_HASH).start(phone=PHONE_NUMBER)

#@client.on(events.NewMessage(chats = CHANNELS))
#async def main(event):
#     me = client.get_me()
#     print(me.stringify())
#     print(event.stringify())

async def get_channel_messages():
    # Sostituisci 'channel_username' con il nome utente del canale (ad esempio, '@example_channel')
    channel_entity = await client.get_entity(CHANNELS[0])

    # Ottieni gli ultimi 10 messaggi dal canale
    messages = await client.get_messages(channel_entity, limit=10)

    for message in messages:
        print(message.text)

if __name__ == '__main__':
    client.loop.run_until_complete(get_channel_messages())