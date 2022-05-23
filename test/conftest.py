from fastapi.testclient import TestClient
from app.main import app
from app.config import env_settings
from app.database import get_db
from app.models import Base
from app import schemas
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


test_db_url = f"{env_settings.DATABASE_TYPE}://" \
                          f"{env_settings.DATABASE_USER}:" \
                          f"{env_settings.DATABASE_PASSWORD}@" \
                          f"{env_settings.DATABASE_HOST}:" \
                          f"{env_settings.DATABASE_PORT}/{env_settings.DATABASE_NAME}_test"

engine = create_engine(test_db_url)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def test_client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_create_user(test_client):
    credential_params = {
        "email": "test@test.com",
        "password": "password"
    }
    response = test_client.post("/users/", json=credential_params)
    assert response.status_code == 201

    # validate with pydantic schema
    test_user = schemas.UserOut(**response.json())

    # add password to the user data to be returned
    return_user = response.json()
    return_user["password"] = credential_params["password"]
    return return_user
