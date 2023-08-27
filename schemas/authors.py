# Python
from typing import Optional
from datetime import date

# Pydantic
from pydantic import BaseModel
from pydantic import Field


# Models Author
class AuthorBase(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=124,
        example="Bastian Lorens Dad"
    )
    nationality:  Optional[str] = Field(
        min_length=1,
        max_length=100,
        example="The UK"
    )
    genre: Optional[str] = Field(
        min_length=1,
        max_length=100,
        example="Fantasy"
    )
    birthdate: Optional[date] = Field(default=None)


class AuthorUpdate(AuthorBase):
    id_author: int = Field(
        ...,
        gt=0
    )
