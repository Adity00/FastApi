import os

from psycopg_pool import ConnectionPool
from dotenv import load_dotenv

load_dotenv()

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")


if any([
    not db_host,
    not db_port,
    not db_name,
    not db_user,
    not db_password
]):
    raise ValueError("Missing required database configuration")


pool = ConnectionPool(
    conninfo=(
        f"host={db_host} "
        f"port={db_port} "
        f"dbname={db_name} "
        f"user={db_user} "
        f"password={db_password} "
    ),
    min_size=1,
    max_size=5,
    open=True
)
