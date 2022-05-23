import pytest
from app.config import env_settings
from app import schemas
from jose import jwt


def test_correct_login(test_client, test_create_user):
    test_user_credentials = {"username": test_create_user["email"],
                             "password": test_create_user["password"]}
    response = test_client.post("/login/", data=test_user_credentials)
    assert response.status_code == 200
    response_token = schemas.AccessToken(**response.json())
    payload = jwt.decode(token=response_token.access_token, key=env_settings.SECRET_KEY,
                         algorithms=env_settings.ALGORITHM)
    user_id = payload.get("user_id")
    assert user_id == test_create_user["user_id"]
    assert response_token.token_type == "Bearer"


@pytest.mark.parametrize("email, password, status_code",
                             [("wrong@wrong.com", "password", 403),
                             ("test@test.com", "wrong", 403),
                             (None, "password", 422)])
def test_wrong_login(test_client, test_create_user, email, password, status_code):
    response = test_client.post("/login/", data={"username": email, "password": password})
    assert response.status_code == status_code


def test_root(test_client):
    response = test_client.get("/")
    assert response.json().get('message') == 'welcome to social town'
    assert response.status_code == 200


