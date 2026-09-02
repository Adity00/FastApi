from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse

from models.url import URLRequest
from services.url_service import create_short_url, get_url_for_redirect
from database.queries import get_url_stats


router = APIRouter()


@router.post("/shorten", status_code=status.HTTP_201_CREATED)
def shorten(request: URLRequest):

    short_code = create_short_url(
        request.url,
        request.expires_in
    )

    return {
        "original_url": request.url,
        "shortcode": short_code
    }


@router.get("/stats/{code}")
def stats(code: str):

    record = get_url_stats(code)

    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short code not found"
        )

    return {
        "shortcode": code,
        "original_url": record["url"],
        "clicks": record["clicks"],
        "expires_at": record["expires_at"]
    }


@router.get("/{code}")
def redirect_url(code: str):

    url = get_url_for_redirect(code)

    if url is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short code not found or URL expired"
        )

    return RedirectResponse(
        url=url,
        status_code=302
    )