from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession 
from .base import BaseDAO
from .models import User, Region, Role, TaskStatus, TaskPriority, Task, ReferLink

class RegionDAO(BaseDAO[Region]):
    model = Region

class RoleDAO(BaseDAO[Role]):
    model = Role

    @classmethod
    async def seed(cls, self, session: AsyncSession):
        defaultRoles = [
            Role(
                id = 1,
                name = 'Admin',
                description = 'Administrator'
            ),
            Role(
                id = 2,
                name = 'Worker',
                description = 'Regular worker'
            )
        ]
        
        try:
            self.upsert()
            for role in defaultRoles:
                session.add(role)
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Ошибка при seed: {e}")
            raise e

class UserDAO(BaseDAO[User]):
    model = User

class TaskStatusDAO(BaseDAO[TaskStatus]):
    model = TaskStatus

class TaskPriorityDAO(BaseDAO[TaskPriority]):
    model = TaskPriority

class TaskDAO(BaseDAO[Task]):
    model = Task

class ReferDAO(BaseDAO[ReferLink]):
    model = ReferLink
