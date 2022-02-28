# This file is for all fixtures used, will available for anyhting in the package
# There is no need to import the fixtures in the test files, they are done autmatically by pytest
# Really great and easy to use file!

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db
from app.main import app
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fixture is a function that runs before our test runs, this is done so that we can keep running our user tests with the same user!
# We drop all tables before we create all tables again, that solves our problem with using the same values for each row!

# We can access our DB object directly too!
# Returns our Dtabase Object

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# This fixture returns our Client
@pytest.fixture
def client(session):
    def override_get_db(): 
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    

# Create a user before running login test
@pytest.fixture
def test_user(client):
    user_data = {"email": "aadil2@gmail.com", 
                "password": "fastapi"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201

    new_user=res.json()
    new_user['password'] = user_data['password']
    return new_user

# Create a user before running login test
@pytest.fixture
def test_user2(client):
    user_data = {"email": "aadil3@gmail.com", 
                "password": "fastapi"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201

    new_user=res.json()
    new_user['password'] = user_data['password']
    return new_user

# This fixture is for getting the token to get posts replies, ech post request needs authentication
# We can fake our own token without having to request a token from the API, we are testing only what we need to
@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

# this fixture gives an authorized client with a jwt token, this makes life easier
@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization" : f"Bearer {token}"
    }

    return client

# This fixture is to create a number of random posts, against which we can do any tests we want to, when needed
# We are going to create a number of posts directly in the database
@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user2['id']
    }]

    
    # This function converts/spreads out a single dictotionary into the format in models.Post
    def create_post_model(post):
        return models.Post(**post)
    
    # The map function, converts the data to be fed into the sqlalchemy function to add
    # data to tables. The function iterates through the list and take each item(dictionary) in the
    # list and convert it into the right format!
    post_map = map(create_post_model, posts_data)
    # The map funtion returns a mao object, need a list
    posts = list(post_map)

    session.add_all(posts)

    # Instead of using the above map function, we could hard code the posts like below! But the above method is better
    # session.add_all([models.Post(title="first title", content="first content", owner_id=test_user['id']),
    #                 models.Post(title="2nd title", content="2nd content", owner_id=test_user['id']), models.Post(title="3rd title", content="3rd content", owner_id=test_user['id'])])
    session.commit()

    posts = session.query(models.Post).all()
    return posts
