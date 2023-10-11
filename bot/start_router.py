import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from db.controller import DbController
from db.models import User

logger = logging.getLogger(__name__)

start_router = Router()
storage = DbController()


@start_router.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    user = storage.get_user(message.from_user.id)
    if not user:
        storage.write_user(
            User(
                user_id=message.from_user.id,
                username=message.from_user.username,
            )
        )

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='test1', callback_data='test1'),
        InlineKeyboardButton(text="test2", callback_data="test2")
    )
    builder.row(
        InlineKeyboardButton(text='test3', url='https://www.google.com')
    )
    await message.answer(
        f"Hello, {message.from_user.full_name}!",
        reply_markup=builder.as_markup(),
    )
