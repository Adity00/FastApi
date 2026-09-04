import random
import string
from datetime import datetime,timedelta

from database.queries import create_url, get_url_for_redirect_db,increment_clicks

def generate_short_code(length=6):
    characters = string.digits + string.ascii_letters
    return ''.join(random.choice(characters) for _ in range(length))    

def create_short_url(url, expire_in=None):
    short_code = generate_short_code()

    expires_at=None

    if expire_in is not None:
        expires_at = datetime.now() + timedelta(seconds=expire_in)

    create_url(
        short_code=short_code,
        url=str(url),
        expires_at=expires_at
    )
    return short_code,expires_at

def get_url_for_redirect(code):
    record = get_url_for_redirect_db(code)

    if record is None:
        return "Not_Found",None

    if record["expires_at"] is not None:
        if datetime.now() > record["expires_at"]:
            return "Expired",None 

    increment_clicks(code)

    return "Success", record["url"]