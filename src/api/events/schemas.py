from typing import List
from pydantic import BaseModel


class EventSchema(BaseModel):
    id: int


# {"id": 12}

class EventListSchema(BaseModel):
    results: List[EventSchema]
    count: int