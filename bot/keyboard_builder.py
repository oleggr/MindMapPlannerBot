import logging

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from bot.callback_data import StateCallbackFactory
from db.controller import DbController


logger = logging.getLogger(__name__)

DEFAULT_STATE = 0


class Builder:
    storage: DbController = None

    @staticmethod
    def get_keyboard(
            storage: DbController,
            user_id: int,
            state: int = DEFAULT_STATE,
            parent_state: int = DEFAULT_STATE,
    ) -> InlineKeyboardBuilder:
        logger.debug(
            f'Build keyboard user {user_id}, state {state}, parent_state {parent_state}'
        )

        leaves = storage.get_leaves(
            user_id=user_id,
            parent_id=state,
        )

        builder = InlineKeyboardBuilder()

        for leaf in leaves:
            builder.button(
                text=leaf.name,
                callback_data=StateCallbackFactory(
                    action='view',
                    state=leaf.leaf_id,
                    name=leaf.name,
                    parent_state=state,
                ),
            )

        builder.button(
            text='Edit',
            callback_data=StateCallbackFactory(action='edit', state=state),
        )

        builder.button(
            text='Add',
            callback_data=StateCallbackFactory(action='add', state=state),
        )

        if state == DEFAULT_STATE:
            builder.button(
                text='Settings',
                callback_data=StateCallbackFactory(action='settings', state=state),
            )
        else:
            _parent_state = parent_state

            builder.button(
                text='<<<',
                callback_data=StateCallbackFactory(
                    action='back',
                    state=state,
                    parent_state=_parent_state
                ),
            )

        return builder

    @staticmethod
    def get_settings_keyboard(
            user_id: int,
            state: int = DEFAULT_STATE,
            parent_state: int = DEFAULT_STATE,
    ):
        logger.debug(
            f'Build settings keyboard for user {user_id}'
        )

        builder = InlineKeyboardBuilder()

        builder.button(
            text='Do nothing',
            callback_data=StateCallbackFactory(action='settings', state=state),
        )

        builder.button(
            text='<<<',
            callback_data=StateCallbackFactory(
                action='back',
                state=state,
                parent_state=parent_state
            ),
        )

        return builder

    @staticmethod
    def get_skip_button():
        kb = [
            [
                KeyboardButton(text="Skip"),
            ],
        ]
        keyboard = ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
        )

        return keyboard
