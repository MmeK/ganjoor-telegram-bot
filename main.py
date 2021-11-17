# coding: utf-8
import signal
import sys
import os
from ganjoor.ganjoor import Ganjoor
from telegram.botcommand import BotCommand

from telegram.ext import Updater, Dispatcher
from importlib import import_module
# import inflection

import utils.logger as logger
import configurations.settings as settings


def load_handlers(dispatcher: Dispatcher, ganjoor: Ganjoor):
    """Load handlers from files in a 'bot' directory."""
    base_path = os.path.join(os.path.dirname(__file__), 'bot')
    ganjoor_base_path = os.path.join(base_path, 'ganjoor')

    files = os.listdir(base_path)
    ganjoor_files = os.listdir(ganjoor_base_path)

    commands = list(filter(lambda x: (x != "__pycache__")
                           and (".py" in x), files))
    ganjoor_commands = list(filter(lambda x: (x != "__pycache__")
                                   and (".py" in x), ganjoor_files))

    modules = []
    for command in commands:
        handler_module, _ = os.path.splitext(command)
        module = import_module(f'.{handler_module}', 'bot')
        modules.append(module)

    for command in ganjoor_commands:
        handler_module, _ = os.path.splitext(command)
        module = import_module(f'.{handler_module}', 'bot.ganjoor')
        modules.append(module)

    modules.sort(key=lambda x: getattr(x, 'PRIORITY', 0))
    for module in modules:
        if 'bot.ganjoor' in module.__name__:
            module.init(dispatcher, ganjoor)
        else:
            module.init(dispatcher)


def graceful_exit(*args, **kwargs):
    """Provide a graceful exit from a webhook server."""
    if updater is not None:
        updater.bot.delete_webhook()

    sys.exit(1)


def app():
    global updater
    logger.init_logger(f'logs/{settings.NAME}.log')

    updater = Updater(token=settings.TOKEN, use_context=True)

    updater.bot.set_my_commands(commands=[BotCommand(
        command='/start', description='نمایش صفحه‌ي اصلی')])

    ganjoor = Ganjoor(cache_time=settings.CACHE_TIME)

    load_handlers(updater.dispatcher, ganjoor)

    if settings.WEBHOOK:
        signal.signal(signal.SIGINT, graceful_exit)
        updater.start_webhook(**settings.WEBHOOK_OPTIONS)
        updater.bot.set_webhook(url=settings.WEBHOOK_URL)
    else:
        updater.start_polling()


if __name__ == "__main__":
    app()
