from pydantic import BaseModel
from typing import List

class QueueItemBase(BaseModel):
    track_id: str
    title: str
    artist: str

class QueueItemCreate(QueueItemBase):
    pass

class QueueItem(QueueItemBase):
    id: int
    votes: int
    class Config:
        orm_mode = True

class EventBase(BaseModel):
    name: str

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    code: str
    items: List[QueueItem] = []
    class Config:
        orm_mode = True
