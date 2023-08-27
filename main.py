# Python
from typing import Optional, Dict, List
from enum import Enum
from datetime import date, datetime

# Base data
from database.funtionsDB import connectionDB

# Pydantic
from pydantic import BaseModel
from pydantic import Field

# FastAPI
from fastapi import FastAPI, status
from fastapi import Body, Query
from fastapi import HTTPException
from fastapi.responses import HTMLResponse

# Middlewares
from middlewares.error_handler import ErrorHandler

# Router
from routes.user import user_router

app = FastAPI()
app.title = "Library"
app.version = " 0.0.1"

app.add_middleware(ErrorHandler)
app.include_router(user_router)


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
    name: str = Field(
        ...,
        min_length=1,
        max_length=124,
        example="Lord Bartholome"
    )
    id_author: int = Field(
        ...,
        gt=0
    )


# Home
@app.get(
    path='/',
    status_code=status.HTTP_200_OK,
    tags=["Home"]
    )
def home() -> Dict:
    return HTMLResponse('<h1> Hello word FastAPI</h1>')
    # return {"Hello": "World"}


# Book
# Create a Book
@app.post(
    path="/book/new",
    status_code=status.HTTP_201_CREATED,
    tags=["Book"],
    response_model=BookBase,
    summary="Create a new book"
    )
def create_book(book: BookBase = Body(...)) -> BookBase:
    """
    It creates a user
    """
    conn = connectionDB()
    sql = ''' INSERT INTO Book(title,reading_age,pages, \
    language,publisher,date_add,date_update)
              VALUES(?,?,?,?,?,?,?) '''
    if book.date_add is not None:
        date_add = book.date_add.strftime("%Y-%m-%d")
    else:
        date_add = datetime.now().strftime("%Y-%m-%d")
    date_update = date_add
    data = (
        book.title,
        book.reading_age.__str__(),
        book.pages,
        book.language.__str__(),
        book.publisher,
        date_add,
        date_update
        )
    cur = conn.cursor()
    cur.execute(sql, data)
    id_book = cur.lastrowid
    conn.commit()
    conn.close()
    results = book.dict()
    results.update({'id_book': id_book, 'date_update': date_add})
    return results


# Read Books
@app.get(
    path="/books",
    status_code=status.HTTP_200_OK,
    summary="Shows all books",
    response_model=List[BookBase],
    tags=["Book"]
)
def show_all_books() -> List[BookBase]:
    """
    Shows all books
    """
    conn = connectionDB()
    cur = conn.cursor()
    colums = "id_book,title,reading_age,pages,"\
        "language,publisher,date_add,date_update"
    cur.execute(f"SELECT {colums} FROM Book")
    rows = cur.fetchall()
    conn.close()
    list_keys = colums.split(',')
    results = list(
        map(
            lambda x: {list_keys[i]: x[i] for i in range(len(x))}, rows)
        )
    return results


# Read a book
@app.get(
    path="/book/details",
    status_code=status.HTTP_200_OK,
    tags=["Book"],
    response_model=BookBase,
    summary="Show details about a book"
    )
def show_book(
    id_book: int = Query(
        ...,
        gt=0,
        title="Book id",
        description="Book id unique"
        )
) -> BookBase:
    conn = connectionDB()
    cur = conn.cursor()
    features = "id_book,title,reading_age,pages,"\
        "language,publisher,date_add,date_update"
    cur.execute(f"SELECT {features} FROM Book WHERE id_book=?", (id_book,))
    rows = cur.fetchall()
    if len(rows) == 0:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="¡The book does not exists!"
            )
    conn.close()
    list_keys = features.split(',')
    row = rows[0]
    results = {list_keys[i]: row[i] for i in range(len(row))}
    return results


# Update a book
@app.put(
    path="/book/update",
    status_code=status.HTTP_200_OK,
    tags=["Book"],
    response_model=BookBase,
    summary="Updates a book"
    )
def update_book(book: BookUpdate = Body(...)) -> BookBase:
    bookUpdate = book.dict()
    [bookUpdate.pop(b) for b in bookUpdate.copy() if bookUpdate.get(b) is None]
    if len(bookUpdate) < 2:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="¡It is necessary a feature to change!"
            )
    conn = connectionDB()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Book WHERE id_book=?", (book.id_book,))
    rows = cur.fetchall()
    if len(rows) == 0:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="¡The book does not exists!"
            )
    features = "id_book,title,reading_age,pages,\
language,publisher,date_add,date_update"
    list_keys = features.split(',')
    row = rows[0]
    dataUpdate = {list_keys[i]: row[i] for i in range(len(row))}
    dataUpdate.update(bookUpdate)
    sql = ''' UPDATE Book
              SET title = ? ,
                  reading_age = ? ,
                  pages = ?,
                  language = ?,
                  publisher = ?,
                  date_add = ?,
                  date_update = ?
              WHERE id_book = ?'''
    values = (
        dataUpdate['title'],
        dataUpdate['reading_age'].__str__(),
        dataUpdate['pages'],
        dataUpdate['language'].__str__(),
        dataUpdate['publisher'],
        dataUpdate['date_add'],
        datetime.now().strftime("%Y-%m-%d"),
        dataUpdate['id_book']
    )
    cur.execute(sql, values)
    conn.commit()
    conn.close()
    return dataUpdate


