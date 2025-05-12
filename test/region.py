import pytest
from taskbot.dao.database import Database
from taskbot.dao.models import Region
from taskbot.dao.dao import RegionDAO
from taskbot.dao.schemas import RegionDto

class RegionTests:
    db = Database()

    async def createRegion(self):
        # newRegion = Region(
        #     name = "Test region 1",
        #     description = "Test region description"
        # )
        
        # self.db._session_factory.add(newRegion)

        # query = select(Region)
        # result = self.db._session_factory.execute(query)
        # record = result.scalar_one_or_none()

        # print(newRegion.id)
        # assert newRegion.id > 0
        
        region = RegionDto(
            name="Test region 1",
            description="Test region 1 description"
        )
        regionRecord = await RegionDAO.add(self.db.session,region)
        
        print(regionRecord)
        assert regionRecord.id > 0