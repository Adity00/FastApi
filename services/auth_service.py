from database.queries import create_user
from security import hash_password

def register_user(email, password):
    return create_user(email,hash_password(password))
