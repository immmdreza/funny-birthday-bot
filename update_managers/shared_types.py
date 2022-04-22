from typing import TypeVar
from telegram import Message, CallbackQuery


UpdateLike = Message | CallbackQuery


T = TypeVar("T", bound=UpdateLike)
