# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT

from logging import ERROR
from ganjoor import Ganjoor
from uuid import uuid4
from telegram.ext import Dispatcher, CallbackContext, InlineQueryHandler
from telegram import (Update, InlineQueryResultArticle,
                      InputTextMessageContent)
from utils.logger import get_logger
from functools import partial

from utils.telegram.keyboards import loading_keyboard

logger = get_logger(__name__)

PRIORITY = 8


def init(dispatcher: Dispatcher, ganjoor: Ganjoor):
    dispatcher.add_handler(
        InlineQueryHandler(
            partial(search_poet_poems, ganjoor=ganjoor), pattern="#poet:"))


def search_poet_poems(update: Update, context: CallbackContext, ganjoor: Ganjoor) -> None:
    """Send all recitations of a random poem from hafez."""
    offset = update.inline_query.offset
    offset = int(offset) if offset else 0
    query = update.inline_query.query.split(':')[1].strip()
    poet_name = query
    poets = find_poets(poet_name, ganjoor=ganjoor)
    try:
        if not poets:
            poets = find_poets('', ganjoor=ganjoor)
        results = []
        for poet in poets[offset:offset+5]:
            results.append(
                # InlineQueryResultArticle('/poet_'+str(poet.id)ar_url,
                #     input_message_content=InputTextMessageContent(
                #         '/poet_'+str(poet.id)
                #     )
                # )
                InlineQueryResultArticle(
                    id=str(uuid4())+":"+str(poet.id),
                    title=poet.name,
                    thumb_url=poet.avatar_url,
                    input_message_content=InputTextMessageContent(
                        poet.name
                    ),
                    reply_markup=loading_keyboard())
            )

    except Exception as e:
        logger.log(ERROR, e)
        results = []
    update.inline_query.answer(results, cache_time=0, next_offset=offset+5)


def find_poets(poet_name: str, ganjoor: Ganjoor) -> int:
    poets = ganjoor.get_all_poets()
    poets.sort(key=lambda x: x.id)
    result = []
    for poet in poets:
        if poet_name in poet.name:
            result.append(poet)
    return result
