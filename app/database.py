from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config  import settings

# SQLALCHEMY_DATABASE_URL = f'postgresql://{postgres}:{root}@{127.0.0.1}:{5432}/{db_fastapi}'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Will keep trying to connect to the database, before starting up the server
# while True:

#     try:
#         # REALDictCursor converts the coloumns into a dictionary!
#         conn= psycopg2.connect(host='127.0.0.1',dbname='db_fastapi', user='postgres',
#                 password='root', cursor_factory=RealDictCursor)
        
#         cursor = conn.cursor()
#         print("Database connection was successful")
#         break
#     except Exception as error:
#         print("Connecting to Database failed")
#         print("Error", error)
#         time.sleep(2)
