import datetime

from aiogram.bot import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ContentTypes, ReplyKeyboardRemove
from aiogram.utils import executor

from config import TOKEN, DB_URL
from database_tools.database_model import DBConnection
from database_tools.entities import Building
from keyboards import *
from tools import *

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
db = DBConnection(DB_URL)


class States(StatesGroup):
    stud_default_state = State()
    stud_choosing_group_state = State()
    teacher_default_state = State()
    teacher_choosing_state = State()
    teacher_choosing_group_state = State()
    teacher_choosing_eq_state = State()
    teacher_choosing_date_state = State()
    teacher_choosing_time_state = State()


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message, state: FSMContext):
    await message.answer("Привет! Здесь ты можешь просматривать и редактировать расписание!",
                         reply_markup=get_default_stud_kb())
    await state.set_state(States.stud_default_state)


@dp.message_handler(state=States.stud_default_state, content_types=ContentTypes.TEXT)
async def def_stud_handler(message: types.Message, state: FSMContext):
    if message.text == "Посмотреть расписание":
        data = await state.get_data()
        if "group" in data.keys():
            curday_schedule = await db.get_stud_schedule_by_date(data["group"])
            await message.answer(await stringify_schedule_list(curday_schedule), parse_mode="MarkdownV2",
                                 reply_markup=get_stud_next_prev_keyboard())
        else:
            await message.answer("У тебя не выбрана группа!")

    elif message.text == "Сменить группу":
        await message.answer("Список доступных групп:")
        groups = await db.get_groups()
        await message.answer(groups, reply_markup=get_kb_from_list(groups))
        await state.set_state(States.stud_choosing_group_state)
    elif message.text == "Режим преподавателя":
        await message.answer("Вы перешли в режим преподавателя.", reply_markup=get_default_teacher_kb())
        await state.set_state(States.teacher_default_state)
    else:
        await message.answer("Не понял тебя.")


@dp.message_handler(state=States.stud_choosing_group_state, content_types=ContentTypes.TEXT)
async def handle_choose_group(message: types.Message, state: FSMContext):
    if await db.group_exists(message.text):
        await state.update_data(group=message.text)
        await message.answer("Группа установлена: " + message.text, reply_markup=get_default_stud_kb())
        await state.set_state(States.stud_default_state)
    else:
        await message.answer("Такой группы не существует.")


@dp.message_handler(state=States.teacher_default_state, content_types=ContentTypes.TEXT)
async def def_teacher_handler(message: types.Message, state: FSMContext):
    if message.text == "Посмотреть расписание":
        data = await state.get_data()
        if "teacher" in data.keys():
            curday_schedule = await db.get_teacher_schedule_by_date(data["teacher"].split()[0])
            await message.answer(await stringify_schedule_list(curday_schedule), parse_mode="MarkdownV2",
                                 reply_markup=get_teacher_next_prev_keyboard())
        else:
            await message.answer("У тебя не выбран преподаватель")
    elif message.text == "Сменить преподавателя":
        await message.answer("Список доступных преподавателей:")
        await message.answer(await db.get_teachers(), reply_markup=ReplyKeyboardRemove())
        await state.set_state(States.teacher_choosing_state)
    elif message.text == "Добавить занятие":
        data = await state.get_data()
        if "teacher" in data.keys():
            await message.answer("Выберите группу:")
            groups = await db.get_groups()
            await message.answer(groups, reply_markup=get_kb_from_list(groups))
            await state.set_state(States.teacher_choosing_group_state)
        else:
            await message.answer("У тебя не выбран преподаватель")
    elif message.text == "Перенести занятие":
        pass
    elif message.text == "Режим студента":
        await state.set_state(States.stud_default_state)
        await message.answer("Вы перешли в режим студента.", reply_markup=get_default_stud_kb())
    else:
        await message.answer("Не понял тебя.")


