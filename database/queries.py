from database.connection import pool
from psycopg.errors import UniqueViolation

def create_url(short_code, url, expires_at=None):
    try:
        with pool.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO urls (shortcode, url, expires_at)
                    VALUES (%s, %s, %s)
                    """,
                    (short_code, url, expires_at)
                )

        return True

    except UniqueViolation:
        print("Collison:",short_code)
        return False

def get_url_stats(shortcode):
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT  url, clicks, expires_at
                FROM urls
                WHERE shortcode = %s
                """,
                (shortcode,)
            )
            row = cursor.fetchone()
    if row is None:
        return None

    return{
        'url': row[0],
        'clicks': row[1],
        'expires_at':row[2]
    }     

def get_url_and_increment_clicks(shortcode):
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE urls
                SET clicks = clicks + 1
                WHERE shortcode = %s
                AND (
                        expires_at is NULL 
                        OR
                        expires_at > CURRENT_TIMESTAMP    
                    )
                RETURNING url, expires_at   
                """,
                (shortcode,)
            )

            row = cursor.fetchone()

            if row is not None:
                return {
                    'status':'success',
                    "url":row[0],
                    'expires_at':row[1]
                }

            cursor.execute(
                """
                SELECT expires_at
                FROM urls
                WHERE shortcode = %s
                """,
                (shortcode,)
            )

            row = cursor.fetchone()

            if row is None:
                return{
                    'status':'not_found'
                }

            return{
                'status':'expired'
            }
        