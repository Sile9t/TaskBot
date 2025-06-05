from datetime import datetime, timedelta
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
    # chat_id: Mapped[Optional[int]]

    users: Mapped[list["User"]] = relationship("User", back_populates="region", lazy='select')
    
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="region", lazy='select')
    
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
    
    users: Mapped[list["User"]] = relationship("User", back_populates="role", lazy='select')

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
    
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="status", lazy='select')
    
    @declared_attr
    def __tablename__(cls) -> str:
        return "task_statuses"

# #
# Task priority class describes priority of the task
# #
class TaskPriority(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    value: Mapped[int] = mapped_column(Integer, unique=True)
    title: Mapped[str]
    description: Mapped[Optional[str]]
    
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="priority", lazy='select')

    @declared_attr
    def __tablename__(cls) -> str:
        return "task_priorities"

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


# task_user_table = Table(
#     "task_user_table",
#     Base.metadata,
#     Column('user_id', ForeignKey('users.id')),
#     Column('task_id', ForeignKey('tasks.id')),
# )

# class ReferLink(Base):
#     user_id: Mapped[int]
#     link: Mapped[str]