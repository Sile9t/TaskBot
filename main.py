from warnings import filterwarnings
from loguru import logger
import gspread
import json
import telegram
from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, ConversationHandler
from telegram.warnings import PTBUserWarning

"""
Первым делом осуществляется настройка проекта.
Для исправной работы подгружается appsettings.json: он содержит в себе токен для бота.
Для взаимодействия с Google-таблицами используется gspread.
В него подргужается credentials.json, содержащий информацию для связи с таблицей.
Документация по gspread: https://docs.gspread.org/en/v6.1.3/
"""
appsettings = json.load(open('./appsettings.json'))
BOT_TOKEN = appsettings['data']['bot_token']
addTask_formlink = appsettings['data']['addTask_formlink']
removeTask_formlink = appsettings['data']['removeTask_formlink']
googleTableName = appsettings['data']['tableName']

"""
Поскольку осуществляется работа с Google-формами - добавляются ссылки к ним в соответствующие переменные.
Формы создаются к Google-таблице, первая форма (Форма1) отвечает за добавление задач, вторая (Форма2) - за их удаление.
"""
gc = gspread.service_account(filename='./credentials.json')
sh = gc.open(googleTableName).sheet1

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
Функция собирает файлы из первого листа, который является ответами на Форму1.
Идет сортировка данных по дедлайнам.
"""
def GetAvailableTasks():
    sh = gc.open("bot").sheet1
    sh_completed = gc.open("bot").worksheet(1)

    keyValue = 1
    data = []
    while True:
        answer = sh.row_values(keyValue)
        if None in answer or "" in answer or answer == []:
            break
        data.append(answer)
        keyValue += 1
    
    data = data[1:]
    data = sorted(data, key=lambda x: datetime.strptime(x[4], '%d.%m.%Y'))
    return data

"""
/start
Начальное сообщение от бота для начала взаимодействия.
Вызывает отдельное сообщение, а не видоизменяет предыдущее, в отличие от всех нижеописанных функций.
"""
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Управление сотрудниками", callback_data=str(EMPLOYEE_MANAGE)),
            InlineKeyboardButton("Создать рассылку",        callback_data=str(SEND_MESSAGES))
        ],
        [
            InlineKeyboardButton("Актуальные задачи",       callback_data=str(TASK_LIST)),
            InlineKeyboardButton("Создать/удалить задачу",  callback_data=str(TASK_ADD))
        ],
        [InlineKeyboardButton("Календарь дедлайнов",        callback_data=str(DEADLINES_LIST))]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Пожалуйста, выберите дальнейшее действие:", reply_markup=reply_markup)

    return START_ROUTES

"""
Вспомогательная функция. Возвращается к сообщению /start из иных состояний.
"""
async def start_over(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Управление сотрудниками", callback_data=str(EMPLOYEE_MANAGE)),
            InlineKeyboardButton("Создать рассылку",        callback_data=str(SEND_MESSAGES))
        ],
        [
            InlineKeyboardButton("Актуальные задачи",       callback_data=str(TASK_LIST)),
            InlineKeyboardButton("Создать/удалить задачу",  callback_data=str(TASK_ADD))
        ],
        [InlineKeyboardButton("Календарь дедлайнов",        callback_data=str(DEADLINES_LIST))]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text("Пожалуйста, выберите дальнейшее действие:", reply_markup=reply_markup)

    return START_ROUTES

"""
Функция для управления сотрудниками. Предоставляет выбор для взаимодействия с аккаунтами.
"""
async def employee_manage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Добавить в качестве сотрудника", callback_data=str(ADD_EMPLOYEE))],
        [InlineKeyboardButton("Удалить из списка сотрудников",  callback_data=str(REMOVE_EMPLOYEE))],
        [InlineKeyboardButton("Вернуться",                      callback_data=str(START_OVER))]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    answer = "Для того, чтобы бот мог обращаться к определенным аккаунтам, их следует зарегистрировать в нем.\n\nЧто сделать с данным аккаунтом?"
    await query.edit_message_text(text=answer, reply_markup=reply_markup)
    return START_ROUTES

"""
Функция добавляет уникальных сотрудников в файл users.txt в формате '{chat_id} {username}'
"""
async def add_employee(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Вернуться",                  callback_data=str(EMPLOYEE_MANAGE))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    currentChat = f"{update.effective_chat.id} {update.effective_chat.username}"
    file_read = open("./users.txt", "r").read().splitlines()
    
    answer = ""
    if currentChat in file_read:
        answer = "Аккаунт уже существует в базе данных бота."
    else:
        file_write = open("./users.txt", "a")
        file_write.write("\n" + currentChat)
        file_write.close()
        answer = "Аккаунт был успешно добавлен в качестве сотрудника."

    await query.edit_message_text(text=answer, reply_markup=reply_markup)
    return START_ROUTES

"""
Функция удаляет сотрудников из файла users.txt
"""
async def remove_employee(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Вернуться",                      callback_data=str(EMPLOYEE_MANAGE))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    answer = ""
    chat_id = str(update.effective_chat.id)
    file_read = open("./users.txt", "r").read().splitlines()

    if file_read == None or file_read == []:
        answer = "Список сотрудников пуст"
    elif chat_id not in file_read:
        answer = "Сотрудник не существует в списке"
    else:
        file_read.remove(chat_id)
        if file_read == []:
            file_read = ""
        file_write = open("./users.txt", "w")
        file_write.truncate(0)
        for data in file_read:
            file_write.write(data)
        file_write.close()
        answer = "Аккаунт был успешно удален из списка сотрудников."
    await query.edit_message_text(text=answer, reply_markup=reply_markup)
    return START_ROUTES

"""
Функция-заглушка для создания рассылки сотрудникам о просроченных задачах.
Поскольку данное действие будет затрагивать большое количество людей, данная функция
является 'предохранителем' от случайного нажатия на кнопку. Если пользователь подтверждает свои
намерения - идет переход в функцию send_message_confirm
"""
async def send_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Подтвердить",                    callback_data=str(SEND_MESSAGE_CONFIRM))],
        [InlineKeyboardButton("Вернуться",                      callback_data=str(START_OVER))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    answer = "Внимание!\n\nВы собираетесь выполнить рассылку сотрудникам, которые не выполнили свои задачи.\n\nПродолжить?"
    await query.edit_message_text(text=answer, reply_markup=reply_markup)
    return START_ROUTES


"""
Функция для создания рассылки сотрудникам о просроченных задачах.
Выполняет сбор информации из users.txt, получает актуальные задачи из таблицы,
после чего сравнивает их дедлайны с текущим временем. При условии, что задача была просрочена,
находит chat_id с помощью username, указанного в таблице.
"""
async def send_message_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Выполнить еще одну рассылку",    callback_data=str(SEND_MESSAGES))],
        [InlineKeyboardButton("Вернуться",                      callback_data=str(START_OVER))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    employees = open("./users.txt", "r").read().splitlines()
    employees_names = []
    if employees == None or employees == []:
        answer = "Список сотрудников пуст"
        await bot.send_message(text=answer, chat_id=update.effective_chat.id)
        return START_ROUTES
    else:
        for item in employees:
            item_splitted = item.split(' ')
            employees_names.append(item_splitted)

    data = GetAvailableTasks()
    currentDate = datetime.now().date()

    bot = telegram.Bot(BOT_TOKEN)
    async with bot:
        for item in data:
            item[4] = datetime.strptime(item[4], "%d.%m.%Y").date()
            if item[4] < currentDate:
                chat_username = item[2]
                for line in employees_names:
                    if line[1] == chat_username:
                        answer = f"Внимание!\nУ вас есть невыполненная задача '{item[1]}, которую необходимо было сдать до следующей даты: {item[4]}'"
                        answer += "\nУбедитесь, что вы заполнили форму для сдачи задачи."
                        await bot.send_message(text=answer, chat_id=line[0])            

    answer = "Рассылка была успешно выполнена!"
    await query.edit_message_text(text=answer, reply_markup=reply_markup)
    return START_ROUTES

"""
Функция выводит список актуальных задач, который собирается из первого листа таблицы с ответами на Форму1.
Задачи уже отсортированы по дедлайнам, вывод в формате: {TaskName} | {TgUsername} | {NameOfEmployee} | {Deadline} | {Link}
"""
async def task_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Создать задачу",                 callback_data=str(TASK_ADD))],
        [InlineKeyboardButton("Вернуться",                      callback_data=str(START_OVER))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    data = GetAvailableTasks()
    answer = "Вывод информации о задачах в формате:\nНаименование задачи | Исполнитель (Telegram-тэг) | Исполнитель (ФИО) | Дедлайн | Ссылка на задачу\n"
    for item in data:
        answer += f"\n{item[1]} | {item[2]} | {item[3]} | {item[4]} | {item[5]}"
    await query.edit_message_text(text=answer, reply_markup=reply_markup)
    return START_ROUTES

"""
Функции добавления и удаления задачи похожи друг на друга. Они выводят ссылки на формы, которые выполняют
свои собственные задачи. Применение Google-форм для этого обусловлено простотой взаимодействия с Google-таблицей,
при необходимости может быть изменено.
"""
async def task_add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Вернуться",                      callback_data=str(START_OVER))],
        [InlineKeyboardButton("Я хочу завершить задачу",        callback_data=str(TASK_REMOVE))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    answer = f"Для создания задачи заполните следующую форму: {addTask_formlink}"

    await query.edit_message_text(text=answer, reply_markup=reply_markup)
    return START_ROUTES

async def task_remove(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Вернуться",                      callback_data=str(START_OVER))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    answer = f"Выполнили задачу? Заполните форму, чтобы исключить ее из списка актуальных задач: {removeTask_formlink}"

    await query.edit_message_text(text=answer, reply_markup=reply_markup)
    return START_ROUTES

"""
Функция для вывода списка задач и их дедлайнов в чат взаимодействия.
Вывод в формате: {TaskName} | {Deadline}
"""
async def deadlines_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Вернуться",                      callback_data=str(START_OVER))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    answer = "Список задач и дат, к которым их следует закончить:\n\nНазвание задачи | Дата сдачи"
    data = GetAvailableTasks()
    for item in data:
        answer += f"\n{item[1]} | {item[4]}"
    await query.edit_message_text(text=answer, reply_markup=reply_markup)
    return START_ROUTES

"""
Функция-пустышка для отслеживания окончания взаимодействия с ботом при выходе из разговора.
Следует удалить из проекта за ненадобностью.
"""
async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Общение с ботом окончено.")
    return ConversationHandler.END

"""
Основная функция. Создает хендлеры, регистрирует бота и запускает его.

