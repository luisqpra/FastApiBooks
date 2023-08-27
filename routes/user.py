# Python
import re
from typing import Optional, List
from datetime import date

# FastAPI
from fastapi import APIRouter
from fastapi import status
from fastapi import Body, Query, Path
from fastapi import HTTPException

# Base data
from database.funtionsDB import connectionDB

# Pydantic
from pydantic import BaseModel
from pydantic import SecretStr
from pydantic import EmailStr
from pydantic import Field

user_router = APIRouter()


# Funtions
def it_is_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(regex, email) is not None


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


# User
# Create a User
@user_router.post(
    path="/user/new",
    status_code=status.HTTP_201_CREATED,
    tags=["User"],
    response_model=User,
    summary="Create a new user"
    )
def create_user(user: User = Body(...)) -> User:
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
@user_router.get(
    path="/users",
    status_code=status.HTTP_200_OK,
    summary="Shows all users",
    response_model=List[User],
    tags=["User"]
)
def show_all_users() -> List[User]:
    """
    Shows all users
    """
    conn = connectionDB()
    cur = conn.cursor()
    colums = 'id_user,firts_name,last_name,email,birth_date,password'
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
@user_router.get(
    path="/user/details",
    status_code=status.HTTP_200_OK,
    tags=["User"],
    response_model=User,
    summary="Show details about a user"
    )
def show_user(
    id_user: int = Query(
        ...,
        gt=0,
        title="User id",
        description="User id unique"
        )
) -> User:
    conn = connectionDB()
    cur = conn.cursor()
    features = 'id_user,firts_name,last_name,email,birth_date,password'
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


# Update a user (Deprecated)
@user_router.put(
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
@user_router.put(
    path="/user/update",
    status_code=status.HTTP_200_OK,
    tags=["User"],
    response_model=User,
    summary="Updates a user"
    )
def update_user2(user: UserUpdate = Body(...)) -> User:
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
    features = 'id_user,firts_name,last_name,email,password,birth_date'
    list_keys = features.split(',')
    row = rows[0]
    dataUpdate = {list_keys[i]: row[i] for i in range(len(row))}
    print(dataUpdate)
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
        dataUpdate['password'],
        dataUpdate['id_user']
    )
    cur.execute(sql, values)
    conn.commit()
    conn.close()
    return dataUpdate


# Delete a user
@user_router.delete(
    path="/user/delete",
    status_code=status.HTTP_200_OK,
    summary="Delete a user",
    response_model=dict,
    tags=["User"]
)
def delete_a_user(id_user: int = Query(
        ...,
        gt=0,
        title="User id",
        description="User id unique"
        )
) -> dict:
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
