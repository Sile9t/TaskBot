from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class RegionDtoBase(BaseModel):
    name: str
    description: Optional[str]
    # lead_id: Optional[int]

    model_config = ConfigDict(from_attributes=True)

class RegionDto(RegionDtoBase):
    id: int = Field(frozen = True)

class RoleDtoBase(BaseModel):
    name: str
    description: Optional[str]

    model_config = ConfigDict(from_attributes=True)

class RoleDto(RoleDtoBase):
    id: int = Field(frozen = True)
    

class UserDtoBase(BaseModel):
    first_name: str
    last_name: str
    telegram_id: int
    role_id: int
    region_id: Optional[int]

class UserDto(UserDtoBase):
    id: int = Field(frozen = True)

    model_config = ConfigDict(from_attributes=True)


class TaskStatusDto(BaseModel):
    id: int = Field(frozen = True)
    title: str
    description: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class TaskPriorityDto(BaseModel):
    id: int = Field(frozen = True)
    value: int
    title: str
    description: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class TaskDto(BaseModel):
    id: int = Field(frozen = True)
    title: str
    description: Optional[str]
    startline: datetime = datetime.now
    deadlline:datetime = (datetime.now() + timedelta(hours=24))
    is_active: bool = True

    status_id: int
    status: Optional[TaskStatusDto]
    priority_id: int
    priority: Optional[TaskPriorityDto]
    region_id: int
    region: Optional[RegionDto]

    model_config = ConfigDict(from_attributes=True)

