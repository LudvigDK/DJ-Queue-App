import uuid
from sqlalchemy.orm import Session
from . import models, schemas

def create_event(db: Session, evt: schemas.EventCreate):
    code = uuid.uuid4().hex[:6]
    db_evt = models.Event(name=evt.name, code=code)
    db.add(db_evt)
    db.commit()
    db.refresh(db_evt)
    return db_evt

def get_event_by_code(db: Session, code: str):
    return db.query(models.Event).filter(models.Event.code == code).first()

def list_events(db: Session):
    return db.query(models.Event).all()

def add_item(db: Session, event_id: int, item: schemas.QueueItemCreate):
    db_item = models.QueueItem(event_id=event_id, **item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def vote_item(db: Session, item_id: int):
    item = db.query(models.QueueItem).get(item_id)
    item.votes += 1
    db.commit()
    return item
