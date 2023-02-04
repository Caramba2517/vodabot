from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup


def start() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Начать регистрацию', callback_data='register')]
    ]
    )
    return kb


def help() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Посмотреть прошлые счетчики', callback_data='all')]
    ]
    )
    return kb


def register() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Синопская', callback_data='sin')],
        [InlineKeyboardButton('Фасоль', callback_data='fas')],
        [InlineKeyboardButton('Лифляндская', callback_data='lif')],
        [InlineKeyboardButton('Римского-Корсакова', callback_data='rk')],
        [InlineKeyboardButton('Стачек', callback_data='st')],

    ]
    )
    return kb


def give_count() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Подать счетчики', callback_data='give_count')]
    ])
    return kb

def appeove() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Подтвердить', callback_data='approve')]
    ])
    return kb