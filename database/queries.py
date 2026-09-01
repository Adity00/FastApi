from database.connection import connection

def create_url(short_code, url, expires_at=None):

    with connection.cursor() as cursor:
        cursor.execute(
            'INSERT INTO urls (shortcode, url, expires_at)' \
            'VALUES (%s,%s,%s)',
            (short_code, url, expires_at)
        )

    connection.commit() 