from pydantic import BaseModel

class RegionChatIdFilter(BaseModel):
    chat_id: int