import logging

from aiogram import Router, F
from aiogram.utils.markdown import hbold
from aiogram.types import CallbackQuery

from bot.callback_data import StateCallbackFactory
from bot.keyboard_builder import Builder
from db.controller import DbController


logger = logging.getLogger(__name__)

main_router = Router()
storage = DbController()


@main_router.callback_query(StateCallbackFactory.filter(F.action == "settings"))
async def show_bot_settings(
        callback: CallbackQuery,
):
    builder = Builder.get_settings_keyboard(
        callback.from_user.id,
    )

    await callback.message.edit_text(
        f'Скоро тут будут {hbold("настройки")}',
        reply_markup=builder.as_markup(),
    )

    await callback.answer()


@main_router.callback_query(StateCallbackFactory.filter(F.action == "back"))
async def backward_to_parent_leaf(
        callback: CallbackQuery,
        callback_data: StateCallbackFactory
):
    builder = Builder.get_keyboard(
        storage,
        callback.from_user.id,
        callback_data.parent_state,
    )

    await callback.message.edit_text(
        'Test',
        reply_markup=builder.as_markup(),
    )

    await callback.answer()
