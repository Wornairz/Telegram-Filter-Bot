import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    ConversationHandler,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from settings import *

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

ADD_CHANNELS, REMOVE_CHANNELS, ADD_KEYWORDS, REMOVE_KEYWORDS = range(4)

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Ciao! Sono il tuo bot. Sono in ascolto su diversi canali."
    )

async def add_channels(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        "Inserisci i canali che vorresti tracciare. Quando hai finito usa /stop."
    )
    return ADD_CHANNELS

    
async def add_channels_message(update: Update, context: CallbackContext) -> int:
    #TODO: validation
    CHANNELS.append(update.message.text)
    await update.message.reply_text(
        "Canale aggiunto alla lista"
    )
    return ADD_CHANNELS

async def remove_channels(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        "Rimuovi i canali che non vuoi più tracciare. Quando hai finito usa /stop."
    )
    return REMOVE_CHANNELS

async def remove_channels_message(update: Update, context: CallbackContext) -> int:
    #TODO: validation
    CHANNELS.remove(update.message.text)
    await update.message.reply_text(
        "Canale rimosso"
    )
    return REMOVE_CHANNELS

async def add_keywords(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        "Inserisci le keywords che vorresti tracciare. Quando hai finito usa /stop."
    )
    return ADD_KEYWORDS

    
async def add_keywords_message(update: Update, context: CallbackContext) -> int:
    #TODO: validation
    KEYWORDS.append(update.message.text)
    await update.message.reply_text(
        "keyword aggiunta alla lista"
    )
    return ADD_KEYWORDS

async def remove_keywords(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        "Rimuovi le keywords che non vuoi più tracciare. Quando hai finito usa /stop."
    )
    return REMOVE_KEYWORDS

async def remove_keywords_message(update: Update, context: CallbackContext) -> int:
    #TODO: validation
    KEYWORDS.remove(update.message.text)
    await update.message.reply_text(
        "keyword rimossa"
    )
    return REMOVE_KEYWORDS

async def stop_interact(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Ok, basta"
    )
    return ConversationHandler.END

async def get_channel_list(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "canali tracciati: " + str(CHANNELS)
    )

async def get_keyword_list(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "keyword attuali: " + str(KEYWORDS)
    )
