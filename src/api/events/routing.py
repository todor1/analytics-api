import os
from fastapi import APIRouter
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
@router.get("/")
def read_events() -> EventListSchema:
    # a bunch of items in a table
    return {
        "results": [
            {"id": 1}, {"id": 2}, {"id": 3}
        ],
        "count": 3
    }

# SEND DATA HERE
# create view
# POST /api/events/
@router.post("/")
def create_event(payload:EventCreateSchema) -> EventModel:
    # a bunch of items in a table
    data = payload.model_dump() # payload -> dict -> pydantic
    return {"id": 123, **data}


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
