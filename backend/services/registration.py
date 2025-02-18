from fastapi import HTTPException
from models.user import UserModel
from passlib.context import CryptContext
from services.user import UserService
from sqlalchemy import exists, select
from sqlalchemy.orm import Session

from backend.schema.registration import RegistrationSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _passwords_match(password1, password2) -> bool:
    return password1 == password2


class RegisterationService(object):
    def __init__(self, session: Session):
        self.session = session
        self.user_svc = UserService(session)

    def _hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def _user_already_exists(self, email: str) -> bool:
        q = select(exists().where(UserModel.email == email))

        return self.session.execute(q).scalar()

    def sign_up(self, user_info: RegistrationSchema):
        if not _passwords_match(user_info.password1, user_info.password2):
            raise HTTPException(status_code=400, detail="Passwords do not match")

        if self._user_already_exists(user_info.email):
            raise HTTPException(
                status_code=400,
                detail="An account with that email address already exists.",
            )

        self.user_svc.create_user(
            user_info.email, self._hash_password(user_info.password2)
        )
