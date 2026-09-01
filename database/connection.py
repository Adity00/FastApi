import psycopg

connection = psycopg.connect(
    host = 'localhost',
    port = 5432,
    dbname = 'url_shortener',
    user = 'postgres',
    password = 'postgres'
)

print(connection)