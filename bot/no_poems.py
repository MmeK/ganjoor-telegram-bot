# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT
from logging import INFO
from utils.logger import get_logger
from telegram import Update
from telegram.ext import CallbackQueryHandler, CallbackContext, Dispatcher
logger = get_logger(__name__)


def init(dispatcher: Dispatcher):
    dispatcher.add_handler(CallbackQueryHandler(
        no_poems, pattern='no_poems'))


def no_poems(update: Update, context: CallbackContext):
    query = update.callback_query
    # query.answer()
    query.answer(
        text="شعری وجود ندارد")
