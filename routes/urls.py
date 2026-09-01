from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse
from datetime import datetime, timedelta

from models.url import URLRequest,URLRecord
from database.memory import url_database
from services.url_service import generate_short_code,create_short_url,get_url_for_redirect


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

    if code in url_database:
        record = url_database[code]
        return {
            "shortcode": code,
            "original_url": record.url,
            "clicks": record.clicks,
            "expires_at": record.expires_at
        }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Short code not found"
    )


@router.get("/{code}")
def redirect_url(code: str):

    url = get_url_for_redirect(code)

    return RedirectResponse(
        url=url,
        status_code=302
    )








# @router.post("/shorten", status_code=status.HTTP_201_CREATED)
# def shorten(request: URLRequest):

#     short_code = generate_short_code()

#     expires_at = None

#     if request.expires_in is not None:
#         expires_at = datetime.now() + timedelta(
#             seconds=request.expires_in
#         )

#     url_database[short_code] = URLRecord(
#         url = request.url,
#         clicks=0,
#         expires_at=expires_at
#     )

#     return {
#         "original_url": request.url,
#         "shortcode": short_code,
#         "expires_at": expires_at
#     }
