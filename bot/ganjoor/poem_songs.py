# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT
from logging import ERROR
from ganjoor import Ganjoor
from uuid import uuid4
from telegram.ext import Dispatcher, CallbackContext, InlineQueryHandler
from telegram import (Update, InlineQueryResultArticle,
                      InputTextMessageContent, InlineQueryResultAudio)
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup
from utils.logger import get_logger
from functools import partial

logger = get_logger(__name__)

PRIORITY = 8


def init(dispatcher: Dispatcher, ganjoor: Ganjoor):
    dispatcher.add_handler(
        InlineQueryHandler(
            partial(poem_images, ganjoor=ganjoor), pattern="#poem-songs:"))


def poem_images(update: Update, context: CallbackContext, ganjoor: Ganjoor) -> None:
    """Send all songs of a random poem from hafez."""
    query = update.inline_query.query.split(':')[1].strip()
    try:
        poem = ganjoor.find_poem_by_id(query, songs=True)
        results = []
        for song in poem.songs:
            results.append(InlineQueryResultArticle(
                id=str(uuid4())+":"+str(poem.id)+":"+str(song.id),
                title=song.track_name,
                input_message_content=InputTextMessageContent(
                    song.artist_name+'\n\n'+song.track_url
                ), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('در حال بارگزاری', callback_data='loading')]])
            ))

    except Exception as e:
        logger.log(ERROR, e)
        results = []

    update.inline_query.answer(results, cache_time=0)
