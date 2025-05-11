from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
import qrcode
from io import BytesIO
from . import crud, schemas, database
import os

router = APIRouter()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/events/", response_model=schemas.Event)
def create_event(evt: schemas.EventCreate, db: Session = Depends(get_db)):
    return crud.create_event(db, evt)

@router.get("/events/{code}", response_model=schemas.Event)
def read_event(code: str, db: Session = Depends(get_db)):
    db_evt = crud.get_event_by_code(db, code)
    if not db_evt:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_evt

@router.get("/events/{code}/qr")
def get_qr(code: str):
    link = f"https://yourdomain.com/guest/{code}"
    img = qrcode.make(link)
    buf = BytesIO()
    img.save(buf)
    return Response(content=buf.getvalue(), media_type="image/png")

@router.post("/events/{code}/items/", response_model=schemas.QueueItem)
def add_track(code: str, item: schemas.QueueItemCreate, db: Session = Depends(get_db)):
    evt = crud.get_event_by_code(db, code)
    if not evt:
        raise HTTPException(404, "Event not found")
    return crud.add_item(db, evt.id, item)

@router.post("/items/{item_id}/vote", response_model=schemas.QueueItem)
def vote(item_id: int, db: Session = Depends(get_db)):
    return crud.vote_item(db, item_id)

# Tidal search proxy (requires TIDAL_API_KEY env var)
@router.get("/search/")
async def search(q: str):
    from aiohttp import ClientSession
    API = 'https://api.tidal.com/v1/search'
    params = {'query': q, 'types': 'TRACK', 'limit': 10, 'countryCode':'US'}
    headers = {'Authorization': f"Bearer {os.getenv('TIDAL_API_KEY')}"}
    async with ClientSession() as session:
        async with session.get(API, params=params, headers=headers) as resp:
            data = await resp.json()
    return [{ 'track_id': t['id'], 'title': t['title'], 'artist': ', '.join(a['name'] for a in t['artists'])} for t in data['tracks']['items']]
