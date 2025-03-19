from pydantic import BaseModel


class EventSchema(BaseModel):
    id: int


# {"id": 12}