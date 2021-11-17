
# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT
# Telegram API framework core imports
from functools import partial
import re
from ganjoor.ganjoor import Ganjoor
from telegram.ext import Dispatcher, CallbackContext
from telegram import Update
from telegram.ext.filters import Filters
# Helper methods import
from utils.logger import get_logger
from utils.telegram.keyboards import poem_keyboard
from utils.telegram.message_strings import poem_string
# Telegram API framework handlers imports
from telegram.ext import MessageHandler

# Init logger
logger = get_logger(__name__)


def init(dispatcher: Dispatcher, ganjoor: Ganjoor):
    """Provide handlers initialization."""
    dispatcher.add_handler(MessageHandler(Filters.regex(
        r'/poem_(\d)+'), partial(poem_id, ganjoor=ganjoor)))


def poem_id(update: Update, context: CallbackContext, ganjoor: Ganjoor) -> int:
    """Process a /start command."""
    command = re.search(r"/poem_(\d)+", update.message.text).group()
    p_id = (command).split('_')[1]
    poem = ganjoor.find_poem_by_id(
        p_id, navigation=True, images=True, recitations=True, songs=True, rhymes=True)
    reply_markup = poem_keyboard(poem, update.update_id)
    update.message.reply_text(text=poem_string(
        poem), reply_markup=reply_markup)
