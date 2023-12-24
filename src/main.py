from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackContext,
)
from settings import *
from telethon.sync import TelegramClient, events
from telethon.tl.custom import Message

client = TelegramClient("bot", API_ID, API_HASH).start(phone=PHONE_NUMBER)
application = Application.builder().token(TOKEN).build()


async def start(update: Update, context: CallbackContext) -> None:
    print(update.effective_chat.id)
    await update.message.reply_text(
        "Ciao! Sono il tuo bot. Sono in ascolto su diversi canali."
    )


def main() -> None:
    application.add_handler(CommandHandler("start", start))
    application.run_polling()


@client.on(events.NewMessage(chats=CHANNELS))
async def handle_new_message(event: Message):
    # from_chat_id=event.chat_id
    channel_username = event.chat.username
    message_id = event.message.id
    for user in USERS:
        message_link = f"https://t.me/{channel_username}/{message_id}"
        await application.bot.send_message(chat_id=user, text=message_link)


if __name__ == "__main__":
    main()
    client.run_until_disconnected()
