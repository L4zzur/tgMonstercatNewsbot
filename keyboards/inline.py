from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def new_post_kb() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="Новая новость", callback_data="new_post"),
        ],
    ]
    kb = InlineKeyboardMarkup(row_width=1, inline_keyboard=buttons)
    return kb
