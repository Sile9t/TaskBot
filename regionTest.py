import asyncio
from taskbot.dao.dao import RegionDAO
from taskbot.dao.schemas import RegionDtoBase
from taskbot.dao.session_maker import connection

@connection
async def addRegion(session):
    newRegion = RegionDtoBase(
        name='Test region',
        description='Test region description'
    )
    
    session = await container.session_with_commit()
    regionRecord = await RegionDAO.add(session, newRegion)
    
    print(f"Session instance: {session}")
    print("Record added with id:", regionRecord.id)
    await session.commit()

asyncio.run(addRegion())