from sqlalchemy import Column, Unicode, BigInteger, Boolean

from core.db import Base
from core.db.mixins import TimestampMixin


class User(Base):
    __tablename__ = "tblUser"

    UserId = Column(Unicode(255), primary_key=True, autoincrement=True)
    Password = Column(Unicode(255), nullable=False)
    Email = Column(Unicode(255), nullable=False, unique=True)
    UserName = Column(Unicode(255), nullable=False, unique=True)
    UserType = Column(Unicode(255), default=False)
