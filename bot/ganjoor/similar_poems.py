# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT
from functools import partial
from logging import ERROR
from uuid import uuid4
from ganjoor import Ganjoor
from ganjoor.exceptions import GanjoorException
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.dispatcher import Dispatcher
from telegram.ext.inlinequeryhandler import InlineQueryHandler
from telegram.inline.inlinequeryresultarticle import InlineQueryResultArticle
from telegram.inline.inputtextmessagecontent import InputTextMessageContent
from telegram.update import Update

from utils.logger import get_logger
from utils.telegram.keyboards import loading_keyboard

logger = get_logger(__name__)


def init(dispatcher: Dispatcher, ganjoor: Ganjoor):
    dispatcher.add_handler(
        InlineQueryHandler(
            partial(similar_poems, ganjoor=ganjoor), pattern=r"#poem_similar:"))


def similar_poems(update: Update, context: CallbackContext, ganjoor: Ganjoor):
    query_args = update.inline_query.query.split(':')
    metre = query_args[1].strip()
    rhyme = query_args[2].strip() if (len(query_args) > 2) else None
    offset = int(
        update.inline_query.offset) if update.inline_query.offset else 0
    try:
        poems = ganjoor.find_similar_poems(
            10, offset+1, metre=metre, rhyme=rhyme)
    except GanjoorException as e:
        logger.log(ERROR, e)
    results = [
        InlineQueryResultArticle(
            id=str(uuid4())+":"+str(poem.id),
            thumb_url=poem.poet.avatar_url,
            title=poem.poet.name + ' - ' + poem.title,
            description=str(poem.plain_text.split('\n')[0]),
            input_message_content=InputTextMessageContent(
                str(poem.plain_text.split('\n')[0])),
            reply_markup=loading_keyboard()
        ) for poem in poems
    ]
    update.inline_query.answer(results, cache_time=0, next_offset=offset+1)
