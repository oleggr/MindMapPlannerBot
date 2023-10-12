import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from db.controller import DbController
from db.models import User

from bot.keyboard_builder import Builder
from bot.message_builder import START_MESSAGE

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

    builder = Builder.get_keyboard(
        storage,
        message.from_user.id,
    )

    await message.answer(
        START_MESSAGE,
        reply_markup=builder.as_markup(),
    )
