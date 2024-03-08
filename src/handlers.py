from telegram import Update
from telegram.ext import (
    ConversationHandler,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    filters,
)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from .settings import get_telegram_client, get_db_collection, get_logger
from .functions import (
    get_user_channels,
    get_user_keywords,
    create_user,
    remove_channel,
    remove_keyword,
)
from .utils import create_keyboard

ADD_CHANNELS, REMOVE_CHANNELS, ADD_KEYWORDS, REMOVE_KEYWORDS = range(4)


async def start(update: Update, _: CallbackContext) -> None:
    create_user(update.message.chat_id)
    await update.message.reply_text(
        "Ciao! Sono il tuo bot. Sono in ascolto su diversi canali."
    )


async def button_handler_keyword(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    keyword_name = query.data.split("?")[1]
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("SI", callback_data=f"deleteKeyword?{keyword_name}"),
            InlineKeyboardButton("NO", callback_data="cancel"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=f"Sei sicuro di voler cancellare '{keyword_name}'?",
        reply_markup=reply_markup,
    )


async def button_handler_channel(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    channel_name = query.data.split("?")[1]
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("SI", callback_data=f"deleteChannel?{channel_name}"),
            InlineKeyboardButton("NO", callback_data="cancel"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=f"Sei sicuro di voler cancellare '{channel_name}'?",
        reply_markup=reply_markup,
    )


async def confirm_delete_keyword(update, context) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data
    if data.startswith("deleteKeyword?"):
        keyword_name = data.split("?")[1]
        remove_keyword(update.effective_chat.id, keyword_name)
        await query.edit_message_text(text=f"Keyword '{keyword_name}' cancellata.")
    elif data == "cancel":
        await query.edit_message_text(text="Cancellazione annullata.")


async def confirm_delete_channel(update, context) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data
    if data.startswith("deleteChannel?"):
        channel_name = data.split("?")[1]
        remove_channel(update.effective_chat.id, channel_name)
        await query.edit_message_text(text=f"Canale '{channel_name}' cancellato.")
    elif data == "cancel":
        await query.edit_message_text(text="Cancellazione annullata.")


async def get_channel_list(update: Update, _: CallbackContext) -> None:
    user_channels = get_user_channels(update.message.chat_id)
    msg = "Canali tracciati:\n"
    for channel in user_channels:
        msg += f"<a href='https://t.me/{channel}'>{channel}</a>\n"
    await update.message.reply_text(
        msg, parse_mode="HTML", disable_web_page_preview=True
    )


async def get_keyword_list(update: Update, _: CallbackContext) -> None:
    user_keywords = get_user_keywords(update.message.chat_id)
    msg = "Keywords tracciate:\n•"
    msg += "\n• ".join(user_keywords)
    await update.message.reply_text(msg)


def get_add_channel_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[CommandHandler("add_channels", add_channels)],
        states={
            ADD_CHANNELS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, __add_channels_state)
            ]
        },
        fallbacks=[CommandHandler("stop", stop_interact)],
    )


def get_add_keywords_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[CommandHandler("add_keywords", add_keywords)],
        states={
            ADD_KEYWORDS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, __add_keywords_state)
            ]
        },
        fallbacks=[CommandHandler("stop", stop_interact)],
    )


async def get_remove_channel_handler(update: Update, _: CallbackContext) -> None:
    user_channels = get_user_channels(update.message.chat_id)
    keyboard = create_keyboard(user_channels, 2, "channel")
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Seleziona il canale da rimuovere", reply_markup=reply_markup
    )


async def get_remove_keywords_handler(update: Update, _: CallbackContext) -> None:
    user_keyword = get_user_keywords(update.message.chat_id)
    keyboard = create_keyboard(user_keyword, 2, "keyword")
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Seleziona la keyword da rimuovere", reply_markup=reply_markup
    )


async def add_channels(update: Update, _: CallbackContext) -> int:
    await update.message.reply_text(
        "Inserisci i canali che vorresti tracciare. Quando hai finito usa /stop."
    )
    return ADD_CHANNELS


async def __add_channels_state(update: Update, _: CallbackContext) -> int:
    input_channel_username = update.message.text.lstrip("@").split("/")[-1]
    user_id = update.message.chat_id
    if input_channel_username in get_user_channels(user_id):
        reply_message = "Il canale @" + input_channel_username + " è già tracciato"
        await update.message.reply_text(reply_message)
        return ADD_CHANNELS

    client = get_telegram_client()
    dialogs = await client.get_dialogs()

    subscribed_channels_username = [
        dialog.entity.username
        for dialog in dialogs
        if dialog.is_channel and not dialog.is_group
    ]

    if input_channel_username in subscribed_channels_username:
        find_query = {"user": user_id}
        update_query = {"$addToSet": {"channels": input_channel_username}}
        get_db_collection().update_one(find_query, update_query, upsert=True)
        reply_message = "Canale @" + input_channel_username + " aggiunto alla lista"
    else:
        reply_message = "Non sei iscritto al canale " + input_channel_username
    await update.message.reply_text(reply_message)
    return ADD_CHANNELS


async def remove_channels(update: Update, _: CallbackContext) -> int:
    await update.message.reply_text(
        "Rimuovi i canali che non vuoi più tracciare. Quando hai finito usa /stop."
    )
    return REMOVE_CHANNELS


async def add_keywords(update: Update, _: CallbackContext) -> int:
    await update.message.reply_text(
        "Inserisci le keywords che vorresti tracciare. Quando hai finito usa /stop."
    )
    return ADD_KEYWORDS


async def __add_keywords_state(update: Update, _: CallbackContext) -> int:
    input_keyword = update.message.text
    user_id = update.message.chat_id
    find_query = {"user": user_id}
    if input_keyword not in get_user_keywords(user_id):
        update_query = {"$addToSet": {"keywords": input_keyword}}
        get_db_collection().update_one(find_query, update_query, upsert=True)
        reply_message = "Keyword " + input_keyword + " aggiunta alla lista"
    else:
        reply_message = "La Keyword " + input_keyword + " è già presente, riprova"

    await update.message.reply_text(reply_message)
    return ADD_KEYWORDS


async def remove_keywords(update: Update, _: CallbackContext) -> int:
    await update.message.reply_text(
        "Rimuovi le keywords che non vuoi più tracciare. Quando hai finito usa /stop."
    )
    return REMOVE_KEYWORDS


async def stop_interact(update: Update, _: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    get_logger().info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text("Ok, basta")
    return ConversationHandler.END