@dp.message_handler(state=States.teacher_choosing_state, content_types=ContentTypes.TEXT)
async def handle_choose_teacher(message: types.Message, state: FSMContext):
    if await db.teacher_exists(message.text):
        await state.update_data(teacher=message.text)
        await message.answer("Преподаватель установлен: " + message.text, reply_markup=get_default_teacher_kb())
        await state.set_state(States.teacher_default_state)
    else:
        await message.answer("Такого преподавателя не существует.")


@dp.message_handler(state=States.teacher_choosing_group_state, content_types=ContentTypes.TEXT)
async def handle_choose_teacher(message: types.Message, state: FSMContext):
    if await db.group_exists(message.text):
        await state.update_data(teacher_group=message.text)
        await message.answer("Какое оборудование необходимо?:")
        eq = await db.get_eq()
        await message.answer(eq, reply_markup=get_kb_from_list(eq))
        await state.set_state(States.teacher_choosing_eq_state)
    else:
        await message.answer("Такой группы не существует.")


@dp.message_handler(state=States.teacher_choosing_eq_state, content_types=ContentTypes.TEXT)
async def handle_choose_teacher(message: types.Message, state: FSMContext):
    if await db.eq_exists(message.text):
        await state.update_data(teacher_eq=message.text)
        await message.answer("Напишите дату занятия в формате YYYY-MM-DD:", reply_markup=ReplyKeyboardRemove())
        await state.set_state(States.teacher_choosing_date_state)
    else:
        await message.answer("Такого оборудования не существует.")


@dp.message_handler(state=States.teacher_choosing_date_state, content_types=ContentTypes.TEXT)
async def handle_choose_teacher(message: types.Message, state: FSMContext):
    try:
        date = datetime.datetime.fromisoformat(message.text)
        await state.update_data(date=date)
        data = await state.get_data()
        raw_list = await db.get_free_classrooms(data["teacher_group"], data["teacher_eq"], date)
        if len(raw_list) != 0:
            await message.answer(await stringify_raw_list(raw_list), parse_mode="MarkdownV2",
                                 reply_markup=get_default_teacher_kb())
            await state.set_state(States.teacher_choosing_time_state)
            await state.update_data(raw_list=raw_list)
        else:
            await message.answer("Нет доступных вариантов на этот день.")
            await state.set_state(States.teacher_default_state)

    except ValueError:
        await message.answer("Введите дату в формате YYYY-MM-DD.")


@dp.message_handler(state=States.teacher_choosing_time_state, content_types=ContentTypes.TEXT)
async def handle_choose_teacher(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text.isdigit() and 0 <= int(message.text) < len(data["raw_list"]):
        await db.add_lesson(data["teacher"],
                            data["date"],
                            data["raw_list"][int(message.text)],
                            data["teacher_group"])
        await message.answer("Успешно добавлено.")
        await state.set_state(States.teacher_default_state)
    else:
        await message.answer("Некорректный ввод.")


@dp.callback_query_handler(lambda c: c.data in ["prev_stud", "next_stud"], state="*")
async def stud_prev_next_handler(callback_query: types.CallbackQuery, state: FSMContext):
    date = await get_datetime_from_callback(callback_query)

    data = await state.get_data()
    res = await db.get_stud_schedule_by_date(data["group"], date)

    await callback_query.message.edit_text(await stringify_schedule_list(res, date), parse_mode="MarkdownV2",
                                           reply_markup=get_stud_next_prev_keyboard())


@dp.callback_query_handler(lambda c: c.data in ["prev_teacher", "next_teacher"], state="*")
async def teacher_prev_next_handler(callback_query: types.CallbackQuery, state: FSMContext):
    date = await get_datetime_from_callback(callback_query)
    data = await state.get_data()
    res = await db.get_teacher_schedule_by_date(data["teacher"].split()[0], date)

    await callback_query.message.edit_text(await stringify_schedule_list(res, date), parse_mode="MarkdownV2",
                                           reply_markup=get_teacher_next_prev_keyboard())


if __name__ == '__main__':
    executor.start_polling(dp)
