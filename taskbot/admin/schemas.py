from pydantic import BaseModel, Field

class UserTelegramId(BaseModel):
    telegram_id: int