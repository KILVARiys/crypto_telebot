from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Функция для создания клавиатуры
def tasks_actions_kb() -> InlineKeyboardMarkup:
    add_quest = InlineKeyboardButton(
        text='[+] Добавить задание [+]',
        callback_data='add_quets',
    )
    del_quest = InlineKeyboardButton(
        text='[-] Удалить задание [-]',
        callback_data='del_quets',
    )
    rows = [
        [add_quest],
        [del_quest],
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    return markup
