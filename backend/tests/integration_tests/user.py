import pytest
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from src.models import Base, UserModel, VisibleFirstNameModel


# Setup for SQLite in-memory database for testing
@pytest.fixture(scope="module")
def engine():
    return create_engine("sqlite:///:memory:")


@pytest.fixture(scope="module")
def session(engine):
    """Session fixture to interact with the database."""
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def user1(session):
    user = UserModel(email="user1@example.com", password="password123")
    session.add(user)
    session.commit()
    return user


@pytest.fixture
def user2(session):
    user = UserModel(email="user2@example.com", password="password123")
    session.add(user)
    session.commit()
    return user


client = TestClient(app)


def test_show_first_name_endpoint(user1, user2, session):
    """Test the /show_first_name/ endpoint."""
    data = {
        "user_id": user1.id,
        "permission_granted_for_user_id": user2.id,
    }

    # Call the endpoint
    response = client.post("/show_first_name/", json=data)

    # Check the response status code and message
    assert response.status_code == 200
    assert response.json() == {"message": "First name visibility granted successfully"}

    # Verify that the record was added to the database
    visible_first_name = (
        session.query(VisibleFirstNameModel)
        .filter_by(user_id=user1.id, permission_granted_for_user_id=user2.id)
        .first()
    )
    assert visible_first_name is not None
    assert visible_first_name.user_id == user1.id
    assert visible_first_name.permission_granted_for_user_id == user2.id


def test_un_show_first_name_endpoint(user1, user2, session):
    """Test the /un_show_first_name/ endpoint."""
    # First, show the first name for user1 to user2
    data_show = {
        "user_id": user1.id,
        "permission_granted_for_user_id": user2.id,
    }
    client.post("/show_first_name/", json=data_show)

    # Now, un-show the first name for user2
    data_unshow = {
        "user_id": user1.id,
        "permission_revoked_for_user_id": user2.id,
    }

    response = client.post("/un_show_first_name/", json=data_unshow)

    # Check the response status code and message
    assert response.status_code == 200
    assert response.json() == {"message": "First name visibility revoked successfully"}

    # Verify that the record was removed from the database
    visible_first_name = (
        session.query(VisibleFirstNameModel)
        .filter_by(user_id=user1.id, permission_granted_for_user_id=user2.id)
        .first()
    )
    assert visible_first_name is None


def test_create_user(user1, session):
    """Test the /create_user/ endpoint."""
    data = {
        "email": "newuser@example.com",
        "password": "password123",
    }

    response = client.post("/create_user/", json=data)

    assert response.status_code == 200
    assert response.json() == {"message": "User created successfully"}

    # Verify the user is created in the database
    new_user = session.query(UserModel).filter_by(email="newuser@example.com").first()
    assert new_user is not None
    assert new_user.email == "newuser@example.com"


def test_edit_user(user1, session):
    """Test the /edit_user/ endpoint."""
    data = {
        "first_name": "New First Name",
        "about": "This is a new about section.",
    }

    response = client.post(f"/edit_user/{user1.id}/", json=data)

    assert response.status_code == 200
    assert response.json() == {"message": "User updated successfully"}

    # Verify that the user data has been updated in the database
    updated_user = session.query(UserModel).filter_by(id=user1.id).first()
    assert updated_user.first_name == "New First Name"
    assert updated_user.about == "This is a new about section."


def test_update_user_email(user1, session):
    """Test the /update_user_email/ endpoint."""
    data = {
        "new_email": "updatedemail@example.com",
    }

    response = client.post(f"/update_user_email/{user1.id}/", json=data)

    assert response.status_code == 200
    assert response.json() == {"message": "Email updated successfully"}

    # Verify that the user's email is updated in the database
    updated_user = session.query(UserModel).filter_by(id=user1.id).first()
    assert updated_user.email == "updatedemail@example.com"


def test_delete_user(user1, session):
    """Test the /delete_user/ endpoint."""
    data = {
        "user_id": user1.id,
    }

    response = client.post(f"/delete_user/{user1.id}/", json=data)

    assert response.status_code == 200
    assert response.json() == {"message": "User deleted successfully"}

    # Verify that the user is deleted from the database
    deleted_user = session.query(UserModel).filter_by(id=user1.id).first()
    assert deleted_user is None


def test_deactivate_account(user1, session):
    """Test the /deactivate_account/ endpoint."""
    data = {
        "user_id": user1.id,
    }

    response = client.post(f"/deactivate_account/{user1.id}/", json=data)

    assert response.status_code == 200
    assert response.json() == {"message": "Account deactivated successfully"}

    # Verify that the user's account is deactivated in the database
    deactivated_user = session.query(UserModel).filter_by(id=user1.id).first()
    assert deactivated_user.is_active is False


def test_suggest_usernames(user1, session):
    """Test the /suggest_usernames/ endpoint."""
    data = {
        "user_id": user1.id,
    }

    response = client.post(f"/suggest_usernames/{user1.id}/", json=data)

    assert response.status_code == 200
    assert "suggested_usernames" in response.json()
