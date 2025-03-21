import os
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from sqlalchemy import func
from timescaledb.hyperfunctions import time_bucket
from datetime import datetime, timedelta, timezone
from api.db.session import get_session

from .models import (
    EventModel, 
    EventBucketSchema, 
    EventCreateSchema,
    EventUpdateSchema,
    get_utc_now
)
router = APIRouter()

DEFAULT_LOOKUP_PAGES = ['/about', '/contact', '/pages', '/pricing', 'pricing']

# Get data here
# List View
# GET /api/events/
@router.get("/", response_model=List[EventBucketSchema])
def read_events(
        duration: str = Query(default="1 day"),
        pages: List = Query(default=None),
        session: Session = Depends(get_session)
    ):
    # a bunch of items in a table
    bucket = time_bucket(duration, EventModel.time)
    lookup_pages = pages if isinstance(pages, list) and len(pages) > 0 else DEFAULT_LOOKUP_PAGES
    query = (
        select(
            bucket.label('bucket'),
            EventModel.page.label('page'),
            func.count().label('count')
        )
        .where(
            EventModel.page.in_(lookup_pages)
        )
        .group_by(
            bucket,
            EventModel.page,
        )
        .order_by(
            bucket,
            EventModel.page,
        )
    )
    results = session.exec(query).fetchall()
    return results

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
@router.get("/{event_id}", response_model=EventModel)
def get_event(event_id:int, session: Session = Depends(get_session)):
    # a single row
    query = select(EventModel).where(EventModel.id == event_id)
    result = session.exec(query).first()
    if not result:
        raise HTTPException(status_code=404, detail="Event not found")
    return result


# Update this data
# PUT /api/events/12
@router.put("/{event_id}", response_model=EventModel)
def update_event(
        event_id:int, 
        payload:EventUpdateSchema, 
        session: Session = Depends(get_session)):
    # a single row
    query = select(EventModel).where(EventModel.id == event_id)
    obj = session.exec(query).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Event not found")
    data = payload.model_dump()
    for k, v in data.items():
        setattr(obj, k, v)
    obj.updated_at = get_utc_now()
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj



# @router.delete("/{event_id}")
# def get_event(event_id:int) -> EventModel:
#     # a single row
#     return {"id": event_id}
