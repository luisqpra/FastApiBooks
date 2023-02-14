# Python
from typing import Optional, Dict, List
from enum import Enum
from datetime import date

# Base data
from database.funtionsDB import connectionDB

# Pydantic
from pydantic import BaseModel
from pydantic import SecretStr
from pydantic import EmailStr
from pydantic import Field


# FastAPI
from fastapi import FastAPI, status
from fastapi import Body
# Body, Path
from fastapi import HTTPException

app = FastAPI()
app.title = "Library"
app.version = " 0.0.1"


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


# Modes User
class UserBase(BaseModel):
    firts_name: str = Field(
        default=None,
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
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


class UserOut(UserBase):
    pass


# Home
@app.get(
    path="/",
    status_code=status.HTTP_200_OK,
    tags=["Home"]
    )
def home() -> Dict:
    return {"Hello": "World"}


# Create a User
@app.post(
    path="/User/new",
    status_code=status.HTTP_201_CREATED,
    tags=["User"],
    summary="Create a new user and return it"
    )
def create_user(user: User = Body(...)):
    """
    It creates a user
    - Args:
      user (User): User = Body(...)
    - Returns:
      The user object with the id_user field added.
    """
    conn = connectionDB()
    sql = ''' INSERT INTO User(firts_name, last_name, email, birth_date, password)
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
    cur = conn.cursor()
    # detect if email exists in DB
    cur.execute("SELECT * FROM User WHERE email=?", (user.email,))
    rows = cur.fetchall()
    if len(rows) > 0:
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
    summary="Show all users",
    tags=["User"]
)
def show_all_users():
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
