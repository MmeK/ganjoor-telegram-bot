# Copyright 2021 Mohammad Kazemi <kazemi.me.222@gmail.com>.
# SPDX-License-Identifier: MIT
from telegram.ext import ChosenInlineResultHandler
from telegram import Update
import re
from typing import Optional, Union


class CustomChosenInlineResultHandler(ChosenInlineResultHandler):
    def check_update(self, update: object) -> Optional[Union[bool, object]]:
        """Determines whether an update should be passed to this handlers :attr:`callback`.
        This overridden method matches the pattern against inline result query instead of id.

        Args:
            update (:class:`telegram.Update` | :obj:`object`): Incoming update.

        Returns:
            :obj:`bool`

        """
        if isinstance(update, Update) and update.chosen_inline_result:
            if type(self.pattern) is list:
                for pat in self.pattern:
                    match = re.match(
                        pat, update.chosen_inline_result.query)
                    if match:
                        return match
            elif self.pattern:
                match = re.match(
                    self.pattern, update.chosen_inline_result.query)
                if match:
                    return match
            else:
                return True
        return None
