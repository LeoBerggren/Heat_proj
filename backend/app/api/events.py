from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.event import Event
from app.api.schemas import EventCreate, EventRead

router = APIRouter()

# CREATE
@router.post("/events", response_model=EventRead)
def create_event(data: EventCreate, db: Session = Depends(get_db)):
    event = Event(
        name=data.name,
        location=data.location,
        start_time=data.start_time,
        end_time=data.end_time
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

# READ ALL
@router.get("/events", response_model=list[EventRead])
def list_events(db: Session = Depends(get_db)):
    return db.query(Event).all()

# READ ONE
@router.get("/events/{event_id}", response_model=EventRead)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

# UPDATE
@router.put("/events/{event_id}", response_model=EventRead)
def update_event(event_id: int, data: EventCreate, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    event.name = data.name
    event.location = data.location
    event.start_time = data.start_time
    event.end_time = data.end_time

    db.commit()
    db.refresh(event)
    return event

# DELETE
@router.delete("/events/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    db.delete(event)
    db.commit()
    return {"status": "deleted"}
