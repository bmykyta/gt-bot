import logging
import os
import music

from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackQueryHandler,
)
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def main():
    token = os.getenv("telegram_token")
    updater = Updater(token, use_context=True)

    try:
        # Get the dispatcher to register handlers
        dp = updater.dispatcher

        # dp.add_handler(CommandHandler("start", start))
        # dp.add_handler(CommandHandler("help", help_command))

        dp.add_handler(music.music_handler)

        # Start the Bot
        updater.start_polling(poll_interval=2.0)

        updater.idle()
    except Exception as e:
        print("Smth go wrong")


if __name__ == '__main__':
    main()
