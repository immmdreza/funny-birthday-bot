from typing import overload
from update_managers.filters import AbstractFilter
from telegram import Message
import re


class Text(AbstractFilter[Message]):
    def _check(self, update: Message) -> bool:
        return update.text is not None


class TextRegex(AbstractFilter[Message]):
    @overload
    def __init__(self, regex: str) -> None: ...

    @overload
    def __init__(self, regex: re.Pattern[str]) -> None: ...

    def __init__(self, regex: str | re.Pattern[str]) -> None:
        if isinstance(regex, str):
            self._regex = re.compile(regex)
        else:
            self._regex = regex

    def _check(self, update: Message) -> bool:
        return update.text is not None and \
            self._regex.search(update.text) is not None
