import re
from loguru import logger
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

def extract_number(text):
    match = re.search(r'\b(\d+)\b', text)
    if match:
        return int(match.group(1))
    else:
        return None
    
async def process_dell_text_msg(message: Message, state: FSMContext):
    bot = message.bot
    data = await state.get_data()
    last_msg_id = data.get('last_msg_id')

    try:
        if last_msg_id:
            await bot.delete_message(chat_id=message.from_user.id, message_id=last_msg_id)
        else:
            logger.warning("Ошибка: Не удалось найти идентификатор последнего сообщения для удаления.")
        await message.delete()

    except Exception as e:
        logger.error(f"Произошла ошибка при удалении сообщения: {str(e)}")