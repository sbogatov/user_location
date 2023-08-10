from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from city.dto.city_dto import CityDTO
from city.models.city_model import City
from config.database import get_session


city_router = APIRouter()


@city_router.get('/city')
async def get_cities(session: AsyncSession = Depends(get_session)):
    cities = await session.execute(select(City))
    return cities.scalars().all()


@city_router.post('/city')
async def create_country(city_dto: CityDTO, session: AsyncSession = Depends(get_session)):
    city: City = City(id=city_dto.id, name=city_dto.name, country_id=city_dto.country_id)
    session.add(city)
    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Duplicated city")
