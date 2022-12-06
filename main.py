import datetime

from aiogram.bot import Bot
from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ContentTypes
from aiogram.utils import executor

from config import TOKEN, DB_URL, DB_HELIOS_URL
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


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message, state: FSMContext):
    await message.answer("Привет! Здесь ты можешь просматривать и редактировать расписание!",
                         reply_markup=get_default_stud_kb())
    await state.set_state(States.stud_default_state)


@dp.message_handler(state=States.stud_default_state, content_types=ContentTypes.TEXT)
async def def_stud_handler(message: types.Message, state: FSMContext):
    if message.text == "Посмотреть расписание":  # TODO вывод пар по дате, вывод корпуса
        data = await state.get_data()
        if "group" in data.keys():
            weekday = await get_weekday() + 1
            parity = await get_parity() + 1
            curday_schedule = list(filter(lambda x: x.week_day == weekday and x.parity == parity,
                                          await db.get_schedule(data["group"])))
            await message.answer(await stringify_schedule_list(curday_schedule), parse_mode="MarkdownV2",
                                 reply_markup=get_next_prev_keyboard())
        else:
            await message.answer("У тебя не выбрана группа!")

    elif message.text == "Сменить группу":
        await message.answer("Список доступных групп:")
        await message.answer(await db.get_groups())
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
            await message.answer("Я еще не научился расписание выводить :(")  # TODO
        else:
            await message.answer("У тебя не выбран преподаватель")
    elif message.text == "Сменить преподавателя":
        await message.answer("Список доступных преподавателей:")
        await message.answer(await db.get_teachers())
        await state.set_state(States.teacher_choosing_state)
    elif message.text == "Добавить занятие":
        pass
    elif message.text == "Перенести занятие":
        pass
    elif message.text == "Режим cтудента":
        await message.answer("Вы перешли в режим студента.", reply_markup=get_default_stud_kb())
    else:
        await message.answer("Не понял тебя.")


@dp.message_handler(state=States.teacher_choosing_state, content_types=ContentTypes.TEXT)
async def handle_choose_teacher(message: types.Message, state: FSMContext):
    if await db.teacher_exists(message.text):
        await state.update_data(teacher=await db.teacher_id_by_name(message.text))
        await message.answer("Преподаватель установлен: " + message.text, reply_markup=get_default_teacher_kb())
        await state.set_state(States.teacher_default_state)
    else:
        await message.answer("Такого преподавателя не существует.")


@dp.message_handler(state=States.stud_default_state, commands=['get_schedule'])
async def schedule_command(message: types.Message):
    building: Building = db.database.get(Building, message.get_args()[0])
    await message.answer(building.address)


@dp.callback_query_handler(lambda c: c.data in ["prev", "next"], state="*")
async def prev_next_handler(callback_query: types.CallbackQuery, state: FSMContext):
    date, day, month, parity, weekday = await get_datetime_from_callback(callback_query)

    data = await state.get_data()
    res = await db.get_schedule_by_weekday(data["group"], weekday, parity)

    await callback_query.message.edit_text(await stringify_schedule_list(res, date), parse_mode="MarkdownV2",
                                           reply_markup=get_next_prev_keyboard())


if __name__ == '__main__':
    executor.start_polling(dp)
