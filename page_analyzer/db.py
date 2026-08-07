import os
 
import psycopg2
import psycopg2.extras
 
 
def get_db_connection():
    conn = psycopg2.connect(
        os.getenv('DATABASE_URL'),
        cursor_factory=psycopg2.extras.RealDictCursor
    )
    return conn
 
 
def find_url_by_name(conn, name):
    with conn.cursor() as curs:
        curs.execute("SELECT id, name FROM urls WHERE name = %s", (name,))
        return curs.fetchone()
 
 
def create_url(conn, name, created_at):
    with conn.cursor() as curs:
        curs.execute(
            "INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id",
            (name, created_at)
        )
        url_id = curs.fetchone()['id']
    conn.commit()
    return url_id
 
 
def get_urls_with_last_check(conn):
    with conn.cursor() as curs:
        curs.execute("""
            SELECT
                urls.id,
                urls.name,
                last_check.created_at AS last_check_date,
                last_check.status_code AS last_status_code
            FROM urls
            LEFT JOIN (
                SELECT DISTINCT ON (url_id)
                    url_id, created_at, status_code
                FROM url_checks
                ORDER BY url_id, created_at DESC
            ) AS last_check ON urls.id = last_check.url_id
            ORDER BY urls.id DESC
        """)
        return curs.fetchall()
 
 
def get_url_by_id(conn, url_id):
    with conn.cursor() as curs:
        curs.execute("SELECT * FROM urls WHERE id = %s", (url_id,))
        return curs.fetchone()
 
 
def get_checks_for_url(conn, url_id):
    with conn.cursor() as curs:
        curs.execute(
            "SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC",
            (url_id,)
        )
        return curs.fetchall()
 
 
def create_url_check(conn, url_id, status_code, h1, title, description, created_at):
    with conn.cursor() as curs:
        curs.execute(
            "INSERT INTO url_checks "
            "(url_id, status_code, h1, title, description, created_at) "
            "VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
            (url_id, status_code, h1, title, description, created_at)
        )
    conn.commit()
 