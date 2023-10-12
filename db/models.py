from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from typing import Optional


class Leaf(BaseModel):
    leaf_id: int
    user_id: int
    name: str
    parent_id: Optional[int] = 0

    target_value: Optional[str] = None
    current_value: Optional[str] = None

    deadline: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class User(BaseModel):
    user_id: int
    username: Optional[str] = ''
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class UserAction(Enum):
    view = 1
    edit_name = 2
    add_name = 3


class UserState(BaseModel):
    user_id: int
    state: int
    action: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class UserMessage(BaseModel):
    user_id: int
    message: str
