# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT
from logging import ERROR
from ganjoor import Ganjoor
from uuid import uuid4
from telegram.ext import Dispatcher, CallbackContext, InlineQueryHandler
from telegram import (Update, InlineQueryResultAudio)
from utils.logger import get_logger
from functools import partial

logger = get_logger(__name__)

PRIORITY = 8


def init(dispatcher: Dispatcher, ganjoor: Ganjoor):
    dispatcher.add_handler(
        InlineQueryHandler(
            partial(poem_images, ganjoor=ganjoor), pattern="#poem-recitations:"))


def poem_images(update: Update, context: CallbackContext, ganjoor: Ganjoor) -> None:
    """Send all recitations of a random poem from hafez."""
    query = update.inline_query.query.split(':')[1].strip()
    try:
        poem = ganjoor.find_poem_by_id(query, recitations=True)
        results = [
            InlineQueryResultAudio(
                id=str(uuid4()),
                audio_url=recitation.mp3_url,
                performer=recitation.audio_artist,
                title=poem.poet.name+' - '+poem.title,
                caption=recitation.audio_artist_url
            )
            for recitation in poem.recitations
        ]
    except Exception as e:
        logger.log(ERROR, e)
        results = []

    update.inline_query.answer(results, cache_time=3600)
