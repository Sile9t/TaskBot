from pydantic import BaseModel, Field

class UserTelegramId(BaseModel):
    telegram_id: int

class UserRoleId(BaseModel):
    role_id: int

class UserTelegramAndRoleIds(UserTelegramId):
    role_id: int