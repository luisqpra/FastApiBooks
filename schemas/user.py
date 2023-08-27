# Python
from typing import Optional
from datetime import date

# Pydantic
from pydantic import BaseModel
from pydantic import SecretStr
from pydantic import EmailStr
from pydantic import Field


# Modes User
class UserBase(BaseModel):
    firts_name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50
    )
    last_name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50
    )
    email: EmailStr = Field(
        ...
    )
    birth_date: Optional[date] = Field(
        default=None,
        example='1986-04-22'
    )


class User(UserBase):
    password: SecretStr = Field(
        ...,
        min_length=8,
        max_length=64
    )


class UserUpdate(User):
    email: Optional[EmailStr] = Field(
    )
    password: Optional[SecretStr] = Field(
        min_length=8,
        max_length=64
    )
    id_user: int = Field(
        ...,
        gt=0
    )
