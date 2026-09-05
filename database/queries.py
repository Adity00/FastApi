from database.connection import pool

def create_url(short_code, url, expires_at=None):
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO urls (shortcode, url, expires_at)' \
                'VALUES (%s,%s,%s)',
                (short_code, url, expires_at)
            )
    

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

def get_url_for_redirect_db(shortcode):
    with pool.connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT url, expires_at
                FROM urls
                WHERE shortcode = %s
                """,
                (shortcode,)
            )
            row = cursor.fetchone()
    if row is None:
        return None
    return{
        "url": row[0],
        "expires_at": row[1]
    } 

def increment_clicks(shortcode):  
    with pool.connection() as connection:
        with  connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE urls 
                SET clicks = clicks + 1
                WHERE shortcode = %s
                """,
                (shortcode,)
            )
