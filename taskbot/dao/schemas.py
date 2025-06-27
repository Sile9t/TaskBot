from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class RegionDtoBase(BaseModel):
    name: str
    description: Optional[str]
    # lead_id: Optional[int]

    model_config = ConfigDict(from_attributes=True)

class RegionDto(RegionDtoBase):
    id: int = Field(frozen=True)

class RoleDtoBase(BaseModel):
    name: str
    description: Optional[str]

    model_config = ConfigDict(from_attributes=True)

class RoleDto(RoleDtoBase):
    id: int = Field(frozen=True)
    

class UserDtoBase(BaseModel):
    first_name: str
    last_name: str
    telegram_id: int
    role_id: int
    region_id: Optional[int]

class UserDto(UserDtoBase):
    id: int = Field(frozen=True)

    model_config = ConfigDict(from_attributes=True)


class TaskStatusDtoBase(BaseModel):
    title: str
    description: Optional[str]

    model_config = ConfigDict(from_attributes=True)

class TaskStatusDto(TaskStatusDtoBase):
    id: int = Field(frozen=True)


class TaskPriorityDtoBase(BaseModel):
    value: int
    title: str
    description: Optional[str]

    model_config = ConfigDict(from_attributes=True)

class TaskPriorityDto(TaskPriorityDtoBase):
    id: int = Field(frozen = True)


class TaskDtoBase(BaseModel):
    title: str
    description: Optional[str]
    startline: datetime = datetime.now
    deadline: datetime = datetime.now()
    is_active: bool = True

    status_id: int
    priority_id: int
    region_id: int
    creator_id: int

    model_config = ConfigDict(from_attributes=True)

class TaskDto(TaskDtoBase):
    id: int = Field(frozen=True)


class ReferDtoBase(BaseModel):
    chat_id: int
    user_id: int
    link: str

class ReferDto(ReferDtoBase):
    id: int = Field(frozen=True)