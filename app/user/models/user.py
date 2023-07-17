from sqlalchemy import Column, Unicode, BigInteger, Boolean, Integer,String,Boolean,DateTime,Text,Float

from core.db import Base
from core.db.mixins import TimestampMixin


class User(Base):
    __tablename__ = "tblUser"

    UserId = Column(Unicode(255), primary_key=True, autoincrement=True)
    Password = Column(Unicode(255), nullable=False)
    Email = Column(Unicode(255), nullable=False, unique=True)
    UserName = Column(Unicode(255), nullable=False, unique=True)
    UserType = Column(Unicode(255), default=False)
class Device(Base):
    __tablename__ = "tblStoreDevice"
    StoreDeviceNo = Column(Integer, primary_key=True, autoincrement=True)
    StoreNo = Column(Integer,default=True)
    DeviceName = Column(String(20), default=True)
    DeviceType = Column(String(6), default=True)
    DeviceKeyNo = Column(String(20), default=True)
    DevicePublicIP = Column(String(15), default=True)
    DeviceUsePort= Column(Integer, default=True)
    DeviceStatus = Column(Boolean, default=True)
    RDPPath = Column(String(200), default=False)
    RegistUserId = Column(String(50), default=True)
    RegistDate = Column(DateTime, default=True)
    DeviceKey = Column(Unicode(255), default=True)
    ListDeviceKeyNo = Column(Text, default=True)
    Network = Column(String(50), default=True)
    Threshold = Column(Float, default=True)