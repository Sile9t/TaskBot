from config import settings
from loguru import logger
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, ConversationHandler, CommandHandler, CallbackQueryHandler, ContextTypes
from taskbot.dao.database import async_session_maker as session, create_db

BOT_TOKEN = settings.TG_KEY

"""
Для настройки маршрутизации создаются номера маршрутов, по которым бот будет обращаться к соответствующим хендлерам.
Для удобства разработки, номера, в зависимости от категории, имеют разницу в десять пунктов.
Пример: Управление сотрудниками осуществляется в маршрутах с 11 по 19, управление задачами - с 21 по 29
"""
START_ROUTES, END_ROUTES, START_OVER = range(3)
EMPLOYEE_MANAGE, ADD_EMPLOYEE, REMOVE_EMPLOYEE = range(11, 14)
SEND_MESSAGES, SEND_MESSAGE_CONFIRM = range (21, 23)
TASK_LIST, TASK_ADD, TASK_REMOVE = range(31, 34)
DEADLINES_LIST = 41

"""
/start
Начальное сообщение от бота для начала взаимодействия.
Вызывает отдельное сообщение, а не видоизменяет предыдущее, в отличие от всех нижеописанных функций.
"""
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # keyboard = [
    #     [
    #         InlineKeyboardButton("Управление сотрудниками", callback_data=str(EMPLOYEE_MANAGE)),
    #         InlineKeyboardButton("Создать рассылку",        callback_data=str(SEND_MESSAGES))
    #     ],
    #     [
    #         InlineKeyboardButton("Актуальные задачи",       callback_data=str(TASK_LIST)),
    #         InlineKeyboardButton("Создать/удалить задачу",  callback_data=str(TASK_ADD))
    #     ],
    #     [InlineKeyboardButton("Календарь дедлайнов",        callback_data=str(DEADLINES_LIST))]
    # ]

    # reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Hello there!")

    # return START_ROUTES

def create_app():
    
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    logger.info("Application is built")

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START_ROUTES: [
                # CallbackQueryHandler(start_over, pattern="^" + str(START_OVER) + "$"),

                # # Управление сотрудниками
                # CallbackQueryHandler(employee_manage, pattern="^" + str(EMPLOYEE_MANAGE) + "$"),
                # CallbackQueryHandler(add_employee, pattern="^" + str(ADD_EMPLOYEE) + "$"),
                # CallbackQueryHandler(remove_employee, pattern="^" + str(REMOVE_EMPLOYEE) + "$"),

                # # Управление рассылкой
                # CallbackQueryHandler(send_messages, pattern="^" + str(SEND_MESSAGES) + "$"),
                # CallbackQueryHandler(send_message_confirm, pattern="^" + str(SEND_MESSAGE_CONFIRM) + "$"),

                # # Управление задачами
                # CallbackQueryHandler(task_list, pattern="^" + str(TASK_LIST) + "$"),
                # CallbackQueryHandler(task_add, pattern="^" + str(TASK_ADD) + "$"),
                # CallbackQueryHandler(task_remove, pattern="^" + str(TASK_REMOVE) + "$"),
                
                # # Управление дедлайнами
                # CallbackQueryHandler(deadlines_list, pattern="^" + str(DEADLINES_LIST) + "$")
            ],
            END_ROUTES: [
                # CallbackQueryHandler(start, pattern="^" + str(START_ROUTES) + "$"),
                # CallbackQueryHandler(end, pattern="^" + str(END_ROUTES) + "$"),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    app.add_handler(conv_handler)
    
    return app