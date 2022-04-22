import abc
from typing import Any, Callable, Generic

from telegram import Bot, CallbackQuery, Message, Update

from .filters import AbstractFilter, CallbackQueryFilter, MessageFilter
from .shared_types import T


class AbstractUpdateHunter(abc.ABC):
    @abc.abstractmethod
    def its_the_hunt(self, update: Update | None) -> bool:
        ...

    @abc.abstractmethod
    def hunt(self, bot: Bot, update: Update) -> Any:
        ...


class GenericAbstractUpdateHunter(Generic[T], AbstractUpdateHunter):
    def __init__(self, update_resolver: Callable[[Update], T | None]) -> None:
        self._update_resolver: Callable[[Update], T | None] = update_resolver

    def its_the_hunt(self, update: Update | None) -> bool:
        if update is None:
            return False
        inner_update = self._update_resolver(update)
        if inner_update is not None:
            return self._its_the_hunt(inner_update)
        return False

    def hunt(self, bot: Bot, update: Update) -> Any:
        inner_update = self._update_resolver(update)
        if inner_update is not None:
            self._hunt(bot, inner_update)
        else:
            raise ValueError("Update is not resolved")

    @abc.abstractmethod
    def _its_the_hunt(self, update: T) -> bool:
        ...

    @abc.abstractmethod
    def _hunt(self, bot: Bot,  update: T) -> Any:
        ...


class GenericUpdateHunter(Generic[T], GenericAbstractUpdateHunter[T]):
    def __init__(
            self,
            update_resolver: Callable[[Update], T | None],
            callback: Callable[[Bot, T], Any],
            filter: AbstractFilter[T]) -> None:
        super().__init__(update_resolver)
        self._callback = callback
        self._filter = filter

    def _its_the_hunt(self, update: T | None) -> bool:
        return update is not None and self._filter.check(update)

    def _hunt(self, bot: Bot,  update: T) -> Any:
        return self._callback(bot, update)


class MessageHunter(GenericUpdateHunter[Message]):
    def __init__(
            self,
            callback: Callable[[Bot, Message], Any],
            filter: MessageFilter) -> None:
        super().__init__(lambda update: update.message, callback, filter)

    def _its_the_hunt(self, update: Message | None) -> bool:
        return update is not None and self._filter.check(update)

    def _hunt(self, bot: Bot,  update: Message) -> Any:
        self._callback(bot, update)


class CallbackQueryHunter(GenericUpdateHunter[CallbackQuery]):
    def __init__(
            self,
            callback: Callable[[Bot, CallbackQuery], Any],
            filter: CallbackQueryFilter) -> None:
        super().__init__(lambda update: update.callback_query, callback, filter)

    def _its_the_hunt(self, update: CallbackQuery | None) -> bool:
        return update is not None and self._filter.check(update)

    def _hunt(self, bot: Bot,  update: CallbackQuery) -> Any:
        self._callback(bot, update)
