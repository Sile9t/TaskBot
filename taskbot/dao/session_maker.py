from functools import wraps
from typing import Optional
from sqlalchemy import text

from taskbot.dao.database import async_session_maker


def connection(method, commit: bool = True):
    @wraps(method)
    async def wrapper(*args, **kwargs):
        async with async_session_maker() as session:
            try:
                result = await method(*args, session=session, **kwargs)

                if commit:
                    await session.commit()

                return result
            except Exception as e:
                await session.rollback()
                raise
            finally:
                await session.close()

    return wrapper