# Delete a book
@app.delete(
    path="/book/delete",
    status_code=status.HTTP_200_OK,
    summary="Delete a book",
    response_model=dict,
    tags=["Book"]
)
def delete_a_book(id_book: int = Query(
        ...,
        gt=0,
        title="Book id",
        description="Book id unique"
        )
) -> dict:
    conn = connectionDB()
    cur = conn.cursor()
    features = "id_book,title,date_add,date_update"
    cur.execute(f"SELECT {features} FROM Book WHERE id_book=?", (id_book,))
    rows = cur.fetchall()
    if len(rows) == 0:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="¡The book does not exists!"
            )
    sql = 'DELETE FROM Book WHERE id_book=?'
    cur.execute(sql, (id_book,))
    conn.commit()
    conn.close()
    list_keys = features.split(',')
    row = rows[0]
    results = {list_keys[i]: row[i] for i in range(len(row))}
    return results


# Author
# Create an Author
@app.post(
    path="/author/new",
    status_code=status.HTTP_201_CREATED,
    tags=["Author"],
    response_model=AuthorBase,
    summary="Create a new author"
    )
def create_author(author: AuthorBase = Body(...)) -> AuthorBase:
    """
    It creates an author
    """
    conn = connectionDB()
    sql = ''' INSERT INTO Author(name,nationality,genre,birthdate)
              VALUES(?,?,?,?) '''
    birthdate = author.birthdate
    if author.birthdate is not None:
        birthdate = birthdate.strftime("%Y-%m-%d")
    data = (
        author.name,
        author.nationality,
        author.genre,
        birthdate
        )
    cur = conn.cursor()
    cur.execute(sql, data)
    id_author = cur.lastrowid
    conn.commit()
    conn.close()
    results = author.dict()
    results.update({'id_author': id_author})
    return results


# Read Authors
@app.get(
    path="/authors",
    status_code=status.HTTP_200_OK,
    summary="Shows all authors",
    response_model=List[AuthorBase],
    tags=["Author"]
)
def show_all_authors() -> List[AuthorBase]:
    """
    Shows all authors
    """
    conn = connectionDB()
    cur = conn.cursor()
    colums = 'id_author,name,nationality,genre,birthdate'
    cur.execute(f"SELECT {colums} FROM Author")
    rows = cur.fetchall()
    conn.close()
    list_keys = colums.split(',')
    results = list(
        map(
            lambda x: {list_keys[i]: x[i] for i in range(len(x))}, rows)
        )
    return results


# Read a Author
@app.get(
    path="/author/details",
    status_code=status.HTTP_200_OK,
    tags=["Author"],
    response_model=AuthorBase,
    summary="Show details about an author"
    )
def show_author(
    id_author: int = Query(
        ...,
        gt=0,
        title="Author id",
        description="Author id unique"
        )
) -> AuthorBase:
    conn = connectionDB()
    cur = conn.cursor()
    features = 'id_author,name,nationality,genre,birthdate'
    cur.execute(f"SELECT {features} FROM Author WHERE id_author=?",
                (id_author,))
    rows = cur.fetchall()
    if len(rows) == 0:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="¡The author does not exists!"
            )
    conn.close()
    list_keys = features.split(',')
    row = rows[0]
    results = {list_keys[i]: row[i] for i in range(len(row))}
    return results


# Update a Author
@app.put(
    path="/author/update",
    status_code=status.HTTP_200_OK,
    tags=["Author"],
    response_model=AuthorBase,
    summary="Updates an author"
    )
def update_author(author: AuthorUpdate = Body(...)) -> AuthorBase:
    authorUpdate = author.dict()
    [authorUpdate.pop(b) for b in authorUpdate.copy() if authorUpdate.get(b) is None]
    if len(authorUpdate) < 2:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="¡It is necessary a feature to change!"
            )
    conn = connectionDB()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Author WHERE id_author=?",
                (authorUpdate['id_author'],))
    rows = cur.fetchall()
    if len(rows) == 0:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="¡The author does not exists!"
            )
    features = 'id_author,name,nationality,genre,birthdate'
    list_keys = features.split(',')
    row = rows[0]
    dataUpdate = {list_keys[i]: row[i] for i in range(len(row))}
    dataUpdate.update(authorUpdate)
    sql = ''' UPDATE Author
              SET name = ? ,
                  nationality = ? ,
                  genre = ?,
                  birthdate = ?
              WHERE id_author = ?'''
    values = (
        dataUpdate['name'],
        dataUpdate['nationality'],
        dataUpdate['genre'],
        dataUpdate['birthdate'],
        dataUpdate['id_author']
    )
    cur.execute(sql, values)
    conn.commit()
    conn.close()
    return dataUpdate


# Delete a Author
