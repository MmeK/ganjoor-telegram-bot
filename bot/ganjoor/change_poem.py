# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT
from logging import INFO
from utils.logger import get_logger
from utils.telegram.keyboards import poem_keyboard
from utils.telegram.message_strings import poem_string
from functools import partial
from telegram import Update
from ganjoor import Ganjoor
from telegram.ext import CallbackQueryHandler, CallbackContext, Dispatcher
logger = get_logger(__name__)


def init(dispatcher: Dispatcher, ganjoor: Ganjoor):
    dispatcher.add_handler(CallbackQueryHandler(
        partial(change_poem, ganjoor=ganjoor), pattern=r'^change_poem_*'))


def change_poem(update: Update, context: CallbackContext, ganjoor: Ganjoor):
    query = update.callback_query
    print("THIS IS QUERY"+query.data)
    poem_id = query.data.split('_')[2]
    message_id = '_'.join(query.data.split('_')[3:])
    print(message_id)
    poem = ganjoor.find_poem_by_id(
        poem_id, navigation=True, images=True, recitations=True, songs=True)
    query.answer()
    keyboard = poem_keyboard(poem, message_id)

    context.bot.edit_message_text(text=poem_string(
        poem), inline_message_id=message_id, reply_markup=keyboard)
