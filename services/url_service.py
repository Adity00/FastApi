import random
import string
from datetime import datetime,timedelta
from exceptions import URLCreationError,URLExpiredError,URLNotFoundError
from psycopg import OperationalError

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

        for attmept in range(3):
            try:
                created = create_url(
                    short_code=short_code,
                    url=str(url),
                    expires_at=expires_at
                )
                break

            except OperationalError:
                if attmept == 2:
                    raise URLCreationError(
                        "could not create short URL"
                    )      

        if created:
            return short_code, expires_at

def get_url_for_redirect(code):
    result = get_url_and_increment_clicks(code)

    if result is None:
        raise URLNotFoundError('URL not Found')

    if result['status'] == 'expired':
        raise URLExpiredError('URL Expired')
    
    return result
