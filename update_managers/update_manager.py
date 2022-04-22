import queue
from typing import Any, Callable, cast

from telegram import Bot, CallbackQuery, Update, Message

from .update_hunter import AbstractUpdateHunter, GenericUpdateHunter
from .filters import AbstractFilter
from .shared_types import T


class UpdateManager:
    def __init__(self, bot: Bot) -> None:
        self._bot = bot
        self._queue = queue.Queue[Update]()
        self._hunter: list[AbstractUpdateHunter] = []

    def _register_hunter(self, hunter: AbstractUpdateHunter) -> None:
        self._hunter.append(hunter)

    def register_hunters(self, *hunters: AbstractUpdateHunter) -> None:
        """ Register one or more `AbstractUpdateHunter`(s) to the manager."""
        for hunter in hunters:
            self._register_hunter(hunter)

    def enqueue_update(self, update: Update | None) -> None:
        for hunter in self._hunter:
            if hunter.its_the_hunt(update):
                hunter.hunt(self._bot, cast(Update, update))

    def register(
            self,
            update_resolver: Callable[[Update], T | None],
            filter: AbstractFilter[T]) -> Callable[[Callable[[Bot, T], Any]], None]:
        def decorator(function: Callable[[Bot, T], Any]):
            self._register_hunter(
                GenericUpdateHunter(update_resolver, function, filter))
        return decorator

    def register_message(
            self,
            filter: AbstractFilter[Message]) -> Callable[
                [Callable[[Bot, Message], Any]], None]:
        def decorator(function: Callable[[Bot, Message], Any]):
            self._register_hunter(
                GenericUpdateHunter(
                    lambda update: update.message, function, filter))
        return decorator

    def register_callback_query(
            self,
            filter: AbstractFilter[CallbackQuery]) -> Callable[
                [Callable[[Bot, CallbackQuery], Any]], None]:
        def decorator(function: Callable[[Bot, CallbackQuery], Any]):
            self._register_hunter(
                GenericUpdateHunter(
                    lambda update: update.callback_query, function, filter))
        return decorator
