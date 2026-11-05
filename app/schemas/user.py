from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr

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

class UserProfileResponse(BaseModel):
    """Public information about the authenticated user."""

    id: int
    email: EmailStr
    full_name: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class UserProfileUpdate(BaseModel):
    """Fields that a user can update."""

    full_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    email: EmailStr | None = None

class PasswordChangeRequest(BaseModel):
    current_password: SecretStr

    new_password: SecretStr = Field(
        min_length=8,
        max_length=128,
    )