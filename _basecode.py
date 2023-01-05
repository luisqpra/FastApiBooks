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
from fastapi import (
    Body, Query, Path, Form, Header, Cookie
    )
from fastapi import UploadFile, File
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


class LoginOut(BaseModel):
    username: str = Field(
        ...,
        max_length=20,
        example="lita2021"
        )
    message: str = Field(
        default="Login Succesfully!"
        )


# root
@app.get(
    path="/",
    status_code=status.HTTP_200_OK,
    tags=["Root"]
    )
def home() -> Dict:
    return {"Hello": "World"}


# Request and Response Body
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


# Validations: Query Parameters
@app.get(
    path="/book/details",
    status_code=status.HTTP_200_OK,
    tags=["Book"],
    summary="Show details about a book"
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
    """
    It returns a dictionary with the title as the key
    and the author as the value

    - Args:
      title (Optional[str]): Optional[str] = Query(
      author (Optional[str]): Optional[str] = Query(

    - Returns:
      A dictionary with the title and author as keys and values.
    """
    return {title: author}


# Validations: Path Parameters
books_id = [1, 2, 3, 4, 5, 6, 7, 8, 9]  # books ID


@app.get(
    path="/book/{code_book}",
    status_code=status.HTTP_200_OK,
    tags=["Book"],
    summary="Checking if a book was created"
    )
def show_book_path(
    code_book: int = Path(
        ...,
        title="Code book",
        gt=0,
        example=7
        )
):
    """
    "Check a book in library"
    It returns a dictionary with the code_book as the
    key and a string as the value. The code_book is an
    integer that is greater than 0 and the example value is 112233.
    If the code_book is not in the code_book list, then it raises
    an HTTPException with a status code of 404 and a detail message.

    - Args:
      code_book (int): int = Path(

    - Returns:
      A dictionary with the code_book as the key and a string as the value.
    """
    if code_book not in books_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="¡This book is not in our library"
            )
    return {code_book: "It exists!"}


@app.put(
    path="/book/update_book/{code_book}/{isbn_10}",
    status_code=status.HTTP_200_OK,
    tags=["Book"],
    summary="Updates a book"
    )
def update_book(
    code_book: int = Path(
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


# Login -forms
@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    tags=["User"],
    summary="Loging a user"
)
def login(
    username: str = Form(
        ...,
        example="luisquiroz"
        ),
    password: SecretStr = Form(
        ...,
        min_length=8,
        max_length=64,
        example="HolaMundo"
        )):
    """
    "Logs in a user and returns a success message"

    - Args:
        username (str): The username of the user.
        password (SecretStr): The password of the user.

    - Returns:
        LoginOut: A `LoginOut` object with the following attributes:
            username (str): The username of the user.
            message (str): A message indicating that the login was successful.
    """
    return LoginOut(username=username)


# Cookies and headers parameters
@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK,
    tags=["User"],
    summary="Form about a contact"
)
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1,
        example="Luis"
    ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1,
        example="Quiroz Prada"
    ),
    email: EmailStr = Form(
        ...,
        example="luis@yahoo.com"
        ),
    message: str = Form(
        ...,
        min_length=20,
        example="Heyyy you, how are you?, what's going on"
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(
        default=None,
        example="this is the info that is tracking"
        )
):
    """
    "Receive and returns information about a form"

    - Args:
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (EmailStr): The email of the user.
        message (str): The message to be sent.
        user_agent (Optional[str]): The user agent of the request.
        ads (Optional[str]): The ads tracking information of the request.

    - Returns:
        dict: A dictionary with the following keys:
            "header" (str): The user agent of the request.
            "cookie" (str): The ads tracking information of the request.
    """
    result = {
        "header": user_agent,
        "cookie": ads
    }
    return result
    # return user_agent


# Files

@app.post(
    path="/post-image",
    tags=["File"],
    summary="Loads a image",
    deprecated=True
)
def post_image(
    image: UploadFile = File(...)
):
    """
    "Uploads an image and returns information about it"

    - Args:
        image (UploadFile): The image file to be uploaded.

    - Returns:
        dict: A dictionary with the following keys:
            "Filename" (str): The name of the image file.
            "Format" (str): The content type of the image file.
            "Size(kb)" (float): The size of the image file in kilobytes.
    """
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024, ndigits=2)
    }


@app.post(
    path='/post-multimages',
    tags=["File"],
    summary="Load several files"
)
def post_multimages(
    images: List[UploadFile] = File(...)
):
    """
    "Uploads several images and returns information about them"

    It takes a list of images, and returns a list of
    dictionaries containing the filename, format, and
    size of each image

    - Args:
      images (List[UploadFile]): List[UploadFile] = File(...)

    - Returns:
      A list of dictionaries.
    """
    info_images = [{
        "filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024, ndigits=2)
    } for image in images]

    return info_images
