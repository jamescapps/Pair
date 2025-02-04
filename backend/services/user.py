from sqlalchemy import delete,update
from sqlalchemy.orm import Session

from ..schema.profile import ProfileSchema
from ..models.user import UserModel
from .auth import AuthService

class UserService(object):
    def __init__(self, session: Session):
        self.session = session
        self.auth_svc = AuthService

    def create_user(self, profile_data: ProfileSchema):
        user = UserModel(
            username=profile_data.username,
            email=profile_data.email,
            first_name=profile_data.first_name,
            about=profile_data.about,
        )
# test
        self.session.add(user)

    def edit_user(self, profile_data: ProfileSchema):
        stmt = update(UserModel)
               .values(
                   first_name=profile_data.first_name,
                   about=profile_data.about,
                   )

    def delete_user(self, user_id):
        stmt = delete(UserModel).where(UserModel.id == user_id)

        self.session.execute(stmt)

    def deactivate_account(self, user_id):
        stmt = update(UserModel).values(is_active = False).where(UserModel.id == user_id)

        self.session.execute(stmt)
