from fastapi import FastAPI

from routes.urls import router
from database.connection import connection
from database.queries import create_url

app = FastAPI()

@app.get("/")
def home():
    return{
        "message":"Welcome to URL shortener"
    }

@app.get("/about")
def ab():
    return{
        "Project":"URL shortener",
        "Author":"Adi"
    }

app.include_router(router)

create_url(
    "test01",
    "https://google.com"
)