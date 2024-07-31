from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.filters.callback_data import CallbackData


TOKEN = "7451251483:AAGNpqnHcQSqK0VAixCsXJQRLempe3gdTOM"


class ChoiceCallback(CallbackData, prefix="choice"):
    option: str


KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/start")],
        [KeyboardButton(text="/help")],
        [KeyboardButton(text="/echo")],
        [KeyboardButton(text="/photo")],
        [KeyboardButton(text="/inline")],
        [KeyboardButton(text="/start_fsm")],
    ],
    resize_keyboard=True,
)

INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Выбор 1", callback_data=ChoiceCallback(option="1").pack()
            )
        ],
        [
            InlineKeyboardButton(
                text="Выбор 2", callback_data=ChoiceCallback(option="2").pack()
            )
        ],
    ]
)
