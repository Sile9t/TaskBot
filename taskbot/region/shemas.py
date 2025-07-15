from pydantic import BaseModel

class RegionChatIdFilter(BaseModel):
    chat_id: int

class FilterRegionById(BaseModel):
    id: int
