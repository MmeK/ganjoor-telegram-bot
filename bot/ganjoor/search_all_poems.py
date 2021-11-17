# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT
from logging import ERROR, INFO
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
            partial(search_all_poems, ganjoor=ganjoor), pattern="#poems:", run_async=True))


def search_all_poems(update: Update, context: CallbackContext, ganjoor: Ganjoor) -> None:
    """Send all recitations of a random poem from hafez."""
    query = update.inline_query.query.split(':')[1].strip()
    offset = int(
        update.inline_query.offset) if update.inline_query.offset else 0
    logger.log(INFO, query)

    try:
        if not query:
            poem = ganjoor.random_poem()
            results = [
                InlineQueryResultArticle(
                    id=str(uuid4())+":"+str(poem.id),
                    title=poem.full_title,
                    input_message_content=InputTextMessageContent(
                        str(poem.verses[0])
                    ),
                    reply_markup=loading_keyboard())
            ]
        else:
            poems = ganjoor.search_poems(
                query, page_size=10, page_number=offset+1)
            results = []
            for poem in poems:
                excerpt_list = [str(poem).split('\n')[i] for i in range(
                    len(str(poem).split('\n'))) if query in (str(poem).split('\n')[i])]
                excerpt = excerpt_list[0] if excerpt_list else str(poem).split('\n')[
                    0]
                results.append(
                    InlineQueryResultArticle(
                        id=str(uuid4())+":"+str(poem.id),
                        thumb_url=poem.poet.avatar_url,
                        title=poem.poet.name + ' - ' + poem.title,
                        description=excerpt,
                        input_message_content=InputTextMessageContent(
                            excerpt
                        ), reply_markup=loading_keyboard()
                    )
                )
    except Exception as e:
        logger.log(ERROR, e)
        results = []

    update.inline_query.answer(results, cache_time=0, next_offset=offset+1)
