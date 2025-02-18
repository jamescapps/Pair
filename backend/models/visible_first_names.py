from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class VisibleFirstNameModel(Base):
    __tablename__ = "visible_first_name"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    permission_granted_for_user_id = Column(
        Integer, ForeignKey("user.id"), nullable=False
    )
    created_at = Column(DateTime, default=func.now(), nullable=False)

    user = relationship(
        "UserModel", foreign_keys=[user_id], backref="visible_first_name"
    )
    permission_granted_for_user = relationship(
        "UserModel",
        foreign_keys=[permission_granted_for_user_id],
        backref="granted_visible_first_name",
    )

    def __repr__(self) -> str:
        return f"<VisibleFirstNameModel(user_id={self.user_id}, permission_granted_for_user_id={self.permission_granted_for_user_id}, created_at={self.created_at})>"
