from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse

from models.url import URLRequest,URLResponse,URLStatsResponse
from services.url_service import create_short_url, get_url_for_redirect, get_stats_for_url
from exceptions import URLCreationError,URLExpiredError,URLNotFoundError


router = APIRouter()


@router.post("/shorten",response_model=URLResponse, status_code=status.HTTP_201_CREATED)
def shorten(request: URLRequest):
    try:
        short_code, expires_at = create_short_url(
            request.url,
            request.expires_in
        )

    except URLCreationError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='could not create short URL'
        )    

    return {
        "original_url": request.url,
        "shortcode": short_code,
        "expires_at":expires_at
    }


@router.get("/stats/{code}", response_model=URLStatsResponse)
def stats(code: str):
    try:
        record = get_stats_for_url(code)
        
    except URLNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short code not found"
        )

    return {
        'shortcode':code,
        'original_url':record['url'],
        'clicks':record['clicks'],
        'expires_at':record['expires_at']
    }    
    

@router.get("/{code}")
def redirect_url(code: str):
    try:
        result = get_url_for_redirect(code)

    except URLExpiredError:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail='URL_Expired'
        )

    except URLNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Short code not found'
        )

    return RedirectResponse(
        url=result['url'],
        status_code=302
    )
