import random
import string

from database.memory import url_database

def generate_short_code(lenght=6):
    char = string.digits+string.ascii_letters

    while True:
        res=''
        for i in range(lenght):
            res+=random.choice(char)
        if res not in url_database:
            return res    