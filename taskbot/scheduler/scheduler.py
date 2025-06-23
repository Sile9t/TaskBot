from loguru import logger
from datetime import datetime, timedelta
from aiogram import Bot, BaseMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from taskbot.dao.models import Task
from taskbot.dao.dao import TaskDAO
from taskbot.dao.session_maker import connection

class NotificationsForTaskPerformers():
    def __init__(self, bot: Bot, session: AsyncSession, task_id: int):
        self.bot = bot
        self.session = session
        self.task_id = task_id

    async def __call__(self, *args, **kwds):
        logger.info(f"Отправка уведомлений иполнителям для задачи#{self.task_id}")
        task = await TaskDAO.find_one_or_none_by_id(self.session, self.task_id)
        remainerTime = task.deadline - datetime.now()

        taskDict = task.getFullCaption()
        taskInfo = ''
        for key, value in taskDict.items():
            taskInfo += f"{key}: {value}\n"

        text = f"До истечения срока задачи {task.title} осталось {remainerTime.days} дней \nДетали задачи: \n{taskInfo}"

        for user in task.performers:
            try:
                logger.info(f"Попытка отправить уведомление пользователю #{user.id}")
                chatId = f"{user.id}{user.id}"
                self.bot.send_message(chatId,text)
            except Exception as e:
                logger.error(f"Ошибка при отправке уведомление по задаче пользователю#{user.id} :{e}")        
        
        logger.info(f"Уведомления исполнителям для задачи#{self.task_id} отправлены")
        
        return True

class TaskNotifier():    
    def __init__(self, bot: Bot, session: AsyncSession,scheduler: AsyncIOScheduler):
        self.bot = bot
        self.scheduler = scheduler
        self.session = session

    async def createOrUpdateTaskNotifications(self, session: AsyncSession, task_id: int):
        logger.info(f"Создание или изменение планирования уведомлений для задачи#{task_id}")

        task = await TaskDAO.find_one_or_none_by_id(session, task_id)
        startDate = task.deadline - timedelta(days=-3)

        self.scheduler.add_job(
            id=f"Job#{task.id}",
            name=f"Notification for task#{task.id}",
            func=NotificationsForTaskPerformers(self.bot, session, task_id),
            trigger=CronTrigger(second=6, start_date=startDate,),
            replace_existing=True
        )
        self.scheduler.start()

    async def deleteTaskNotifications(self, task_id: int):
        logger.info(f"Удаление запланированных уведомлений для задачи#{task_id}")

        self.scheduler.remove_job(
            id=f"Job#{task_id}",
        )
