# Python
from typing import Optional, Dict
from enum import Enum
from datetime import date, datetime
import re

# Base data
from database.funtionsDB import connectionDB

# Pydantic
from pydantic import BaseModel
from pydantic import SecretStr
from pydantic import EmailStr
from pydantic import Field


# FastAPI
from fastapi import FastAPI, status
from fastapi import Body, Query, Path
from fastapi import HTTPException

app = FastAPI()
app.title = "Library"
app.version = " 0.0.1"


# Funtions
def it_is_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(regex, email) is not None


# Modes
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


# Home
@app.get(
    path="/",
    status_code=status.HTTP_200_OK,
    tags=["Home"]
    )
def home() -> Dict:
    return {"Hello": "World"}


# User
# Create a User
@app.post(
    path="/user/new",
    status_code=status.HTTP_201_CREATED,
    tags=["User"],
    summary="Create a new user"
    )
def create_user(user: User = Body(...)):
    """
    It creates a user
    """
    conn = connectionDB()
    sql = ''' INSERT INTO User(firts_name, last_name, \
    email, birth_date, password)
              VALUES(?,?,?,?,?) '''
    if user.birth_date is not None:
        birth_date = user.birth_date.strftime("%Y-%m-%d")
    else:
        birth_date = None
    data = (
        user.firts_name,
        user.last_name,
        user.email,
        birth_date,
        user.password.get_secret_value()
        )
    if not it_is_email(user.email):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="¡It is not valid email!"
            )
    cur = conn.cursor()
    # detect if email exists in DB
    cur.execute("SELECT * FROM User WHERE email=?", (user.email,))
    rows = cur.fetchall()
    if len(rows) > 0:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="¡This email already exists!"
            )
    cur.execute(sql, data)
    id_user = cur.lastrowid
    conn.commit()
    conn.close()
    results = user.dict()
    results.update({'id_user': id_user})
    return results


# Read Users
@app.get(
    path="/users",
    status_code=status.HTTP_200_OK,
    summary="Shows all users",
    tags=["User"]
)
def show_all_users():
    """
    Shows all users
    """
    conn = connectionDB()
    cur = conn.cursor()
    colums = 'id_user,firts_name,last_name,email,birth_date'
    cur.execute(f"SELECT {colums} FROM User")
    rows = cur.fetchall()
    conn.close()
    list_keys = colums.split(',')
    results = list(
        map(
            lambda x: {list_keys[i]: x[i] for i in range(len(x))}, rows)
        )
    return results


# Read a user
@app.get(
    path="/user/details",
    status_code=status.HTTP_200_OK,
    tags=["User"],
    summary="Show details about a user"
    )
def show_user(
    id_user: int = Query(
        ...,
        gt=0,
        title="User id",
        description="User id unique"
        )
):
    conn = connectionDB()
    cur = conn.cursor()
    features = 'id_user,firts_name,last_name,email,birth_date'
    cur.execute(f"SELECT {features} FROM User WHERE id_user=?", (id_user,))
    rows = cur.fetchall()
    if len(rows) == 0:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="¡The user does not exists!"
            )
    conn.close()
    list_keys = features.split(',')
    row = rows[0]
    results = {list_keys[i]: row[i] for i in range(len(row))}
    return results


# Update a user
@app.put(
    path="/user/update_user/{id_user}/{feature}/{data}",
    status_code=status.HTTP_200_OK,
    tags=["User"],
    summary="Updates a user",
    deprecated=True
    )
def update_user(
    id_user: int = Path(
        ...,
        title="user id",
        gt=0
    ),
    feature: str = Path(
        ...,
        title="Feature",
        description="feature to change"
    ),
    data: str = Path(
        ...,
        title="data",
        description="data changing"
    )
):
    if feature == 'email' and not it_is_email(data):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="¡It is not valid email!"
            )
    conn = connectionDB()
    cur = conn.cursor()
    cur.execute(f"SELECT {feature} FROM User WHERE id_user=?", (id_user,))
    rows = cur.fetchall()
    if len(rows) == 0:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="¡The user does not exists!"
            )
    query = f"UPDATE user SET {feature} = '{data}' WHERE id_user = {id_user}"
    cur.execute(query)
    conn.commit()
    conn.close()
    result = {
        'mesmessage': 'Update successful',
        'id_user': id_user,
        feature: data
        }
    return result


# Update a user
@app.put(
    path="/user/update",
    status_code=status.HTTP_200_OK,
    tags=["User"],
    summary="Updates a user"
    )
def update_user2(user: UserUpdate = Body(...)):
    userUpdate = user.dict()
    [userUpdate.pop(b) for b in userUpdate.copy() if userUpdate.get(b) is None]
    if len(userUpdate) < 2:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="¡It is necessary a feature to change!"
            )
    conn = connectionDB()
    cur = conn.cursor()
    cur.execute("SELECT * FROM User WHERE id_user=?", (user.id_user,))
    rows = cur.fetchall()
    if len(rows) == 0:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="¡The user does not exists!"
            )
    features = 'id_user,firts_name,last_name,email,birth_date,password'
    list_keys = features.split(',')
    row = rows[0]
    dataUpdate = {list_keys[i]: row[i] for i in range(len(row))}
    dataUpdate.update(userUpdate)
    sql = ''' UPDATE User
              SET firts_name = ? ,
                  last_name = ? ,
                  email = ?,
                  birth_date = ?,
                  password = ?
              WHERE id_user = ?'''
    values = (
        dataUpdate['firts_name'],
        dataUpdate['last_name'],
        dataUpdate['email'],
        dataUpdate['birth_date'],
        dataUpdate['password'].get_secret_value(),
        dataUpdate['id_user']
    )
    cur.execute(sql, values)
    conn.commit()
    conn.close()
    return dataUpdate


# Delete a user
@app.delete(
    path="/user/delete",
    status_code=status.HTTP_200_OK,
    summary="Delete a user",
    tags=["User"]
)
def delete_a_user(id_user: int = Query(
        ...,
        gt=0,
        title="User id",
        description="User id unique"
        )
):
    conn = connectionDB()
    cur = conn.cursor()
    features = 'id_user,firts_name,last_name,email,birth_date'
    cur.execute(f"SELECT {features} FROM User WHERE id_user=?", (id_user,))
    rows = cur.fetchall()
    if len(rows) == 0:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="¡The user does not exists!"
            )
    sql = 'DELETE FROM User WHERE id_user=?'
    cur.execute(sql, (id_user,))
    conn.commit()
    conn.close()
    list_keys = features.split(',')
    row = rows[0]
    results = {list_keys[i]: row[i] for i in range(len(row))}
    return results


# Book
# Create a Book
@app.post(
    path="/book/new",
    status_code=status.HTTP_201_CREATED,
    tags=["Book"],
    summary="Create a new book"
    )
def create_book(book: BookBase = Body(...)):
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
    tags=["Book"]
)
def show_all_books():
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
    summary="Show details about a book"
    )
def show_book(
    id_book: int = Query(
        ...,
        gt=0,
        title="Book id",
        description="Book id unique"
        )
):
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


# Update a user
@app.put(
    path="/book/update",
    status_code=status.HTTP_200_OK,
    tags=["Book"],
    summary="Updates a book"
    )
def update_book(book: BookUpdate = Body(...)):
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
        dataUpdate['date_update'],
        dataUpdate['id_book']
    )
    cur.execute(sql, values)
    conn.commit()
    conn.close()
    return dataUpdate
