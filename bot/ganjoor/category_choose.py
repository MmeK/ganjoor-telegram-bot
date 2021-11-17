
# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT
# Telegram API framework core imports
from collections import namedtuple
from functools import partial
from ganjoor.ganjoor import Ganjoor
from telegram.ext import Dispatcher, CallbackContext
from telegram import Update
# Helper methods import
from utils.logger import get_logger
from utils.telegram.keyboards import category_keyboard
# Telegram API framework handlers imports
from telegram.ext import CallbackQueryHandler

# Init logger
logger = get_logger(__name__)
CallbackData = namedtuple('CallbackData', "menu_name doto")


def init(dispatcher: Dispatcher, ganjoor: Ganjoor):
    """Provide handlers initialization."""
    dispatcher.add_handler(CallbackQueryHandler(
        partial(category_id, ganjoor=ganjoor), pattern=r'^category_*'))


def category_id(update: Update, context: CallbackContext, ganjoor: Ganjoor) -> int:
    """Process a /start command."""
    query = update.callback_query

    message_id = '_'.join(query.data.split('_')[2:])
    cat_id = query.data.split('_')[1]
    cat = ganjoor.find_category_by_id(cat_id, with_poems=True)

    # query.answer()
    query.answer()

    context.bot.edit_message_reply_markup(
        inline_message_id=message_id, reply_markup=category_keyboard(cat, message_id))
    # query.edit_reply_markup()
