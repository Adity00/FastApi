import random
import string
from datetime import datetime,timedelta

from database.memory import url_database
from models.url import URLRecord

def generate_short_code(lenght=6):
    char = string.digits+string.ascii_letters

    while True:
        res=''
        for i in range(lenght):
            res+=random.choice(char)
        if res not in url_database:
            return res    

def create_short_url(url, expire_in=None):
    short_code = generate_short_code()
    expires_at=None

    if expire_in is not None:
        expires_at = datetime.now() + timedelta(seconds=expire_in)

    url_database[short_code] = URLRecord(
        url = url,
        clicks = 0,
        expires_at= expires_at
    )
    return short_code