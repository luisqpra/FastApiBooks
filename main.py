# FastAPI
from fastapi import FastAPI

# Middlewares
from middlewares.error_handler import ErrorHandler

# Router
from routes.user import user_router
from routes.book import book_router
from routes.home import home_router
from routes.author import author_router

app = FastAPI()
app.title = "Library"
app.version = " 0.0.1"

app.add_middleware(ErrorHandler)
app.include_router(home_router)
app.include_router(user_router)
app.include_router(book_router)
app.include_router(author_router)
