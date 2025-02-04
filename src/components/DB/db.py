import os
from sqlalchemy import create_engine, text
from pandas import read_sql

def connect_to_postgres():
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("POSTGRES_DB")
    DB_USER = os.getenv("POSTGRES_USER")
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    try:
        DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        engine = create_engine(DATABASE_URL)

        with engine.connect() as conn:
            result = conn.execute(text("SELECT 'Connection successful'"))
            print(result.fetchone()[0])
        return engine
    except Exception as e:
        print("Error connecting to PostgreSQL:", e)
        return None

def query_db(engine, query):
    return read_sql(query, engine)