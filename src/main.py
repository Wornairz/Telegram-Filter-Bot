from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler
from settings import TOKEN, API_ID, API_HASH, PHONE_NUMBER, CHANNELS, USERS, KEYWORDS
from telethon.sync import TelegramClient, events
from telethon.tl.custom import Message
from handlers import *

client = TelegramClient("bot", API_ID, API_HASH).start(phone=PHONE_NUMBER)
application = Application.builder().token(TOKEN).build()


def main() -> None:
    application.add_handler(CommandHandler("start", start))
    
    add_channel_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("add_channels", add_channels)],
        states={ADD_CHANNELS: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_channels_message)]},
        fallbacks=[CommandHandler("stop", stop_interact)],
    )

    remove_channel_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("remove_channels", remove_channels)],
        states={REMOVE_CHANNELS: [MessageHandler(filters.TEXT & ~filters.COMMAND, remove_channels_message)]},
        fallbacks=[CommandHandler("stop", stop_interact)],
    )

    add_keywords_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("add_keywords", add_keywords)],
        states={ADD_KEYWORDS: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_keywords_message)]},
        fallbacks=[CommandHandler("stop", stop_interact)],
    )

    remove_keywords_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("remove_keywords", remove_keywords)],
        states={REMOVE_KEYWORDS: [MessageHandler(filters.TEXT & ~filters.COMMAND, remove_keywords_message)]},
        fallbacks=[CommandHandler("stop", stop_interact)],
    )

    application.add_handler(add_channel_conv_handler)
    application.add_handler(remove_channel_conv_handler)
    application.add_handler(add_keywords_conv_handler)
    application.add_handler(remove_keywords_conv_handler)
    application.run_polling()


@client.on(events.NewMessage)
async def handle_new_message(event: Message):
    channel_username = event.chat.username if event.chat is not None else event.chat_id
    message_id = event.message.id
    if channel_username in CHANNELS:
        for keyword in KEYWORDS:
            if keyword.lower() in event.text.lower():
                for user in USERS:
                    message_title = f"Trovata corrispondenza con la keyword <b>{keyword}</b> nel canale <i>{event.chat.title}</i>"
                    message_link = f"https://t.me/{channel_username}/{message_id}"
                    await application.bot.send_message(
                        chat_id=user,
                        text=message_title + "\n\n" + message_link,
                        parse_mode=ParseMode.HTML,
                    )


if __name__ == "__main__":
    main()
    client.run_until_disconnected()
