from aiogram.utils.keyboard import InlineKeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardBuilder, \
    ReplyKeyboardBuilder, ReplyKeyboardMarkup, \
    KeyboardButton

from src.tgbot.common.keyboards.wrapper import keyboard


@keyboard()
def inline_menu_markup(builder: InlineKeyboardBuilder) -> InlineKeyboardMarkup:
    builder.row(
        InlineKeyboardButton(
            text="Inline",
            callback_data="inline_menu"
        )
    )


@keyboard(inline=False, resize_keyboard=True)
def menu_markup(builder: ReplyKeyboardBuilder) -> ReplyKeyboardMarkup:
    builder.row(
        KeyboardButton(text="1"),
    )
