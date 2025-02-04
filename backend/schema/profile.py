from pydantic import BaseModel


class ProfileSchema(BaseModel):
    username: str
    password: str
    email: str
    first_name: str
    about: str
