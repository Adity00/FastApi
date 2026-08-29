from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse
from datetime import datetime, timedelta

from models.url import URLRequest
from database.memory import url_database
from services.url_service import generate_short_code


router = APIRouter()


@router.post("/shorten", status_code=status.HTTP_201_CREATED)
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

    return {
        "original_url": request.url,
        "shortcode": short_code,
        "expires_at": expires_at
    }


@router.get("/stats/{code}")
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


@router.get("/{code}")
def redirect_url(code: str):

    if code not in url_database:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short code not found"
        )

    url_data = url_database[code]

    if url_data["expires_at"] is not None:

        if datetime.now() > url_data["expires_at"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="URL expired"
            )

    url_data["clicks"] += 1

    return RedirectResponse(
        url=url_data["url"],
        status_code=302
    )