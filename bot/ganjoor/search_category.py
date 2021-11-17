# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT
import json

from logging import ERROR, INFO
from ganjoor import Ganjoor
from uuid import uuid4
from ganjoor.models import Poet
from telegram.ext import Dispatcher, CallbackContext, InlineQueryHandler
from telegram import (Update, InlineQueryResultArticle,
                      InputTextMessageContent)
from utils.logger import get_logger
from utils.telegram.keyboards import loading_keyboard
from functools import partial

logger = get_logger(__name__)

PRIORITY = 8


def init(dispatcher: Dispatcher, ganjoor: Ganjoor):
    dispatcher.add_handler(
        InlineQueryHandler(
            partial(search_cat_poems, ganjoor=ganjoor), pattern=r"#category_[0-9]+:"))


def search_cat_poems(update: Update, context: CallbackContext, ganjoor: Ganjoor) -> None:
    """Send all recitations of a random poem from hafez."""
    offset = update.inline_query.offset
    offset = int(offset) if offset else 0
    cat_id = update.inline_query.query.split(
        ':')[0].strip().split('_')[1].strip()
    query = update.inline_query.query.split(':')[1].strip()
    term = query
    logger.log(INFO, term)
    poet = ganjoor.find_category_by_id(cat_id, with_poems=False).poet
    results = []
    try:
        if not term:
            cat = ganjoor.find_category_by_id(cat_id, with_poems=True)
            poems = cat.poems
            results = [
                InlineQueryResultArticle(
                    id=str(uuid4())+":"+str(poem.id),
                    title=poem.title,
                    description=poem.excerpt,
                    thumb_url=cat.poet.avatar_url,
                    input_message_content=InputTextMessageContent(
                        poem.excerpt
                    ),
                    reply_markup=loading_keyboard()
                )

                for poem in poems[offset*10:offset*10+10]
            ]
        else:
            poems = ganjoor.search_poems(
                term, page_size=10, page_number=offset+1, cat_id=cat_id, poet_id=poet.id)
            results = []
            for poem in poems:
                excerpt_list = [str(poem).split('\n')[i] for i in range(
                    len(str(poem).split('\n'))) if term in (str(poem).split('\n')[i])]
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
                        ), reply_markup=loading_keyboard())

                )
    except Exception as e:
        logger.log(ERROR, e)
    update.inline_query.offset = 5
    update.inline_query.answer(
        results, cache_time=0, next_offset=offset+1,)
