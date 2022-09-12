from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
from .config import settings

# demo: connect DB via psycopg2

# def get_db():
#     global conn
#     try:
#         conn = psycopg2.connect(host=settings.database_hostname, database=settings.database_name,
#                                 user=settings.database_username,
#                                 password=settings.database_password, port=settings.database_port,
#                                 cursor_factory=RealDictCursor)
#         # cursor = conn.cursor()
#         print("Database connection was succesfull!")
#         yield conn
#
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(2)
#     finally:
#         if conn:
#             conn.close()


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@\
{settings.database_hostname}:{settings.database_port}/{settings.database_name}"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
