from pydantic import BaseModel

class FilterUserByTelegramId(BaseModel):
    telegram_id: int
    