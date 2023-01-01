# Python
from typing import Optional, Dict
from enum import Enum

# Pydantic
from pydantic import BaseModel, Field

# FastAPI
from fastapi import FastAPI, status
from fastapi import Body, Query, Path

app = FastAPI()


# Model
class ReadingAge(Enum):
    yearsDefault = "No defined"
    years1_3 = "1 - 3 years"
    years4_7 = "4 - 7 years"
    years8_10 = "8 - 10 years"
    years11_14 = "11 - 14 years"
    years15_17 = "15 - 17 years"
    years18 = "older than 18"


class Language(Enum):
    default = "No defined"
    english = "english"
    spanish = "spanish"
    french = "french "
    german = "german "


class BookBase(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        example="A Monster Calls"
    )
    author: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Patrick Ness"
    )
    reading_age: Optional[ReadingAge] = Field(
        default=ReadingAge.yearsDefault,
        example=ReadingAge.years18
    )
    pages: Optional[int] = Field(
        default=None,
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


class Book(BookBase):
    isbn_10: str = Field(
        ...,
        min_length=10,
        max_length=12,
        example="0763692158"
    )
    id_hide: str = Field(
        ...,
        min_length=8,
        example='3N1gM4H1D3'
    )


class BookOut(BookBase):
    pass


class AuthorBase(BaseModel):
    author: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Patrick Ness"
    )
    birthdate: Optional[str] = Field(
        default=None,
        example="27/08/1991",
        min_length=10,
        max_length=10
    )
    nationality: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=120,
        example='American-British'
    )
    genre: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=120,
        example='Young adult'
    )


class Author(AuthorBase):
    id_hide: str = Field(
        ...,
        min_length=8,
        example='Hid3N1T3M5'
    )


class AuthorOut(AuthorBase):
    pass


@app.get(
    path="/",
    status_code=status.HTTP_200_OK
    )
def home() -> Dict:
    return {"Hello": "World"}


# Request and Response Body
@app.post(
    path="/book/new",
    response_model=BookOut,
    status_code=status.HTTP_201_CREATED
    )
def create_book(book: Book = Body(...)):
    return book


@app.post(
    path="/author/new",
    response_model=AuthorOut,
    status_code=status.HTTP_201_CREATED
    )
def create_author(author: Author = Body(...)):
    return author


# Validaciones: Query Parameters
@app.get(
    path="/book/details",
    status_code=status.HTTP_200_OK
    )
def show_book(
    title: Optional[str] = Query(
        None,
        min_length=1,
        max_length=100,
        title="book title",
        description="The name of the book",
        example="A Monster Calls"
        ),
    author: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title="author book",
        description="The author of the book",
        example="Patrick Ness"
        )
):
    return {title: author}


# Validaciones: Path Parameters

@app.get(
    path="/book/{book_id}",
    status_code=status.HTTP_200_OK
    )
def show_book_path(
    book_id: int = Path(
        ...,
        gt=0,
        example=112233
        )
):
    return {book_id: "It exists!"}


@app.put(
    path="/book/{book_id}",
    status_code=status.HTTP_200_OK
    )
def update_book(
    book_id: int = Path(
        ...,
        title="book ID",
        description="This is the book ID",
        gt=0,
        example=224455
    ),
    book: Book = Body(...)
):
    results = book.dict()
    return results