ВАЖНО: здесь выполнена реализации т.н. Conversation - это значит, что при перезапуске бота,
равно как и при попытках вызвать команды, минуя команду /start, ничего происходить не будет.
Все взаимодействия с ботом осущестляются последовательно, маршрут к ним проложен с помощью
соответствующих роутов, указанных в строках [33-37].
"""
def main() -> None:
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(start_over, pattern="^" + str(START_OVER) + "$"),

                # Управление сотрудниками
                CallbackQueryHandler(employee_manage, pattern="^" + str(EMPLOYEE_MANAGE) + "$"),
                CallbackQueryHandler(add_employee, pattern="^" + str(ADD_EMPLOYEE) + "$"),
                CallbackQueryHandler(remove_employee, pattern="^" + str(REMOVE_EMPLOYEE) + "$"),

                # Управление рассылкой
                CallbackQueryHandler(send_messages, pattern="^" + str(SEND_MESSAGES) + "$"),
                CallbackQueryHandler(send_message_confirm, pattern="^" + str(SEND_MESSAGE_CONFIRM) + "$"),

                # Управление задачами
                CallbackQueryHandler(task_list, pattern="^" + str(TASK_LIST) + "$"),
                CallbackQueryHandler(task_add, pattern="^" + str(TASK_ADD) + "$"),
                CallbackQueryHandler(task_remove, pattern="^" + str(TASK_REMOVE) + "$"),
                
                # Управление дедлайнами
                CallbackQueryHandler(deadlines_list, pattern="^" + str(DEADLINES_LIST) + "$")
            ],
            END_ROUTES: [
                CallbackQueryHandler(start, pattern="^" + str(START_ROUTES) + "$"),
                CallbackQueryHandler(end, pattern="^" + str(END_ROUTES) + "$"),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )
    
    logger.info("Bot is running")
    app.add_handler(conv_handler)
    app.run_polling(allowed_updates=Update.ALL_TYPES)

"""
Точка входа в программу.
По всей видимости, при желании создать автоматическую рассылку сообщений, придется
все переделывать в asyncio, чтобы убрать бота в один поток, а средство для
рассылки - в другой.
"""
if __name__ == "__main__":
    main()