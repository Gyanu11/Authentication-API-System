import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models.user import User


# Use a separate in-memory SQLite database for tests.
TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False,
)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    Base.metadata.create_all(bind=test_engine)

    with TestClient(app) as test_client:
        yield test_client

    Base.metadata.drop_all(bind=test_engine)


def test_register_user_successfully(client):
    response = client.post(
        "/api/auth/register",
        json={
            "email": "student@example.com",
            "full_name": "Ram Sharma",
            "password": "StrongPass123!",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == "student@example.com"
    assert data["full_name"] == "Ram Sharma"
    assert data["is_active"] is True

    # The API must not expose passwords or password hashes.
    assert "password" not in data
    assert "hashed_password" not in data


def test_register_duplicate_email(client):
    payload = {
        "email": "student@example.com",
        "full_name": "Ram Sharma",
        "password": "StrongPass123!",
    }

    first_response = client.post(
        "/api/auth/register",
        json=payload,
    )

    second_response = client.post(
        "/api/auth/register",
        json=payload,
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409


def test_register_with_invalid_email(client):
    response = client.post(
        "/api/auth/register",
        json={
            "email": "invalid-email",
            "full_name": "Ram Sharma",
            "password": "StrongPass123!",
        },
    )

    assert response.status_code == 422


def test_register_with_short_password(client):
    response = client.post(
        "/api/auth/register",
        json={
            "email": "student@example.com",
            "full_name": "Ram Sharma",
            "password": "short",
        },
    )

    assert response.status_code == 422