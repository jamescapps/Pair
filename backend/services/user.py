from sqlalchemy.orm import Session
from ..schema.profile import ProfileSchema
from ..models.user import UserModel

class UserService(object):
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, profile_data: ProfileSchema):
        user = UserModel(
            username=profile_data.username,
            email=profile_data.email,
            first_name=profile_data.first_name,
            about=profile_data.about,
        )

        self.session.add(user)

    def edit_user(self, profile_data: ProfileSchema):
        ...

    def delete_user(self, user_id):
        ...

    def deactivate_account(self, user_id):
        ...
