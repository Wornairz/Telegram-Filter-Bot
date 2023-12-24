from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackContext,
)
from settings import TOKEN, API_ID, API_HASH, PHONE_NUMBER, CHANNELS, USERS, KEYWORDS
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
    channel_username = event.chat.username
    message_id = event.message.id
    for keyword in KEYWORDS:
        if keyword.lower() in event.text.lower():
            for user in USERS:
                message_title = f"Trovata corrispondenza con la keyword <b>{keyword}</b> nel canale <i>{event.chat.title}</i>"
                message_link = f"https://t.me/{channel_username}/{message_id}"
                await application.bot.send_message(chat_id=user, text=message_title + "\n\n" + message_link, parse_mode=ParseMode.HTML)


if __name__ == "__main__":
    main()
    client.run_until_disconnected()
