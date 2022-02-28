from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db
from app.main import app
from app.config import settings
from app.database import get_db, Base


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fixture is a function that runs before our test runs, this is done so that we can keep running our user tests with the same user!
# We drop all tables before we create all tables again, that solves our problem with using the same values for each row!

# We can access our DB object directly too!
# Returns our Dtabase Object

# This file is not used any more, moved to conftest.py!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# This fixture returns our Client
@pytest.fixture(scope="function")
def client(session):
    def override_get_db(): 
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    