import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from ..app.main import app
from services.registration import RegisterationService

# Create a test client for FastAPI
client = TestClient(app)

# Mock database session
mock_db = MagicMock()

# Mock UserService with our fake database session
svc = RegisterationService(mock_db)


@pytest.fixture
def reset_mocks():
    """Reset mock call history before each test."""
    mock_db.reset_mock()
    svc.reset_mock()


def test_user_signup_success(reset_mocks):
    """Test successful user signup."""
    svc.user_exists.return_value = False

    response = client.post(
        "/",
        json={
            "email": "testuser@example.com",
            "password": "SecurePass123!",
            "confirm_password": "SecurePass123!",
        },
    )

    assert response.status_code == 200

    svc.user_exists.assert_called_once_with("testuser@example.com")
    svc.create_user.assert_called_once()


def test_user_signup_password_mismatch(reset_mocks):
    """Test signup failure when passwords do not match."""
    response = client.post(
        "/",
        json={
            "email": "testuser@example.com",
            "password": "SecurePass123!",
            "confirm_password": "WrongPass",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Passwords do not match"
    svc.create_user.assert_not_called()


def test_user_signup_existing_user(reset_mocks):
    """Test signup failure when user already exists."""
    svc.user_exists.return_value = True

    response = client.post(
        "/",
        json={
            "email": "existinguser@example.com",
            "password": "SecurePass123!",
            "confirm_password": "SecurePass123!",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "User already exists"
    svc.create_user.assert_not_called()
