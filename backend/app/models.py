from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    code = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    items = relationship("QueueItem", back_populates="event")

class QueueItem(Base):
    __tablename__ = "queue_items"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    track_id = Column(String, index=True)
    title = Column(String)
    artist = Column(String)
    votes = Column(Integer, default=0)
    event = relationship("Event", back_populates="items")
