# Python
from typing import Optional, List
from datetime import date

# Base data
from database.funtionsDB import connectionDB

# Pydantic
from pydantic import BaseModel
from pydantic import Field

# FastAPI
from fastapi import status
from fastapi import Body, Query
from fastapi import HTTPException
from fastapi import APIRouter

author_router = APIRouter()


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


# Author
# Create an Author
@author_router.post(
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
@author_router.get(
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
@author_router.get(
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
@author_router.put(
    path="/author/update",
    status_code=status.HTTP_200_OK,
    tags=["Author"],
    response_model=AuthorBase,
    summary="Updates an author"
    )
def update_author(author: AuthorUpdate = Body(...)) -> AuthorBase:
    autUp = author.dict()
    [autUp.pop(b) for b in autUp.copy() if autUp.get(b) is None]
    authorUpdate = autUp
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
@author_router.delete(
    path="/author/delete",
    status_code=status.HTTP_200_OK,
    summary="Delete an author",
    response_model=dict,
    tags=["Author"]
)
def delete_an_author(id_author: int = Query(
        ...,
        gt=0,
        title="Author id",
        description="Author id unique"
        )
) -> dict:
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
    sql = 'DELETE FROM Author WHERE id_author=?'
    cur.execute(sql, (id_author,))
    conn.commit()
    conn.close()
    list_keys = features.split(',')
    row = rows[0]
    results = {list_keys[i]: row[i] for i in range(len(row))}
    return results
