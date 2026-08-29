from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, HttpUrl
from fastapi.responses import RedirectResponse
from datetime import datetime, timedelta
import random
import string


app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Welcome to URL shortener API"
    }


@app.get("/about")
def ab():
    return {
        "Project": "URL shortener",
        "Author": "Adi"
    }


@app.get("/hello/{name}")
def greet(name: str):
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
def search(q: str):
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


# Request model
class URLRequest(BaseModel):
    url: HttpUrl
    expires_in: int | None = None


# Temporary in-memory database
url_database = {}


# Create short URL
@app.post("/shorten", status_code=status.HTTP_201_CREATED)
def shorten(request: URLRequest):

    short_code = generate_short_code()

    expires_at = None

    if request.expires_in is not None:
        expires_at = datetime.now() + timedelta(
            seconds=request.expires_in
        )

    url_database[short_code] = {
        "url": request.url,
        "clicks": 0,
        "expires_at": expires_at
    }

    print(url_database)

    return {
        "originalUrl": request.url,
        "shortcode": short_code,
        "expires_at": expires_at
    }


# Get statistics
@app.get("/stats/{code}")
def stats(code: str):

    if code in url_database:
        return {
            "shortcode": code,
            "original_url": url_database[code]["url"],
            "clicks": url_database[code]["clicks"],
            "expires_at": url_database[code]["expires_at"]
        }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Short code not found"
    )


# Redirect short URL
@app.get("/{code}")
def redirect(code: str):

    if code not in url_database:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short code not found"
        )

    url_data = url_database[code]

    # Check expiration
    if url_data["expires_at"] is not None:

        if datetime.now() > url_data["expires_at"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Short URL has expired"
            )

    # Count click
    url_data["clicks"] += 1

    # Redirect
    return RedirectResponse(
        url=url_data["url"],
        status_code=302
    )


# Generate unique short code
def generate_short_code(length=6):

    chars = string.digits + string.ascii_letters

    while True:

        res = ""

        for i in range(length):
            res += random.choice(chars)

        if res not in url_database:
            return res