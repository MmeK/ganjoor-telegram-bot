# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT
from functools import partial
from telegram.ext import Dispatcher
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update
from utils.telegram import CustomChosenInlineResultHandler
from utils.telegram.keyboards import poem_keyboard
from utils.telegram.message_strings import poem_string
from ganjoor import Ganjoor


def init(dispatcher: Dispatcher, ganjoor: Ganjoor):
    dispatcher.add_handler(CustomChosenInlineResultHandler(
        partial(chosen_poem, ganjoor=ganjoor), pattern=[
            '#poet_poems', '#poem_similar', '#category', '#poems'])
    )


def chosen_poem(update: Update, context: CallbackContext, ganjoor: Ganjoor):
    m_id = update.chosen_inline_result.inline_message_id
    p_id = (update.chosen_inline_result.result_id).split(':')[1]
    poem = ganjoor.find_poem_by_id(
        p_id, navigation=True, images=True, recitations=True, songs=True, rhymes=True)
    reply_markup = poem_keyboard(poem, m_id=m_id)
    context.bot.edit_message_text(
        inline_message_id=update.chosen_inline_result.inline_message_id, text=poem_string(
            poem), reply_markup=reply_markup)
