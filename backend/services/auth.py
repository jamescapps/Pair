import jwt
from datetime import datetime, timedelta

from .user import UserService

from fastapi import HTTPException


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


class AuthService(object):
    def __init__(self, session, secret_key: str, token_expiration_in_minutes: int):
        self.session = session
        self.SECRET_KEY = secret_key
        self.TOKEN_EXPIRATION_IN_MINUTES = token_expiration_in_minutes
        self.user_svc = UserService(session)

    def generate_token(self, user_id: int) -> str:
        return jwt.encode(
            {
                "sub": user_id,
                "exp": datetime.utcnow()
                + timedelta(minutes=self.TOKEN_EXPIRATION_IN_MINUTES),
            },
            self.SECRET_KEY,
            algorithm="HS256",
        )

    def login(self, email: str, password: str) -> dict[str, str]:
        user = self.user_svc.get_user_by_email(email)

        if not user:
            raise HTTPException(status_code=401, detail="Invalid email")

        if not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid password")

        return {"access_token": self.generate_token(user.id), "token_type": "bearer"}

    def logout(self): ...

    def send_email_update_verification(self, email: str): ...

    def confirm_emai_update(self): ...
