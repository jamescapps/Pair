from pydantic import BaseModel


class RegistrationSchema(BaseModel):
    email: str
    password1: str
    password2: str
