
from telegram import Update
from telegram.ext import (
    ConversationHandler,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    filters
)

from .settings import get_telegram_client, get_db_collection, get_logger
from .functions import get_user_channels, get_user_keywords


ADD_CHANNELS, REMOVE_CHANNELS, ADD_KEYWORDS, REMOVE_KEYWORDS = range(4)


async def start(update: Update, _: CallbackContext) -> None:
    await update.message.reply_text(
        "Ciao! Sono il tuo bot. Sono in ascolto su diversi canali."
    )



async def get_channel_list(update: Update, _: CallbackContext) -> None:
    user_channels = get_user_channels(update.message.chat_id)
    await update.message.reply_text(
        "canali tracciati: " + str(user_channels)
    )



async def get_keyword_list(update: Update, _: CallbackContext) -> None:
    user_keywords = get_user_keywords(update.message.chat_id)
    await update.message.reply_text(
        "keyword attuali: " + str(user_keywords)
    )


def get_add_channel_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[CommandHandler("add_channels", add_channels)],
        states={ADD_CHANNELS: [MessageHandler(filters.TEXT & ~filters.COMMAND, __add_channels_state)]},
        fallbacks=[CommandHandler("stop", stop_interact)],
    )


def get_remove_channel_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[CommandHandler("remove_channels", remove_channels)],
        states={REMOVE_CHANNELS: [MessageHandler(filters.TEXT & ~filters.COMMAND, __remove_channels_state)]},
        fallbacks=[CommandHandler("stop", stop_interact)],
    )


def get_add_keywords_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[CommandHandler("add_keywords", add_keywords)],
        states={ADD_KEYWORDS: [MessageHandler(filters.TEXT & ~filters.COMMAND, __add_keywords_state)]},
        fallbacks=[CommandHandler("stop", stop_interact)],
    )


def get_remove_keywords_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[CommandHandler("remove_keywords", remove_keywords)],
        states={REMOVE_KEYWORDS: [MessageHandler(filters.TEXT & ~filters.COMMAND, __remove_keywords_state)]},
        fallbacks=[CommandHandler("stop", stop_interact)],
    )


async def add_channels(update: Update, _: CallbackContext) -> int:
    await update.message.reply_text(
        "Inserisci i canali che vorresti tracciare. Quando hai finito usa /stop."
    )
    return ADD_CHANNELS


async def __add_channels_state(update: Update, _: CallbackContext) -> int:
    input_channel_username = update.message.text.lstrip("@").split('/')[-1]

    user_id = update.message.chat_id

    if input_channel_username in get_user_channels(user_id):
        reply_message = "Il canale @" + input_channel_username + " è già tracciato"
        await update.message.reply_text(reply_message)
        return ADD_CHANNELS

    client = get_telegram_client()
    dialogs = await client.get_dialogs()

    subscribed_channels_username = [dialog.entity.username for dialog in dialogs if
                                    dialog.is_channel and not dialog.is_group]

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


async def __remove_channels_state(update: Update, _: CallbackContext) -> int:
    # TODO: inserire lista bottoni (magari con paginazione)
    input_channel_username = update.message.text.lstrip("@")

    find_query = {"user": update.message.chat_id}
    user_channels = get_db_collection().find_one(find_query).get("channels")
    if input_channel_username in user_channels:
        update_query = {"$pull": {"channels": input_channel_username}}
        get_db_collection().update_one(find_query, update_query)
        reply_message = "Canale @" + input_channel_username + " rimosso dalla lista"
    else:
        reply_message = "Il canale @" + input_channel_username + " non è presente nella lista"

    await update.message.reply_text(reply_message)
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


async def __remove_keywords_state(update: Update, _: CallbackContext) -> int:
    # TODO: inserire lista bottoni (magari con paginazione)
    input_keyword = update.message.text

    find_query = {"user": update.message.chat_id}
    user_keywords = get_db_collection().find_one(find_query).get("keywords")
    if input_keyword in user_keywords:
        update_query = {"$pull": {"keywords": input_keyword}}
        get_db_collection().update_one(find_query, update_query)
        reply_message = "Keyword " + input_keyword + " rimosso dalla lista"
    else:
        reply_message = "La Keyword " + input_keyword + " non è presente nella lista"

    await update.message.reply_text(reply_message)
    return REMOVE_KEYWORDS


async def stop_interact(update: Update, _: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    get_logger().info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Ok, basta"
    )
    return ConversationHandler.END

