import random
import string
from datetime import datetime,timedelta

from database.queries import create_url, get_url_and_increment_clicks

def generate_short_code(length=6):
    characters = string.digits + string.ascii_letters
    return ''.join(random.choice(characters) for _ in range(length))    

def create_short_url(url, expire_in=None):

    expires_at=None

    if expire_in is not None:
        expires_at = datetime.now() + timedelta(seconds=expire_in)

    while True:
        short_code = generate_short_code()

        created = create_url(
            short_code=short_code,
            url=str(url),
            expires_at=expires_at
        )

        if created:
            return short_code, expires_at

def get_url_for_redirect(code):
    return get_url_and_increment_clicks(code)
