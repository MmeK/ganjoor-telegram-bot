# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT
from utils.logger import get_logger
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext, Dispatcher
logger = get_logger(__name__)


def init(dispatcher: Dispatcher):
    dispatcher.add_handler(CommandHandler('help', help))


def help(update: Update, context: CallbackContext):
    custom_keyboard = [['top-left', 'top-right'],
                       ['bottom-left', 'bottom-right']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Custom Keyboard Test",
                             reply_markup=reply_markup)
