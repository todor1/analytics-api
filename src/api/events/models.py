from typing import List, Optional
# from pydantic import BaseModel, Field
from sqlmodel import SQLModel, Field


class EventModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # id: int
    page: Optional[str] = ""
    description: Optional[str] = ""


class EventCreateSchema(SQLModel):
    page: str
    description: Optional[str] = Field(default="")


class EventUpdateSchema(SQLModel):
    description: str


# {"id": 12}

class EventListSchema(SQLModel):
    results: List[EventModel]
    count: int