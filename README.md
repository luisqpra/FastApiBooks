# FastApiBooks
FastAPI is a Python framework designed for the creation of fast and secure web API applications. Using FastAPI, it is easy to define and expose endpoints to receive and send HTTP requests and process input and output data. Additionally, FastAPI provides a dynamic user interface for quickly and easily testing and documenting the API.

## FastAPI Test App
This is a simple API developed using the FastAPI framework in Python.

Requirements
FastAPI
pydantic
typing

### Endpoints
GET /
Returns a simple message.

GET /books/{id}
Takes an id parameter and returns it in the response.

POST /books
Takes a Book object as input and returns a message indicating that the book has been inserted.

### Book Model
The Book model has the following attributes:

title (required): Title of the book.
author (required): Author of the book.
pages (required): Number of pages in the book.
editorial (optional): Editorial of the book.

