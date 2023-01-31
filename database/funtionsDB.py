import sqlite3 as sql
from sqlite3 import Error


def connectionDB() -> sql.Connection:
    conn = sql.connect("database/library.db")
    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    - Args:
      conn: Connection object
      create_table_sql: a CREATE TABLE statement
    - Returns:
      Optional [print error]
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    conn = connectionDB()
    sql_create_table_user = """CREATE TABLE IF NOT EXISTS User (
        id_user integer NOT NULL,
        firts_name text,
        last_name text,
        email text,
        password text NOT NULL,
        birth_date text,
        PRIMARY KEY(id_user),
        UNIQUE(id_user,email)
        );"""
    sql_create_table_Book = """CREATE TABLE IF NOT EXISTS Book (
        id_book integer NOT NULL,
        title text,
        reading_age text,
        pages integer NOT NULL,
        language text,
        publisher text,
        date_add text NOT NULL,
        date_update text NOT NULL,
        PRIMARY KEY(id_book),
        UNIQUE(id_book)
        );"""
    sql_create_table_Author = """CREATE TABLE IF NOT EXISTS Author (
        id_author integer NOT NULL,
        name text NOT NULL,
        nationality text,
        genre text,
        birthdate text,
        PRIMARY KEY(id_author),
        UNIQUE(id_author)
        );"""
    sql_create_table_User_Book = """CREATE TABLE IF NOT EXISTS User_Book (
        id_user_book integer NOT NULL,
        fk_id_user integer NOT NULL,
        fk_id_book integer NOT NULL,
        PRIMARY KEY(id_user_book),
        UNIQUE(id_user_book),
        FOREIGN KEY (fk_id_user)
            REFERENCES User (id_user)
                ON UPDATE CASCADE
                ON DELETE CASCADE,
        FOREIGN KEY (fk_id_book)
            REFERENCES Book (id_book)
                ON UPDATE CASCADE
                ON DELETE CASCADE
        );"""
    sql_create_table_Book_Author = """CREATE TABLE IF NOT EXISTS Book_Author (
        id_book_author integer NOT NULL,
        fk_id_author integer NOT NULL,
        fk_id_book integer NOT NULL,
        PRIMARY KEY(id_book_author),
        UNIQUE(id_book_author),
        FOREIGN KEY (fk_id_author)
            REFERENCES Author (id_author)
                ON UPDATE CASCADE
                ON DELETE CASCADE,
        FOREIGN KEY (fk_id_book)
            REFERENCES Book (id_book)
                ON UPDATE CASCADE
                ON DELETE CASCADE
        );"""
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_table_user)
        create_table(conn, sql_create_table_Book)
        create_table(conn, sql_create_table_Author)
        create_table(conn, sql_create_table_User_Book)
        create_table(conn, sql_create_table_Book_Author)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
