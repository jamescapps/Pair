from typing import Generator, List
from unittest.mock import MagicMock

import pytest
from sqlalchemy.exc import NoResultFound

from ...models.user import UserModel
from ...schema.profile import ProfileSchema
from ...schema.registration import RegistrationSchema
from ...services.user import UserService


@pytest.fixture
def mock_session() -> MagicMock:
    return MagicMock()


@pytest.fixture
def user_service(mock_session: MagicMock) -> UserService:
    return UserService(mock_session)


@pytest.fixture
def mock_user() -> UserModel:
    return UserModel(
        id=1,
        first_name="John",
        email="john.doe@example.com",
        password="hashed_password",
    )


def test_get_user_found(
    user_service: UserService, mock_session: MagicMock, mock_user: UserModel
) -> None:
    """Test retrieving a user successfully"""
    mock_session.execute.return_value.scalar_one.return_value = mock_user

    user = user_service.get_user(1)

    assert user == mock_user
    mock_session.execute.assert_called_once()


def test_get_user_not_found(user_service: UserService, mock_session: MagicMock) -> None:
    """Test getting a user that doesn't exist should raise an exception"""
    mock_session.execute.return_value.scalar_one.side_effect = NoResultFound

    with pytest.raises(NoResultFound):
        user_service.get_user(999)


def test_create_user(user_service: UserService, mock_session: MagicMock) -> None:
    """Test creating a user"""
    profile_data = RegistrationSchema(
        email="test@example.com", password="securepassword"
    )

    user_service.create_user(profile_data)

    mock_session.add.assert_called_once()


def test_edit_user(
    user_service: UserService, mock_session: MagicMock, mock_user: UserModel
) -> None:
    """Test editing a user's profile"""
    profile_data = ProfileSchema(first_name="Johnny", about="New bio", email=None)
    user_service.get_user = MagicMock(return_value=mock_user)

    user_service.edit_user(1, profile_data)

    mock_session.execute.assert_called_once()


def test_edit_user_email_update(
    user_service: UserService, mock_session: MagicMock, mock_user: UserModel
) -> None:
    """Test editing a user's email triggers email verification"""
    user_service.get_user = MagicMock(return_value=mock_user)
    user_service.auth_svc.send_email_update_verification = MagicMock()

    profile_data = ProfileSchema(
        first_name="John", about="Same bio", email="new.email@example.com"
    )

    user_service.edit_user(1, profile_data)

    user_service.auth_svc.send_email_update_verification.assert_called_once_with(
        "new.email@example.com"
    )
    mock_session.execute.assert_called_once()


def test_update_user_email_address(
    user_service: UserService, mock_session: MagicMock
) -> None:
    """Test updating a user's email"""
    user_service.update_user_email_address(1, "new.email@example.com")

    mock_session.execute.assert_called_once()


def test_delete_user(user_service: UserService, mock_session: MagicMock) -> None:
    """Test deleting a user"""
    user_service.delete_user(1)

    mock_session.execute.assert_called_once()


def test_deactivate_account(user_service: UserService, mock_session: MagicMock) -> None:
    """Test deactivating a user account"""
    user_service.deactivate_account(1)

    mock_session.execute.assert_called_once()


def test_suggest_usernames_with_first_name(user_service: UserService) -> None:
    """Test username suggestions when a first name is available"""
    mock_user = UserModel(id=1, first_name="John", email="john.doe@example.com")
    user_service.get_user = MagicMock(return_value=mock_user)

    suggestions: List[str] = user_service.suggest_usernames(1)

    assert len(suggestions) > 0
    assert any(s.startswith("john") for s in suggestions)


def test_suggest_usernames_with_email(user_service: UserService) -> None:
    """Test username suggestions when first name is unavailable"""
    mock_user = UserModel(id=2, first_name=None, email="jane.doe@example.com")
    user_service.get_user = MagicMock(return_value=mock_user)

    suggestions: List[str] = user_service.suggest_usernames(2)

    assert len(suggestions) > 0
    assert any(s.startswith("jane.doe") for s in suggestions)


def test_suggest_usernames_raises_if_user_not_found(user_service: UserService) -> None:
    """Test that NoResultFound is raised when user doesn't exist"""
    user_service.get_user = MagicMock(side_effect=NoResultFound)

    with pytest.raises(NoResultFound):
        user_service.suggest_usernames(3)
