from typing import Optional

from aiogram.filters.callback_data import CallbackData


class StateCallbackFactory(CallbackData, prefix="cmd"):
    action: str
    state: int = 0
    parent_state: Optional[int] = 0
