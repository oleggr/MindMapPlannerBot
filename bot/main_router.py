import logging
from random import randint

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, CallbackQuery

from db.controller import DbController


logger = logging.getLogger(__name__)

main_router = Router()
storage = DbController()


@main_router.callback_query(F.data == "random_value")
async def send_random_value(callback: CallbackQuery):
    await callback.message.answer(str(randint(1, 10)))


@main_router.callback_query(F.data == "test2")
async def fail_agent(call: CallbackQuery):
    await call.message.answer(f'Привет {str(randint(1, 10))}')
    await call.answer('Ку')
