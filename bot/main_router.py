from contextlib import suppress
import logging

from aiogram import Router, F
from aiogram.utils.markdown import hbold
from aiogram.types import CallbackQuery, Message
from aiogram.exceptions import TelegramBadRequest

from bot.callback_data import StateCallbackFactory
from bot.keyboard_builder import Builder
from bot.message_builder import START_MESSAGE, WRITE_NAME, EDIT_TOPIC
from db.controller import DbController
from db.models import UserState, UserAction, UserMessage, Leaf


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
        message = START_MESSAGE

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


@main_router.callback_query(StateCallbackFactory.filter(F.action == "add"))
async def view_leaf(
        callback: CallbackQuery,
        callback_data: StateCallbackFactory
):
    logger.debug(
        f'Call action ADD for user {callback.from_user.id}, '
        f'state {callback_data.state}, parent_state {callback_data.parent_state}'
    )

    storage.upsert_user_state(
        UserState(
            user_id=callback.from_user.id,
            state=callback_data.state,
            action=UserAction.add_name.value,
        )
    )

    await callback.message.edit_text(WRITE_NAME)
    await callback.answer()


@main_router.callback_query(StateCallbackFactory.filter(F.action == "edit"))
async def view_leaf(
        callback: CallbackQuery,
        callback_data: StateCallbackFactory
):
    logger.debug(
        f'Call action EDIT for user {callback.from_user.id}, '
        f'state {callback_data.state}, parent_state {callback_data.parent_state}'
    )

    storage.upsert_user_state(
        UserState(
            user_id=callback.from_user.id,
            state=callback_data.state,
            action=UserAction.edit_name.value,
        )
    )

    await callback.message.answer(
        EDIT_TOPIC,
        reply_markup=Builder.get_edit_menu(),
    )
    await callback.answer()


@main_router.message()
async def handle_message(message: Message) -> None:
    user_id = message.from_user.id
    user_state = storage.get_user_state(user_id)

    _message = 'default'
    _parent_state = DEFAULT_STATE

    if user_state.state == DEFAULT_STATE:
        _message = START_MESSAGE

    if user_state.action == UserAction.add_name.value:
        storage.write_leaf(
            Leaf(
                leaf_id=0,  # not required here
                user_id=user_id,
                name=message.text,
                parent_id=user_state.state,
                target_value='',
                current_value='',
            )
        )

        storage.upsert_user_state(
            UserState(
                user_id=user_id,
                state=user_state.state,
                action=UserAction.view.value,
            )
        )

        builder = Builder.get_keyboard(
            storage=storage,
            user_id=user_id,
            state=user_state.state,
            parent_state=_parent_state,
        )

        leaf = storage.get_leaf_by_id(user_state.state)
        if leaf:
            _message = leaf.name
            _parent_state = leaf.parent_id

        await message.answer(
            _message,
            reply_markup=builder.as_markup(),
        )

    elif user_state.action == UserAction.edit_name.value:
        if message.text != 'Skip' \
                and message.text != 'Delete' \
                and user_state.state != DEFAULT_STATE:
            storage.update_leaf(user_state.state, message.text)

        storage.upsert_user_state(
            UserState(
                user_id=user_id,
                state=user_state.state,
                action=UserAction.view.value,
            )
        )

        leaf = storage.get_leaf_by_id(user_state.state)
        if leaf:
            _message = leaf.name
            _parent_state = leaf.parent_id

        _state = user_state.state

        if message.text == 'Delete':
            storage.delete_leaf(user_state.state)
            _state = DEFAULT_STATE

            if _parent_state == DEFAULT_STATE:
                _message = START_MESSAGE
                _parent_state = DEFAULT_STATE

            parent_leaf = storage.get_leaf_by_id(_parent_state)
            if parent_leaf:
                _message = parent_leaf.name
                _state = parent_leaf.leaf_id
                _parent_state = parent_leaf.parent_id

        builder = Builder.get_keyboard(
            storage=storage,
            user_id=user_id,
            state=_state,
            parent_state=_parent_state,
        )

        await message.answer(
            _message,
            reply_markup=builder.as_markup(),
        )

    else:
        storage.write_message(
            UserMessage(
                user_id=user_id,
                message=message.text,
            )
        )
