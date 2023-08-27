# Python
from typing import Dict

# FastAPI
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi import status

home_router = APIRouter()


# Home
@home_router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    tags=["Home"]
    )
def home() -> Dict:
    return HTMLResponse('<h1> Hello word FastAPI</h1>')
    # return {"Hello": "World"}
