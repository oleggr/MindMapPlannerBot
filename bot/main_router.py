from contextlib import suppress
import logging

from aiogram import Router, F
from aiogram.utils.markdown import hbold
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from bot.callback_data import StateCallbackFactory
from bot.keyboard_builder import Builder
from bot.message_builder import MessageBuilder
from db.controller import DbController


logger = logging.getLogger(__name__)

main_router = Router()
storage = DbController()

DEFAULT_STATE = 0


@main_router.callback_query(StateCallbackFactory.filter(F.action == "settings"))
async def show_bot_settings(
        callback: CallbackQuery,
):
    logger.debug(
        f'Call action SETTING for user {callback.from_user.id}'
    )

    builder = Builder.get_settings_keyboard(
        callback.from_user.id,
    )

    with suppress(TelegramBadRequest):
        await callback.message.edit_text(
            f'{hbold("Settings")} will appear here {hbold("soon")}',
            reply_markup=builder.as_markup(),
        )

    await callback.answer()


@main_router.callback_query(StateCallbackFactory.filter(F.action == "back"))
async def backward_to_parent_leaf(
        callback: CallbackQuery,
        callback_data: StateCallbackFactory
):
    logger.debug(
        f'Call action BACK for user {callback.from_user.id}, '
        f'state {callback_data.state}, parent_state {callback_data.parent_state}'
    )
    message = 'default'

    if callback_data.parent_state == DEFAULT_STATE:
        message = MessageBuilder.get_start_message()

    leaf = storage.get_leaf_by_id(callback_data.parent_state)
    if leaf:
        message = leaf.name

    builder = Builder.get_keyboard(
        storage=storage,
        user_id=callback.from_user.id,
        state=callback_data.parent_state,
        parent_state=leaf.parent_id if leaf else DEFAULT_STATE
    )

    await callback.message.edit_text(
        message,
        reply_markup=builder.as_markup(),
    )

    await callback.answer()


@main_router.callback_query(StateCallbackFactory.filter(F.action == "view"))
async def view_leaf(
        callback: CallbackQuery,
        callback_data: StateCallbackFactory
):
    logger.debug(
        f'Call action VIEW for user {callback.from_user.id}, '
        f'state {callback_data.state}, parent_state {callback_data.parent_state}'
    )
    builder = Builder.get_keyboard(
        storage=storage,
        user_id=callback.from_user.id,
        state=callback_data.state,
        parent_state=callback_data.parent_state,
    )

    await callback.message.edit_text(
        callback_data.name,
        reply_markup=builder.as_markup(),
    )

    await callback.answer()
