
# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT
# Telegram API framework core imports
from collections import namedtuple
from functools import partial
import re
from ganjoor.ganjoor import Ganjoor
from telegram.ext import Dispatcher, CallbackContext
from telegram import Update
from telegram.ext.filters import Filters
from utils.telegram.keyboards import poet_keyboard
# Helper methods import
from utils.logger import get_logger
# Telegram API framework handlers imports
from telegram.ext import MessageHandler

from utils.telegram.message_strings import poet_description_string

# Init logger
logger = get_logger(__name__)


def init(dispatcher: Dispatcher, ganjoor: Ganjoor):
    """Provide handlers initialization."""
    dispatcher.add_handler(MessageHandler(Filters.regex(
        r'/poet_(\d)+'), partial(poet_id, ganjoor=ganjoor)))


def poet_id(update: Update, context: CallbackContext, ganjoor: Ganjoor) -> int:
    """Process a /start command."""
    command = re.search(r"/poet_(\d)+", update.message.text).group()
    p_id = (command).split('_')[1]
    m_id = (command).split('_')[2]
    poet = ganjoor.find_poet_by_id(p_id)
    reply_markup = poet_keyboard(poet, m_id)
    update.message.reply_photo(photo=poet.avatar_url,
                               caption=poet_description_string(poet), reply_markup=reply_markup)
