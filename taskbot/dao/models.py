from datetime import datetime, timedelta, date
from typing import Annotated, List, Optional
from sqlalchemy import String, Boolean, Integer, TIMESTAMP, func, ForeignKey, text, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship, declared_attr

from .database import Base, DeclarativeBase


# #
# Region class intepreting region separation of users 
# for processing task for specified region
# #
class Region(Base):
    name: Mapped[str]
    description: Mapped[Optional[str]]
    chat_id: Mapped[Optional[int]]

    users: Mapped[List["User"]] = relationship("User", back_populates="region", lazy='select')
    
    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="region", lazy='select')

    def getNameAndIdTuple(self):
        return (self.name, self.id)


# #
# Role class determines user right
#
# Possible roles:
#   1. administrator (all rights)
#   2. lead (all rights in case of his region)
#   3. employee (can only change tasks state)
# #
class Role(Base):
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[Optional[str]]
    
    users: Mapped[List["User"]] = relationship("User", back_populates="role", lazy='select')

    def getNameAndIdTuple(self):
        return (self.name, self.id)


task_user_table = Table(
    "task_user_table",
    Base.metadata,
    Column('user_id', ForeignKey('users.id')),
    Column('task_id', ForeignKey('tasks.id')),
)


# #
# User class describes system user
# #
class User(Base):
    first_name: Mapped[str]
    last_name: Mapped[str]
    telegram_id: Mapped[int] = mapped_column(unique=True)
    
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'))
    role: Mapped["Role"] = relationship("Role",back_populates="users", foreign_keys="[User.role_id]", lazy="joined")
    
    region_id: Mapped[Optional[int]] = mapped_column(ForeignKey("regions.id"))
    region: Mapped[Optional["Region"]] = relationship("Region", back_populates="users", foreign_keys="[User.region_id]", lazy="joined")

    refer_links: Mapped[List["ReferLink"]] = relationship("ReferLink", back_populates="user")

    created_tasks: Mapped[List["Task"]] = relationship("Task", back_populates="creator", lazy="joined")
    
    perform_tasks: Mapped[List["Task"]] = relationship(secondary=task_user_table, back_populates="performers", lazy="selectin")

    def getRoleTitleAndFullNameCaption(self):
        return f"{self.role.name} {self.first_name} {self.last_name}"
    
    def getRoleTitleFullNameAndIdTuple(self):
        return (self.getRoleTitleAndFullNameCaption(), self.id)
    
    def getFullCaption(self):
        return { 
            "id": str(self.id), 
            "telegram_id": self.telegram_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "role": self.role.name,
            "region": self.region.name if self.region else None,
            'updated_at': self.updated_at,
            'created_at': self.created_at
        }
    

# #
# Task status class describes status of the task
# 
# Possible statuses:
#   1. done
#   2. in work
#   3. created
# #
class TaskStatus(Base):    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[Optional[str]]
    
    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="status", lazy='select')
    
    @declared_attr
    def __tablename__(cls) -> str:
        return "task_statuses"
    
    def getTitleAndIdTuple(self):
        return (self.title, self.id)


# #
# Task priority class describes priority of the task
# #
class TaskPriority(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    value: Mapped[int] = mapped_column(Integer, unique=True)
    title: Mapped[str]
    description: Mapped[Optional[str]]
    
    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="priority", lazy='select')

    @declared_attr
    def __tablename__(cls) -> str:
        return "task_priorities"
    
    def getTitleAndIdTuple(self):
        return (self.title, self.id)


# #
# Task class describes task as an object wich store information
# about task, his status, priority, start and end date, and so on
# #
class Task(Base):
    title: Mapped[str]
    description: Mapped[Optional[str]]
    startline: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    deadline: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.today() + timedelta(hours=24))
    # Link to form wich processing due the task
    # form_url: Mapped[Optional[String]]
    # Expected result of the task
    # result: Mapped[Optional[String]]
    # is task can be processed by bot
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default=text("'true'"))
    
    status_id: Mapped[int] = mapped_column(ForeignKey("task_statuses.id"))
    status: Mapped["TaskStatus"] = relationship("TaskStatus", back_populates="tasks", foreign_keys="[Task.status_id]", lazy="joined")
    
    priority_id: Mapped[int] = mapped_column(ForeignKey("task_priorities.id"))
    priority: Mapped["TaskPriority"] = relationship("TaskPriority", back_populates="tasks", foreign_keys="[Task.priority_id]", lazy="joined")
    
    region_id: Mapped[int] = mapped_column(ForeignKey("regions.id"))
    region: Mapped["Region"] = relationship("Region", back_populates="tasks", foreign_keys="[Task.region_id]", lazy="joined")
    
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    creator: Mapped["User"] = relationship("User", back_populates="created_tasks", lazy='selectin')

    performers: Mapped[List["User"]] = relationship("User", secondary=task_user_table, back_populates="perform_tasks", lazy="selectin")

    def getPerformersCaption(self):
        return ",\n".join(user.getRoleTitleAndFullNameCaption() for  user in self.performers) or '—'

    def getTitleAndIdTuple(self):
        return (self.title, self.id)

    def getFullCaption(self):
        return {
                "id": str(self.id), 
                "title": self.title,
                "description": self.description,
                "startline": self.startline,
                "deadline": self.deadline,
                "is_active": 'Да' if self.is_active else 'Нет',
                "status": self.status.title,
                "priority": self.priority.title,
                "region": self.region.name if self.region else None,
                "performers": self.getPerformersCaption(),
                'updated_at': self.updated_at,
                'created_at': self.created_at
            }
    
    def toBeautifiedText(self):
        days_left = (self.deadline.date() - date.today()).days
        
        days_left_text = 'сегодня крайний срок'
        if (days_left < 0):
            days_left_text = f"на {((-1) * days_left)} дней просрочена"
        elif (days_left > 0):
            days_left_text = f"{days_left} дней осталось"

        performersCaption = self.getPerformersCaption()
        return (
                f"📌 <b>{self.title}</b> (ID: {self.id})\n"
                f"📝 Описание: {self.description or 'Без описания'}\n"
                f"🗓 Сроки: с {self.startline.strftime('%d.%m.%Y')} по {self.deadline.strftime('%d.%m.%Y')} ({days_left_text})\n"
                f"✔ Статус: {self.status.title}\n"
                f"🔥 Приоритет: {self.priority.title}\n"
                f"🌍 Регион: {self.region.name}\n"
                f"👷 Исполнители:\n{performersCaption}\n"
            )


class ReferLink(Base):
    chat_id: Mapped[int]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates='refer_links')
    link: Mapped[str]


    @declared_attr
    def __tablename__(cls) -> str:
        return "refer_links"