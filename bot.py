import asyncio
import logging
from random import randint

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQuery, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.utils.markdown import hbold

import config


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


dp = Dispatcher()


@dp.message(CommandStart())
async def handle(message):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='test1', callback_data='test1'),
        InlineKeyboardButton(text="test2", callback_data="test2")
    )
    builder.row(
        InlineKeyboardButton(text='test3', url='https://www.google.com')
    )
    await message.answer(
        f"Hello, {hbold(message.from_user.full_name)}!",
        reply_markup=builder.as_markup(),
        # reply_markup=keyboard,
    )


@dp.callback_query(F.data == "random_value")
async def send_random_value(callback: CallbackQuery):
    await callback.message.answer(str(randint(1, 10)))


@dp.callback_query(F.data == "test2")
async def fail_agent(call: CallbackQuery):
    print(call)
    await call.message.answer(f'Привет {str(randint(1, 10))}')
    await call.answer('Ку')


async def main() -> None:
    bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)

try:
    logger.info("Polling started")

    asyncio.run(main())

    logger.info("Polling stopped manually")
except Exception as e:
    logger.error('Error while polling: {}'.format(e))
