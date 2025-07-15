from pydantic import BaseModel

class FilterRecordById(BaseModel):
    id: int
