import os
from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from api.db.session import get_session

from .models import (
    EventModel, 
    EventListSchema, 
    EventCreateSchema,
    EventUpdateSchema
)
router = APIRouter()


# Get data here
# List View
# GET /api/events/
@router.get("/", response_model=EventListSchema)
def read_events(session: Session = Depends(get_session)):
    # a bunch of items in a table
    query = select(EventModel).order_by(EventModel.id.asc()).limit(10)
    results = session.exec(query).all()
    return {
        "results": results,
        "count": len(results)
    }

# SEND DATA HERE
# create view
# POST /api/events/
@router.post("/", response_model=EventModel)
def create_event(
        payload:EventCreateSchema, 
        session: Session = Depends(get_session)):
    # a bunch of items in a table
    data = payload.model_dump() # payload -> dict -> pydantic
    obj = EventModel.model_validate(data)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


# GET /api/events/12
@router.get("/{event_id}")
def get_event(event_id:int) -> EventModel:
    # a single row
    return {"id": event_id}


# Update this data
# PUT /api/events/12
@router.put("/{event_id}")
def update_event(event_id:int, payload:EventUpdateSchema) -> EventModel:
    # a single row
    data = payload.model_dump()
    return {"id": event_id, **data}



# @router.delete("/{event_id}")
# def get_event(event_id:int) -> EventModel:
#     # a single row
#     return {"id": event_id}
