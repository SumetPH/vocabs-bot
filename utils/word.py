import psycopg2.extras
from utils.db import get_db_connection, release_db_connection

async def get_words(q: str = None, limit: int = 10, page: int = 1):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    sql = f"""
        select * from word
        where 1=1 
    """
    value = []

    if q:
        sql += "and word ilike %s"
        value.append(f"%{q}%")
    

    sql += "offset %s"
    value.append((page - 1) * limit)

    sql += "limit %s"
    value.append(limit)

    cur.execute(sql, value)
    rows = [dict(row) for row in cur.fetchall()]

    cur.close()
    release_db_connection(conn)
    
    return rows

async def random_word():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    sql = """
        select * from word
        where remember = false
        order by random()
        limit 1
    """
    cur.execute(sql)
    row = dict(cur.fetchone())

    cur.close()
    release_db_connection(conn)

    return row

async def remember_word(word: str):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    sql = """
        update word
        set remember = true
        where word = %s
    """
    cur.execute(sql, (word,))
    conn.commit()

    cur.close()
    release_db_connection(conn)
    return True