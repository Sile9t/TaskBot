from typing import List
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from taskbot.dao.session_maker import connection
from taskbot.dao.dao import RoleDAO, RegionDAO
from taskbot.dao.schemas import RoleDto, RegionDto


defaultRoles = [
    RoleDto(
        id=1,
        name='Администратор',
        description=None
    ),
    RoleDto(
        id=2,
        name='Руководитель региона',
        description=None
    ),
    RoleDto(
        id=3,
        name='Сотрудник(Исполнитель)',
        description=None
    )
]

@connection
async def seedRoles(session: AsyncSession, data: List[RoleDto] = defaultRoles):
    count = await RoleDAO.count(session)
    
    if (count == 0):
        try:
            for item in data:
                await RoleDAO.add(session, item)
            
            await session.commit()
        except Exception as e:
            logger.error(f"Ошибка при seedRoles: {e}")
            raise e


defaultRegions = [
    RegionDto(
        id=1,
        name='Алтайский край',
        description='Код: 22'
    ),
    RegionDto(
        id=2,
        name='Амурская область',
        description='Код: 28'
    ),
    RegionDto(
        id=3,
        name='Архангельская область',
        description='Код: 29'
    ),
    RegionDto(
        id=4,
        name='Астраханская область',
        description='Код: 30'
    ),
    RegionDto(
        id=5,
        name='Астраханская область',
        description='Код: 31'
    ),
    RegionDto(
        id=6,
        name='Брянская область',
        description='Код: 32'
    ),
    RegionDto(
        id=7,
        name='Владимирская область',
        description='Код: 33'
    ),
    RegionDto(
        id=8,
        name='Волгоградская область',
        description='Код: 34'
    ),
    RegionDto(
        id=9,
        name='Волгоградская область',
        description='Код: 35'
    ),
    RegionDto(
        id=10,
        name='Воронежская область',
        description='Код: 36'
    ),
    RegionDto(
        id=11,
        name='город федерального значения Москва',
        description='Код: 77'
    ),
    RegionDto(
        id=12,
        name='город федерального значения Санкт-Петербург',
        description='Код: 78'
    ),
    RegionDto(
        id=13,
        name='город федерального значения Севастополь',
        description='Код: 92'
    ),
    RegionDto(
        id=14,
        name='Донецкая Народная Республика',
        description='Код: 93'
    ),
    RegionDto(
        id=15,
        name='Еврейская автономная область',
        description='Код: 79'
    ),
    RegionDto(
        id=16,
        name='Забайкальский край',
        description='Код: 75'
    ),
    RegionDto(
        id=17,
        name='Запорожская область',
        description='Код: 90'
    ),
    RegionDto(
        id=18,
        name='Ивановская область',
        description='Код: 37'
    ),
    RegionDto(
        id=19,
        name='Иные территории,включая город и космодром Байконур',
        description='Код: 99'
    ),
    RegionDto(
        id=20,
        name='Иркутская область',
        description='Код: 38'
    ),
    RegionDto(
        id=21,
        name='Кабардино-Балкарская Республика',
        description='Код: 7'
    ),
    RegionDto(
        id=22,
        name='Калининградская область',
        description='Код: 39'
    ),
    RegionDto(
        id=23,
        name='Калужская область',
        description='Код: 40'
    ),
    RegionDto(
        id=24,
        name='Камчатский край',
        description='Код: 41'
    ),
    RegionDto(
        id=25,
        name='Карачаево-Черкесская Республика',
        description='Код: 9'
    ),
    RegionDto(
        id=26,
        name='Кемеровская область — Кузбасс',
        description='Код: 42'
    ),
    RegionDto(
        id=27,
        name='Кировская область',
        description='Код: 43'
    ),
    RegionDto(
        id=28,
        name='Костромская область',
        description='Код: 44'
    ),
    RegionDto(
        id=29,
        name='Краснодарский край',
        description='Код: 23'
    ),
    RegionDto(
        id=30,
        name='Красноярский край',
        description='Код: 24'
    ),
    RegionDto(
        id=31,
        name='Курганская область',
        description='Код: 45'
    ),
    RegionDto(
        id=32,
        name='Курская область',
        description='Код: 46'
    ),
    RegionDto(
        id=33,
        name='Ленинградская область',
        description='Код: 47'
    ),
    RegionDto(
        id=34,
        name='Липецкая область',
        description='Код: 48'
    ),
    RegionDto(
        id=35,
        name='Луганская Народная Республика',
        description='Код: 94'
    ),
    RegionDto(
        id=36,
        name='Магаданская область',
        description='Код: 49'
    ),
    RegionDto(
        id=37,
        name='Московская область',
        description='Код: 50'
    ),
    RegionDto(
        id=38,
        name='Мурманская область',
        description='Код: 51'
    ),
    RegionDto(
        id=39,
        name='Ненецкий автономный округ',
        description='Код: 83'
    ),
    RegionDto(
        id=40,
        name='Нижегородская область',
        description='Код: 52'
    ),
    RegionDto(
        id=41,
        name='Новгородская область',
        description='Код: 53'
    ),
    RegionDto(
        id=42,
        name='Новосибирская область',
        description='Код: 54'
    ),
    RegionDto(
        id=43,
        name='Омская область',
        description='Код: 55'
    ),
    RegionDto(
        id=44,
        name='Оренбургская область',
        description='Код: 56'
    ),
    RegionDto(
        id=45,
        name='Орловская область',
        description='Код: 57'
    ),
    RegionDto(
        id=46,
        name='Пензенская область',
        description='Код: 58'
    ),
    RegionDto(
        id=47,
        name='Пермский край',
        description='Код: 59'
    ),
    RegionDto(
        id=48,
        name='Приморский край',
        description='Код: 25'
    ),
    RegionDto(
        id=49,
        name='Псковская область',
        description='Код: 60'
    ),
    RegionDto(
        id=50,
        name='Республика Адыгея (Адыгея)',
        description='Код: 1'
    ),
    RegionDto(
        id=51,
        name='Республика Алтай',
        description='Код: 4'
    ),
    RegionDto(
        id=52,
        name='Республика Алтай',
        description='Код: 2'
    ),
    RegionDto(
        id=53,
        name='Республика Бурятия',
        description='Код: 3'
    ),
    RegionDto(
        id=54,
        name='Республика Дагестан',
        description='Код: 5'
    ),
    RegionDto(
        id=55,
        name='Республика Ингушетия',
        description='Код: 6'
    ),
    RegionDto(
        id=56,
        name='Республика Калмыкия',
        description='Код: 8'
    ),
    RegionDto(
        id=57,
        name='Республика Карелия',
        description='Код: 10'
    ),
    RegionDto(
        id=58,
        name='Республика Коми',
        description='Код: 11'
    ),
    RegionDto(
        id=59,
        name='Республика Крым',
        description='Код: 91'
    ),
    RegionDto(
        id=60,
        name='Республика Марий Эл',
        description='Код: 12'
    ),
    RegionDto(
        id=61,
        name='Республика Марий Эл',
        description='Код: 13'
    ),
    RegionDto(
        id=62,
        name='Республика Саха (Якутия)',
        description='Код: 14'
    ),
    RegionDto(
        id=63,
        name='Республика Северная Осетия — Алания',
        description='Код: 15'
    ),
    RegionDto(
        id=64,
        name='Республика Северная Осетия — Алания',
        description='Код: 16'
    ),
    RegionDto(
        id=65,
        name='Республика Тыва',
        description='Код: 17'
    ),
    RegionDto(
        id=66,
        name='Республика Хакасия',
        description='Код: 19'
    ),
    RegionDto(
        id=67,
        name='Республика Хакасия',
        description='Код: 61'
    ),
    RegionDto(
        id=68,
        name='Рязанская область',
        description='Код: 62'
    ),
    RegionDto(
        id=69,
        name='Самарская область',
        description='Код: 63'
    ),
    RegionDto(
        id=70,
        name='Самарская область',
        description='Код: 64'
    ),
    RegionDto(
        id=71,
        name='Самарская область',
        description='Код: 65'
    ),
    RegionDto(
        id=72,
        name='Свердловская область',
        description='Код: 66'
    ),
    RegionDto(
        id=73,
        name='Свердловская область',
        description='Код: 67'
    ),
    RegionDto(
        id=74,
        name='Ставропольский край',
        description='Код: 26'
    ),
    RegionDto(
        id=75,
        name='Тамбовская область',
        description='Код: 68'
    ),
    RegionDto(
        id=76,
        name='Тверская область',
        description='Код: 69'
    ),
    RegionDto(
        id=77,
        name='Томская область',
        description='Код: 70'
    ),
    RegionDto(
        id=78,
        name='Тульская область',
        description='Код: 71'
    ),
    RegionDto(
        id=79,
        name='Тюменская область',
        description='Код: 72'
    ),
    RegionDto(
        id=80,
        name='Удмуртская Республика',
        description='Код: 18'
    ),
    RegionDto(
        id=81,
        name='Ульяновская область',
        description='Код: 73'
    ),
    RegionDto(
        id=82,
        name='Хабаровский край',
        description='Код: 27'
    ),
    RegionDto(
        id=83,
        name='Ханты-Мансийский автономный округ — Югра',
        description='Код: 86'
    ),
    RegionDto(
        id=84,
        name='Херсонская область',
        description='Код: 95'
    ),
    RegionDto(
        id=85,
        name='Челябинская область',
        description='Код: 74'
    ),
    RegionDto(
        id=86,
        name='Чеченская Республика',
        description='Код: 20'
    ),
    RegionDto(
        id=87,
        name='Чувашская Республика — Чувашия',
        description='Код: 21'
    ),
    RegionDto(
        id=88,
        name='Чукотский автономный округ',
        description='Код: 87'
    ),
    RegionDto(
        id=89,
        name='Ямало-Ненецкий автономный округ',
        description='Код: 89'
    ),
    RegionDto(
        id=90,
        name='Ямало-Ненецкий автономный округ',
        description='Код: 76'
    )
]

@connection
async def seedRegions(session: AsyncSession, data: List[RegionDto] = defaultRegions):
    count = await RegionDAO.count(session)
    
    if (count == 0):
        try:
            for item in data:
                await RegionDAO.add(session, item)
            
            await session.commit()
        except Exception as e:
            logger.error(f"Ошибка при seedRegions: {e}")
            raise e


async def seed():
    await seedRoles()
    await seedRegions()