from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_default_stud_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.row(KeyboardButton("Посмотреть расписание"), KeyboardButton("Сменить группу"))
    kb.row(KeyboardButton("Режим преподавателя"))
    return kb


def get_default_teacher_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.row(KeyboardButton("Посмотреть расписание"), KeyboardButton("Сменить преподавателя"))
    kb.row(KeyboardButton("Добавить занятие"), KeyboardButton("Перенести занятие"))
    kb.row(KeyboardButton("Режим студента"))
    return kb


def get_teacher_next_prev_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.row(InlineKeyboardButton("<", callback_data='prev_teacher'),
           InlineKeyboardButton(">", callback_data='next_teacher'))
    return kb


def get_stud_next_prev_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.row(InlineKeyboardButton("<", callback_data='prev_stud'),
           InlineKeyboardButton(">", callback_data='next_stud'))
    return kb


def get_kb_from_list(_list):
    kb = ReplyKeyboardMarkup(row_width=4,resize_keyboard=True)
    for val in _list:
        kb.insert(KeyboardButton(val))
    return kb
