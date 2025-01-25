from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class Gender(enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    NON_BINARY = "NON_BINARY"


class UserModel(Base):
    __tablename__ = "users"  

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True,nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    first_name = Column(String, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    image_1 = Column(String)
    image_2 = Column(String)
    image_3 = Column(String)
    about = Column(String)

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"
