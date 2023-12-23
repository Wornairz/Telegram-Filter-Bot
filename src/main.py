from telegram import Update
from telegram.ext import (
    Application,
    Updater,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext,
)
from settings import *
from telethon.sync import TelegramClient, events
from telethon.tl.custom import Message

client = TelegramClient("prova", API_ID, API_HASH).start(phone=PHONE_NUMBER)
application = Application.builder().token(TOKEN).build()


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Ciao! Sono il tuo bot. Sono in ascolto su diversi canali."
    )

def main() -> None:
    application.add_handler(CommandHandler("start", start))
    application.run_polling()


@client.on(events.NewMessage(chats=CHANNELS))
async def handle_new_message(event: Message):
    print(event.message.text)
    # for user in USERS:
    #   await updater.bot.send_message(chat_id=user, text=event.message.text)

    # context.bot.forward_message(
    #    chat_id=user_id,
    #    from_chat_id=update.message.chat_id,
    #    message_id=update.message.message_id,
    # )


if __name__ == "__main__":
    client.run_until_disconnected()
