import psycopg2.extras
from utils.db import get_db_connection, release_db_connection

async def get_vocabs(q: str = None, limit: int = 10, page: int = 1):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    sql = f"""
        select * from vocabs
        where 1=1 
    """
    value = []

    if q:
        sql += "and vocab ilike %s"
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

async def random_vocab():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    sql = """
        select * from vocabs
        where remember = false
        order by random()
        limit 1
    """
    cur.execute(sql)
    row = dict(cur.fetchone())

    cur.close()
    release_db_connection(conn)

    return row

async def remember_vocab(vocab: str):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    sql = """
        update vocabs
        set remember = true
        where vocab = %s
    """
    cur.execute(sql, (vocab,))
    conn.commit()

    cur.close()
    release_db_connection(conn)
    return True