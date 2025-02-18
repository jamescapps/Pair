import random
import string

from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

from ..models.user import UserModel
from ..models.visible_first_names import VisibleFirstNameModel
from ..schema.profile import ProfileSchema, SignUpSchema
from .auth import AuthService


class UserService(object):
    def __init__(self, session: Session) -> None:
        self.session = session
        self.auth_svc = AuthService

    def get_user(self, user_id: int) -> UserModel:
        q = select(UserModel).where(UserModel.id == user_id)

        return self.session.execute(q).scalar_one()

    def create_user(self, profile_data: SignUpSchema) -> None:
        user = UserModel(
            email=profile_data.email,
            password=profile_data.password,
        )

        self.session.add(user)

    def edit_user(self, user_id: int, profile_data: ProfileSchema) -> None:
        user = self.get_user(user_id)

        if profile_data.email is not None and user.email != profile_data.email:
            self.auth_svc.send_email_update_verification(profile_data.email)

        stmt = (
            update(UserModel)
            .values(
                first_name=profile_data.first_name,
                about=profile_data.about,
            )
            .where(UserModel.id == user_id)
        )

        self.session.execute(stmt)

    def update_user_email_address(self, user_id: int, new_email: str) -> None:
        stmt = update(UserModel).values(email=new_email).where(UserModel.id == user_id)

        self.session.execute(stmt)

    def delete_user(self, user_id: int) -> None:
        stmt = delete(UserModel).where(UserModel.id == user_id)

        self.session.execute(stmt)

    def deactivate_account(self, user_id: int) -> None:
        """Deactivates a given user_id's account. DOES NOT DELETE"""
        stmt = update(UserModel).values(is_active=False).where(UserModel.id == user_id)

        self.session.execute(stmt)

    def suggest_usernames(self, user_id: int) -> list[str]:
        """Suggests a series of usernames for the given user_id based on the users first name and/or email address"""
        user = self.get_user(user_id)

        base_username = (
            user.first_name.lower() if user.first_name else user.email.split("@")[0]
        )

        suggestions = set()

        # Generate some variations
        suggestions.add(base_username)
        suggestions.add(f"{base_username}{random.randint(10, 99)}")
        suggestions.add(f"{base_username}_{random.randint(100, 999)}")
        suggestions.add(f"{base_username}.{random.randint(1, 999)}")
        suggestions.add(f"{base_username}{random.choice(string.ascii_lowercase)}")

        return list(suggestions)

    def show_first_name(self, user_id: int, permission_granted_for_id: int) -> None:
        """Allow the permission_granted_for user to see the given user_id's first name"""
        visible_first_name = VisibleFirstNameModel(
            user_id=user_id, permission_granted_for_user_id=permission_granted_for_id
        )

        self.session.add(visible_first_name)

    def un_show_first_name(self, user_id: int, permission_revoked_for_id: int) -> None:
        """Un-show the first name of the given user id from the permission_revoked_for id"""
        stmt = delete(VisibleFirstNameModel).where(
            VisibleFirstNameModel.user_id == user_id,
            VisibleFirstNameModel.permission_granted_for_user_id
            == permission_revoked_for_id,
        )

        self.session.execute(stmt)
