# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT
from functools import partial
from telegram.ext import Dispatcher
from telegram.ext.callbackcontext import CallbackContext
from telegram.files.inputmedia import InputMediaPhoto
from telegram.files.photosize import PhotoSize
from telegram.update import Update
from utils.telegram import CustomChosenInlineResultHandler
from utils.telegram.keyboards import poet_keyboard
from utils.telegram.message_strings import poet_description_string
from ganjoor import Ganjoor


def init(dispatcher: Dispatcher, ganjoor: Ganjoor):
    dispatcher.add_handler(CustomChosenInlineResultHandler(
        partial(chosen_poet, ganjoor=ganjoor), pattern='#poet:')
    )


def chosen_poet(update: Update, context: CallbackContext, ganjoor: Ganjoor):
    m_id = update.chosen_inline_result.inline_message_id
    p_id = (update.chosen_inline_result.result_id).split(':')[1]
    poet = ganjoor.find_poet_by_id(p_id)
    reply_markup = poet_keyboard(poet, m_id)
    context.bot.edit_message_text(
        inline_message_id=update.chosen_inline_result.inline_message_id, text=poet_description_string(
            poet), reply_markup=reply_markup)
