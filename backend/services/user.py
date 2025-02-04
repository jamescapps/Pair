from sqlalchemy import delete,update
from sqlalchemy.orm import Session

from ..schema.profile import ProfileSchema
from ..models.user import UserModel
from .auth import AuthService

class UserService(object):
    def __init__(self, session: Session):
        self.session = session
        self.auth_svc = AuthService

    def get_user(self, user_id: int)-> UserModel:# -> Any:
        q = select(UserModel).where(UserModel.id == user_id)

        return self.session.execute(q).scalar_one()

    def create_user(self, profile_data: ProfileSchema):
        user = UserModel(
            username=profile_data.username,
            email=profile_data.email,
            first_name=profile_data.first_name,
            about=profile_data.about,
        )

        self.session.add(user)

    def edit_user(self, user_id: int,  profile_data: ProfileSchema):
        user = self.get_user(user_id)
        
        if profile_data.email is not None and user.email != profile_data.email:
            self.auth_svc.send_email_update_verification(profile_data.email)
        
        stmt = update(UserModel)
               .values(
                   first_name=profile_data.first_name,
                   about=profile_data.about,
                )
                .where(UserModel.id == user_id)
        
        self.session.execute(stmt)

    def update_user_email_address(self, user_id: int, new_email: str):
        stmt = update(UserModel)
                .values(email=new_email)
                .where(UserModel.id == user_id)
        
        self.session.execute(stmt)

    def delete_user(self, user_id):
        stmt = delete(UserModel).where(UserModel.id == user_id)

        self.session.execute(stmt)

    def deactivate_account(self, user_id):
        stmt = update(UserModel).values(is_active = False).where(UserModel.id == user_id)

        self.session.execute(stmt)
