from typing import Callable

from aiogram.utils.keyboard import \
    InlineKeyboardBuilder, InlineKeyboardMarkup, \
    ReplyKeyboardMarkup, ReplyKeyboardBuilder


def keyboard(inline: bool = True, **keyboard_kwargs):
    def kb_wrapper(func: Callable):
        def wrapper(*args, **kwargs):
            builder = InlineKeyboardBuilder() \
                if inline else ReplyKeyboardBuilder()

            kwargs["builder"] = builder
            func(*args, **kwargs)
            return builder.as_markup(**keyboard_kwargs)

        return wrapper
    return kb_wrapper
