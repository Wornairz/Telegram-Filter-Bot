from telegram.constants import ParseMode
from telegram.ext import CommandHandler, CallbackQueryHandler
from telethon.sync import events
from telethon.tl.custom import Message

from src.handlers import button_handler_channel, button_handler_keyword, confirm_delete_channel, start, get_channel_list, get_keyword_list, get_add_channel_handler, get_add_keywords_handler, \
    get_remove_keywords_handler, get_remove_channel_handler, confirm_delete_keyword
from src.settings import get_telegram_application, get_telegram_client
from src.functions import get_user_channels, get_user_keywords, get_all_users_data

client = get_telegram_client()
application = get_telegram_application()


def main() -> None:

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("channel_list", get_channel_list))
    application.add_handler(CommandHandler("keyword_list", get_keyword_list))
    application.add_handler(CommandHandler("remove_channels", get_remove_channel_handler))
    application.add_handler(CommandHandler("remove_keywords", get_remove_keywords_handler))

    application.add_handler(get_add_channel_handler())
    # application.add_handler(get_remove_channel_handler())
    application.add_handler(get_add_keywords_handler())
    # application.add_handler(get_remove_keywords_handler())

    application.add_handler(CallbackQueryHandler(button_handler_keyword, pattern="^keyword?"))
    application.add_handler(CallbackQueryHandler(button_handler_channel, pattern="^channel?"))
    application.add_handler(CallbackQueryHandler(confirm_delete_channel, pattern="^(deleteChannel?|cancel)"))    
    application.add_handler(CallbackQueryHandler(confirm_delete_keyword, pattern="^(deleteKeyword?|cancel)"))    
    application.run_polling()


@client.on(events.NewMessage)
async def handle_new_message(event: Message):
    channel_username = event.chat.username if event.chat is not None else event.chat_id
    message_id = event.message.id
    for user_data in get_all_users_data():
        user_id = user_data.get("user")
        if channel_username in get_user_channels(user_id):
            for keyword in get_user_keywords(user_id):
                if keyword.lower() in event.text.lower():
                    message_title = f"Trovata corrispondenza con la keyword <b>{keyword}</b> nel canale <i>{event.chat.title}</i>"
                    message_link = f"https://t.me/{channel_username}/{message_id}"
                    await application.bot.send_message(
                        chat_id=user_id,
                        text=message_title + "\n\n" + message_link,
                        parse_mode=ParseMode.HTML,
                    )

if __name__ == "__main__":
    main()
    client.run_until_disconnected()