

# Telegram API framework core imports
from collections import namedtuple
from telegram.ext import Dispatcher, CallbackContext
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.files.photosize import PhotoSize
from utils.telegram.keyboards import start_keyboard
# Helper methods import
from utils.logger import get_logger
# Telegram API framework handlers imports
from telegram.ext import CommandHandler

# Init logger
logger = get_logger(__name__)
CallbackData = namedtuple('CallbackData', "menu_name doto")


def init(dispatcher: Dispatcher):
    """Provide handlers initialization."""
    dispatcher.add_handler(CommandHandler('start', start,))


def start(update: Update, context: CallbackContext) -> int:
    """Process a /start command."""

    reply_markup = start_keyboard()
    update.message.reply_photo(
        PhotoSize('https://ganjoor.net/image/gm.gif', 'logo', 50, 50), reply_markup=reply_markup)
