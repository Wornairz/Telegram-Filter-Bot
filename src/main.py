from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackContext,
)
from settings import *
from telethon.sync import TelegramClient, events
from telethon.tl.custom import Message

client = TelegramClient("prova", API_ID, API_HASH).start(phone=PHONE_NUMBER)
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
    for user in USERS:
        print(user)
        print(event.chat_id)
        print(event.message.id)
        await application.bot.forward_message(chat_id=user, from_chat_id=event.chat_id, message_id=event.message.id)


if __name__ == "__main__":
    main()
    client.run_until_disconnected()
