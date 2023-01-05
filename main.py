# Python
from typing import Optional, Dict, List
from enum import Enum
from uuid import UUID
from datetime import date, datetime


# Pydantic
from pydantic import BaseModel
from pydantic import SecretStr
from pydantic import EmailStr
from pydantic import Field


# FastAPI
from fastapi import FastAPI, status
from fastapi import Body, Path
from fastapi import HTTPException

app = FastAPI()


# Modes
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
    '''
    Class base of books
    '''
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
    date_add: datetime = Field(default=datetime.now())
    date_update: Optional[datetime] = Field(default=None)


class Book(BookBase):
    isbn_10: str = Field(
        ...,
        min_length=10,
        max_length=12,
        example="0763692158"
    )
    id_book: UUID = Field(...)


class BookOut(BookBase):
    '''
    Books as response
    '''
    pass


class AuthorBase(BaseModel):
    full_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Patrick Ness"
    )
    birthdate: Optional[date] = Field(
        default=None,
        example='1998-06-23'
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
    id_author: UUID = Field(...)


class AuthorOut(AuthorBase):
    pass


class LoginBase(BaseModel):
    username: str = Field(
        ...,
        max_length=20,
        example="lita2021"
        )
    email: EmailStr = Field(
        ...
        )
    message: str = Field(
       default="Login Succesfully!"
        )


class Login(LoginBase):
    password: SecretStr = Field(
        ...,
        min_length=8,
        max_length=64
    )


class LoginOut(LoginBase):
    pass


# root
@app.get(
    path="/",
    status_code=status.HTTP_200_OK,
    tags=["Root"]
    )
def home() -> Dict:
    return {"Hello": "World"}


# Books
# Create a book
@app.post(
    path="/book/new",
    response_model=BookOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Book"],
    summary="Create a new book and return it"
    )
def create_book(book: Book = Body(...)):
    """
    "Create a new book"

    - Args:
      book (Book): Book = Body(...)

    - Returns:
      The book object that was passed in.
    """
    return book


books_id = [1, 2, 3, 4, 5, 6, 7, 8, 9]  # books ID


# Show a book
@app.get(
    path="/book/{id_book}",
    status_code=status.HTTP_200_OK,
    response_model=BookOut,
    tags=["Book"],
    summary="Show a book"
    )
def show_book_path(
    id_book: int = Path(
        ...,
        title="Code book",
        gt=0,
        example=7
        )
):
    """
    "Check a book in library"
    It returns a dictionary with the id_book as the
    key and a string as the value. The id_book is an
    integer that is greater than 0 and the example value is 112233.
    If the id_book is not in the id_book list, then it raises
    an HTTPException with a status code of 404 and a detail message.

    - Args:
      id_book (int): int = Path(

    - Returns:
      A dictionary with the id_book as the key and a string as the value.
    """
    if id_book not in books_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="¡This book is not in our library"
            )
    return {id_book: "It exists!"}


# Show all books
@app.get(
    path="/books",
    response_model=List[BookOut],
    status_code=status.HTTP_200_OK,
    summary="Show all books",
    tags=["Book"]
)
def show_all_books():
    pass


# Delete a book
@app.delete(
    path="/book/{id_book}/delete",
    response_model=BookOut,
    status_code=status.HTTP_200_OK,
    summary="Delete a book",
    tags=["Book"]
)
def delete_a_book():
    pass


# Update a book
@app.put(
    path="/book/update_book/{id_book}/{isbn_10}",
    status_code=status.HTTP_200_OK,
    tags=["Book"],
    summary="Updates a book"
    )
def update_book(
    id_book: int = Path(
        ...,
        title="Code book",
        gt=0,
        example=7
    ),
    isbn_10: str = Path(
        ...,
        title="book ID (ISBN-10)",
        description="Code ISBN-10",
        min_length=10,
        max_length=12,
        example="0111112229"
    ),
    book: Book = Body(...)
):
    """
    "Updates a book and returns it"

    - Args:
        code_book (int): The ID of the book to be updated.
        book (Book): A `Book` object with the updated information.

    - Returns:
        dict: A dictionary with the updated book information.
    """
    results = book.dict()
    results.update({'isbn_10': isbn_10})
    return results


# Author
# Create an author
@app.post(
    path="/author/new",
    response_model=AuthorOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Author"],
    summary="Create a new author"
    )
def create_author(author: Author = Body(...)):
    """
    "Create a new author"

    - Args:
      author (Author): Author = Body(...)

    - Returns:
      The author object
    """
    return author


# Show an author
@app.get(
    path="/author/{id_author}",
    response_model=AuthorOut,
    status_code=status.HTTP_200_OK,
    summary="Show an author",
    tags=["Author"]
)
def show_an_author():
    pass


# Show all authors
@app.get(
    path="/authors",
    response_model=List[AuthorOut],
    status_code=status.HTTP_200_OK,
    summary="Show all authors",
    tags=["Author"]
)
def show_all_authors():
    pass


# Delete an author
@app.delete(
    path="/author/{id_author}/delete",
    response_model=AuthorOut,
    status_code=status.HTTP_200_OK,
    summary="Delete an author",
    tags=["Author"]
)
def delete_an_author():
    pass


# Update an author
@app.put(
    path="/author/{id_author}/update",
    response_model=AuthorOut,
    status_code=status.HTTP_200_OK,
    summary="Update an author",
    tags=["Author"]
)
def update_an_author():
    pass


# Login
# Register a user
@app.post(
    path="/signup",
    response_model=LoginOut,
    status_code=status.HTTP_201_CREATED,
    summary="Register a User",
    tags=["Login"]
)
def signup():
    pass


# Login a user
@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    summary="Login a User",
    tags=["Login"]
)
def login():
    pass
