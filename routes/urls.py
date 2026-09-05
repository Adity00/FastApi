from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse

from models.url import URLRequest,URLResponse,URLStatsResponse
from services.url_service import create_short_url, get_url_for_redirect
from database.queries import get_url_stats


router = APIRouter()


@router.post("/shorten",response_model=URLResponse, status_code=status.HTTP_201_CREATED)
def shorten(request: URLRequest):

    short_code, expires_at = create_short_url(
        request.url,
        request.expires_in
    )

    return {
        "original_url": request.url,
        "shortcode": short_code,
        "expires_at":expires_at
    }


@router.get("/stats/{code}", response_model=URLStatsResponse)
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

    result, url = get_url_for_redirect(code)

    if result == 'Not_Found':
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short code not found"
        )
    if result == 'Expired':
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="URL_Expired"
        )

    return RedirectResponse(
        url=url,
        status_code=302
    )