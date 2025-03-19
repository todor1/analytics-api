from fastapi import APIRouter
from .schemas import EventSchema
router = APIRouter()


# /api/events/
@router.get("/")
def read_events():
    # a bunch of items in a table
    return {
        "results": [1,2,3]
    }


@router.get("/{event_id}")
def get_event(event_id:int) -> EventSchema:
    # a single row
    return {"id": event_id}