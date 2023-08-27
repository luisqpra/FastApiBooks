# Python
from typing import List
from datetime import datetime

# FastAPI
from fastapi import APIRouter
from fastapi import status
from fastapi import Body, Query
from fastapi import HTTPException

# Base data
from database.funtionsDB import connectionDB

# Model
from schemas.book import BookBase, BookUpdate

book_router = APIRouter()


# Book
# Create a Book
@book_router.post(
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
@book_router.get(
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
@book_router.get(
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
@book_router.put(
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
@book_router.delete(
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
