from pydantic import BaseModel,Field,EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime

class UserBase(BaseModel):
    phone_number: str= Field(...,min_length=10,max_length=15)
    email: str= Field(...,max_length=128)
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

#Transfered Abhay's auth.py from app/schermas to father schemas at one place
class SignupRequest(BaseModel):
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    email: EmailStr
    phone_number: str = Field(..., min_length=10, max_length=15)


class SignupResponse(BaseModel):
    message: str
##

class ConversationResponse(BaseModel):
    id: UUID
    user1_id: UUID
    user2_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

class MessageCreate(BaseModel):
    receiver_id: UUID
    content: str=Field(...,max_length=1024)

class MessageResponse(BaseModel):
    id: UUID
    conversation_id: UUID
    sender_id: UUID
    content: str
    created_at: datetime

    class Config:
        from_attributes = True