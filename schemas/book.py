# Python
from typing import Optional
from enum import Enum
from datetime import date

# Pydantic
from pydantic import BaseModel
from pydantic import Field


# Models
class ReadingAge(Enum):
    yearsDefault = "No defined"
    years1_3 = "1 - 3 years"
    years4_7 = "4 - 7 years"
    years8_10 = "8 - 10 years"
    years11_14 = "11 - 14 years"
    years15_17 = "15 - 17 years"
    years18 = "older than 18"

    def __str__(self):
        return str(self.value)


class Language(Enum):
    default = "No defined"
    english = "english"
    spanish = "spanish"
    french = "french "
    german = "german "

    def __str__(self):
        return str(self.value)


# Models Book
class BookBase(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        example="A Monster Calls"
    )
    reading_age: Optional[ReadingAge] = Field(
        default=ReadingAge.yearsDefault,
        example=ReadingAge.years18
    )
    pages: int = Field(
        ...,
        ge=1,
        le=10000,
        example=128
    )
    language: Optional[Language] = Field(
        default=Language.default,
        example=Language.english
    )
    publisher: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50,
        example="Candlewick"
    )
    date_add: Optional[date] = Field(default=date.today())
    date_update: Optional[date] = Field(default=date.today())


class BookUpdate(BookBase):
    title: Optional[str] = Field(
        min_length=1,
        max_length=100
    )
    pages: Optional[int] = Field(
        ge=1,
        le=10000,
        example=128
    )
    language: Optional[Language] = Field(
        default=None
    )
    reading_age: Optional[ReadingAge] = Field(
        default=None
    )
    id_book: int = Field(
        ...,
        gt=0
    )
