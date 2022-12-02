from aiogram.bot import Bot
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN, DB_URL, DB_HELIOS_URL
from database_tools.database_model import DBConnection
from database_tools.entities import Building

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
con = DBConnection(DB_HELIOS_URL)


@dp.message_handler(commands=['get_building'])
async def process_start_command(message: types.Message):
    building: Building = con.database.get(Building, message.get_args()[0])
    await message.answer(building.address)

if __name__ == '__main__':
    executor.start_polling(dp)



