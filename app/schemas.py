from pydantic import BaseModel,Field
from typing import Optional
from uuid import UUID
from datetime import datetime

class UserBase(BaseModel):
    phone_number: str= Field(...,min_length=10,max_length=15)
    first_name: str=Field(...,min_length=1,max_length=32)
    last_name: Optional[str] = Field(None, max_length=32)
    about: Optional[str] = Field("Hey there! I am a User.", max_length=128)

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    user_id: UUID
    is_active: bool
    created_at: datetime
    class Config:
        from_attributes = True