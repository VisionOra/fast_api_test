from app import schemas
from jose import jwt
import pytest
from app.config import settings




def test_create_user(client):
    res = client.post("/users/", json={"email": "aadil2@gmail.com", "password": "fastapi"})
    
    new_user = schemas.UserCreateRespose(**res.json())
    assert new_user.email == "aadil2@gmail.com"
    assert res.status_code == 201

def test_login_user(test_user, client):
    res = client.post("/login", data={"username": test_user['email'] , "password": test_user['password']})
    login_res= schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id: str = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'fastapi', 403),
    ('aadil2@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'fastapi', 422),
    ('aadil2@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email , "password": password})
    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid Credentials'