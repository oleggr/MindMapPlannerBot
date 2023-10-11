from datetime import datetime
from pydantic import BaseModel, field_validator
from typing import Optional


class MapLeaf(BaseModel):
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

