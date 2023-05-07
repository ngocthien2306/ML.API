from sqlalchemy import Column, Unicode, BigInteger, Boolean, Integer, String,ForeignKey
from sqlalchemy.orm import relationship
from core.db import Base
from core.db.mixins import TimestampMixin


class Track(Base):
    __tablename__ = "tblTrack"
    Id = Column(Integer, primary_key=True, index=True)
    trackNumber = Column(Integer)
    vehicleId = Column(Integer, ForeignKey('tblVehicle.id'))
    startTime = Column(String(20))
    endTime = Column(String(20), default=False)
    fee = Column(String(20), default=False)
    siteId= Column(Integer, default=True)
    locationX = Column(String(20), default=False)
    locationY = Column(String(20), default=False)
    userId = Column(Integer)
    detectInFace = Column(String(250), default=True) 
    detectOutFace = Column(String(250), default=False) 
    plateIn = Column(String(250), default=True)
    plateOut = Column(String(250), default=False)
    vehicle = relationship("Vehicle", back_populates="tracks")
