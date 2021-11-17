# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT
from logging import ERROR
from ganjoor import Ganjoor
from uuid import uuid4
from telegram.ext import Dispatcher, CallbackContext, InlineQueryHandler
from telegram import (Update, InlineQueryResultPhoto)
from utils.logger import get_logger
from functools import partial

logger = get_logger(__name__)

PRIORITY = 8


def init(dispatcher: Dispatcher, ganjoor: Ganjoor):
    dispatcher.add_handler(
        InlineQueryHandler(
            partial(poem_images, ganjoor=ganjoor), pattern="#poem-images:"))


def poem_images(update: Update, context: CallbackContext, ganjoor: Ganjoor) -> None:
    """Send all recitations of a random poem from hafez."""
    query = update.inline_query.query.split(':')[1].strip()
    try:
        poem = ganjoor.find_poem_by_id(query, images=True)
        results = [
            InlineQueryResultPhoto(
                id=str(uuid4()),
                photo_url=image.normal_image_url,
                title=image.alt_text,
                thumb_url=image.thumbnail_image_url,
                photo_width=10000, photo_height=10000
            )
            for image in poem.images
        ]
    except Exception as e:
        logger.log(ERROR, e)
        results = []

    update.inline_query.answer(results, cache_time=0)
