# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT
from logging import ERROR, INFO
from ganjoor import Ganjoor
from uuid import uuid4
from telegram.ext import Dispatcher, CallbackContext, InlineQueryHandler
from telegram import (Update, InlineQueryResultArticle,
                      InputTextMessageContent)
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup
from utils.logger import get_logger
from functools import partial

from utils.telegram.keyboards import loading_keyboard

logger = get_logger(__name__)

PRIORITY = 8


def init(dispatcher: Dispatcher, ganjoor: Ganjoor):
    dispatcher.add_handler(
        InlineQueryHandler(
            partial(search_poet_poems, ganjoor=ganjoor), pattern=r"#poet_poems_[0-9]+:"))


def search_poet_poems(update: Update, context: CallbackContext, ganjoor: Ganjoor) -> None:
    """Send all recitations of a random poem from hafez."""
    offset = update.inline_query.offset
    offset = int(offset) if offset else 0
    poet_id = update.inline_query.query.split(
        ':')[0].strip().split('_')[2].strip()
    query = update.inline_query.query.split(':')[1].strip()
    term = query
    logger.log(INFO, term)
    results = []
    try:
        if not term:
            poet = ganjoor.find_poet_by_id(poet_id)
            poem = ganjoor.random_poem(poet_id=poet_id)
            results = [
                InlineQueryResultArticle(
                    id=str(uuid4())+":"+str(poem.id),
                    title=poem.title,
                    description=str(poem.verses[0]),
                    thumb_url=poet.avatar_url,
                    input_message_content=InputTextMessageContent(
                        str(poem.verses[0])
                    ),
                    reply_markup=loading_keyboard()
                )]
        else:
            poems = ganjoor.search_poems(
                term, page_size=10, page_number=offset+1, poet_id=poet_id)
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
                            excerpt),
                        reply_markup=loading_keyboard()
                    )
                )
    except Exception as e:
        logger.log(ERROR, e)
    update.inline_query.answer(
        results, cache_time=0, next_offset=offset+1)
