from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import random
import string
from fastapi.responses import RedirectResponse

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Welcome to URL shortener Api"
    }


@app.get("/about")
def ab():
    return {
        "Project": "Url shortener",
        "Author": "Adi"
    }


@app.get("/hello/{name}")
def greet(name):
    return {
        "Message": f"Hello {name}",
        "message": "Welcome!",
        "original": name,
        "uppercase": name.upper(),
        "lowercase": name.lower(),
        "length": len(name),
        "first_letter": name[0],
        "last_letter": name[-1],
        "reversed": name[::-1]
    }


@app.get("/search")
def search(q):
    return {
        "query": q
    }


@app.get("/calculator")
def calculate(a: int, b: int):
    return {
        "a": a,
        "b": b,
        "sum": a + b
    }


class URLRequest(BaseModel):
    url: str


url_database = {}


@app.post("/shorten", status_code=status.HTTP_201_CREATED)
def shorten(request: URLRequest):
    short_code = generate_short_code()

    url_database[short_code] = request.url

    print(url_database)

    return {
        "originalUrl": request.url,
        "shortcode": short_code
    }


@app.get("/code/{code}")
def redirect(code: str):
    if code in url_database:
        return RedirectResponse(
            url=url_database[code],
            status_code=302
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Short code not found"
    )


def generate_short_code(length=6):
    chars = string.digits + string.ascii_letters

    while True:
        res = ""

        for i in range(length):
            res += random.choice(chars)

        if res not in url_database:
            return res