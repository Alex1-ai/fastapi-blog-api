from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import sessionmaker
import psycopg2
import time
from .config import settings



SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


while True:
    try:
        conn = psycopg2.connect(host=f"{settings.database_hostname}", database=f"{settings.database_name}", user=f"{settings.database_username}", password=f"{settings.database_password}", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Database connection failed")
        print("Error: ", error)
        time.sleep(2)
