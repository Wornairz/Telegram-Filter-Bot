from telegram.constants import ParseMode
from telegram.ext import CommandHandler, CallbackQueryHandler
from telethon.sync import events
from telethon.tl.custom import Message

from src.handlers import (
    button_handler_channel,
    button_handler_keyword,
    confirm_delete_channel,
    start,
    get_channel_list,
    get_keyword_list,
    get_add_channel_handler,
    get_add_keywords_handler,
    get_remove_keywords_handler,
    get_remove_channel_handler,
    confirm_delete_keyword,
)
from src.settings import get_telegram_application, get_telegram_client
from src.functions import get_user_channels, get_user_keywords, get_all_users_data

client = get_telegram_client()
application = get_telegram_application()


def main() -> None:

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("channel_list", get_channel_list))
    application.add_handler(CommandHandler("keyword_list", get_keyword_list))
    application.add_handler(
        CommandHandler("remove_channels", get_remove_channel_handler)
    )
    application.add_handler(
        CommandHandler("remove_keywords", get_remove_keywords_handler)
    )

    application.add_handler(get_add_channel_handler())
    # application.add_handler(get_remove_channel_handler())
    application.add_handler(get_add_keywords_handler())
    # application.add_handler(get_remove_keywords_handler())

    application.add_handler(
        CallbackQueryHandler(button_handler_keyword, pattern="^keyword?")
    )
    application.add_handler(
        CallbackQueryHandler(button_handler_channel, pattern="^channel?")
    )
    application.add_handler(
        CallbackQueryHandler(confirm_delete_channel, pattern="^(deleteChannel?|cancel)")
    )
    application.add_handler(
        CallbackQueryHandler(confirm_delete_keyword, pattern="^(deleteKeyword?|cancel)")
    )
    application.run_polling()


@client.on(events.NewMessage)
async def handle_new_message(event: Message):
    await check_message_against_user_keywords(event)


async def check_message_against_user_keywords(event: Message):
    channel_identifier = get_channel_identifier(event)
    message_text = event.text.lower()
    message_id = event.message.id

    users_data = get_all_users_data()
    for user_data in users_data:
        user_id = user_data.get("user")
        if is_user_subscribed_to_channel(user_id, channel_identifier):
            keywords = get_user_keywords(user_id)
            await check_keywords_and_notify(
                user_id,
                keywords,
                message_text,
                channel_identifier,
                event.chat.title,
                message_id,
            )


def get_channel_identifier(event: Message):
    return event.chat.username if event.chat is not None else event.chat_id


async def check_keywords_and_notify(
    user_id, keywords, message_text, channel_identifier, chat_title, message_id
):
    for keyword in keywords:
        if keyword.lower() in message_text:
            await send_keyword_match_message(
                user_id, keyword, chat_title, channel_identifier, message_id
            )


async def send_keyword_match_message(
    user_id, keyword, chat_title, channel_identifier, message_id
):
    message_title = f"Trovata corrispondenza con la keyword <b>{keyword}</b> nel canale <i>{chat_title}</i>"
    message_link = f"https://t.me/{channel_identifier}/{message_id}"
    await application.bot.send_message(
        chat_id=user_id,
        text=message_title + "\n\n" + message_link,
        parse_mode=ParseMode.HTML,
    )


def is_user_subscribed_to_channel(user_id, channel_identifier):
    user_channels = get_user_channels(user_id)
    return channel_identifier in user_channels


if __name__ == "__main__":
    main()
    client.run_until_disconnected()
