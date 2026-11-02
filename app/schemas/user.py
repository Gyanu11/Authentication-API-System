from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field 

class UserCreate(BaseModel):
    email: EmailStr

    full_name: str = Field(
        min_length=2,
        max_length=100,
    )

    password: str = Field(
        min_length=8,
        max_length=128,
    )

class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    is_verified: bool
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)