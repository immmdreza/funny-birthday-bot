import abc
from typing import Callable, Generic
from .shared_types import T
from telegram import Message, CallbackQuery


class AbstractFilter(abc.ABC, Generic[T]):
    @abc.abstractmethod
    def _check(self, update: T) -> bool:
        ...

    def check(self, update: T) -> bool:
        return self._check(update)


class Filter(Generic[T], AbstractFilter[T]):
    def __init__(self, filter: Callable[[T], bool]) -> None:
        self._filter: Callable[[T], bool] = filter

    def _check(self, update: T) -> bool:
        return self._filter(update)


class MessageFilter(Filter[Message]):
    def __init__(self, filter: Callable[[Message], bool]) -> None:
        super().__init__(filter)


class CallbackQueryFilter(Filter[CallbackQuery]):
    def __init__(self, filter: Callable[[CallbackQuery], bool]) -> None:
        super().__init__(filter)
