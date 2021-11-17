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
        partial(chosen_faal, ganjoor=ganjoor), pattern='#faal')
    )


def chosen_faal(update: Update, context: CallbackContext, ganjoor: Ganjoor):
    m_id = update.chosen_inline_result.inline_message_id
    faal = ganjoor.hafez_faal()
    reply_markup = poem_keyboard(faal, m_id=m_id)
    context.bot.edit_message_text(
        inline_message_id=update.chosen_inline_result.inline_message_id, text=poem_string(
            faal, p_name='حافظ شیرازی'), reply_markup=reply_markup)
