# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT
# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT
from logging import ERROR
from ganjoor import Ganjoor
from uuid import uuid4
from telegram.ext import Dispatcher, CallbackContext, InlineQueryHandler
from telegram import (Update)
from telegram.inline.inlinequeryresultarticle import InlineQueryResultArticle
from telegram.inline.inputtextmessagecontent import InputTextMessageContent
from utils.logger import get_logger
from utils.telegram.message_strings import poem_string
from utils.telegram.keyboards import loading_keyboard, poem_keyboard, start_keyboard
from functools import partial

logger = get_logger(__name__)

PRIORITY = 10


def init(dispatcher: Dispatcher, ganjoor: Ganjoor):
    dispatcher.add_handler(InlineQueryHandler(
        partial(hafez_faal, ganjoor=ganjoor))
    )


def hafez_faal(update: Update, context: CallbackContext, ganjoor: Ganjoor) -> None:
    """Send all recitations of a random poem from hafez."""
    try:
        hafez = ganjoor.find_poet_by_id(2)
    except Exception as e:
        logger.log(ERROR, e)
    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="شروع ربات",
            description="دسترسی به تمام اشعار",
            thumb_url='https://ganjoor.net/image/gm.gif',
            input_message_content=InputTextMessageContent(
                message_text="به ربات شعر خوش آمدید لطفا یکی از گزینه‌ها را انتخاب کنید"),
            reply_markup=start_keyboard())
    ]

    update.inline_query.answer(results, cache_time=0)
