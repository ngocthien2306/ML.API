from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,LargeBinary
from sqlalchemy.orm import relationship

from core.db import Base


class UserPhoto(Base):
    __tablename__ = "tblUserPhoto"
    UserPhotoNo = Column(Integer, primary_key=True, index=True, autoincrement=True)
    UserID =Column(String(20), default=True)
    TakenPhoto =Column(LargeBinary, default=True)
    IdCardPhoto = Column(LargeBinary, default=False)
