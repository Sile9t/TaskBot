from pydantic import BaseModel, Field

class UserTelegramId(BaseModel):
    telegram_id: int

class UserRoleId(BaseModel):
    role_id: int

class UserTelegramAndRoleIds(UserTelegramId):
    role_id: int

class ReferLinkFilterByChatAndUserIds(BaseModel):
    chat_id: int
    user_id: int