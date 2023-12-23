from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)
from settings import *
from messages import *


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Ciao! Sono il tuo bot. Sono in ascolto su diversi canali."
    )


def echo(update: Update, context: CallbackContext) -> None:
    # Puoi gestire i messaggi ricevuti qui
    chat_id = update.message.chat_id
    message_text = update.message.text
    context.bot.send_message(chat_id=chat_id, text=f"Hai detto: {message_text}")


def main() -> None:
    updater = Updater(token=TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    for channel in CHANNELS:
        dp.add_handler(MessageHandler(Filters.chat(chat_id=channel), echo))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
