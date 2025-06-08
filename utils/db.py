import os
import psycopg2.pool
from dotenv import load_dotenv

load_dotenv()

conn_pool = psycopg2.pool.SimpleConnectionPool(1, 10, os.getenv("DATABASE_URL"))

def get_db_connection():
    return conn_pool.getconn()

def release_db_connection(conn):
    conn_pool.putconn(conn)