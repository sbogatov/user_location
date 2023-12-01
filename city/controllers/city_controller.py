from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from city.dto.city_dto import CityDTO
from city.models.city_model import City
from city.repositories.city_repository import CityRepository
from config.database import get_session
from exceptions import DuplicatedObjectException

city_router = APIRouter()

CITIES_URL = "/cities"


@city_router.get(CITIES_URL, response_model=list[CityDTO])
async def get_cities(country_id: int, session: AsyncSession = Depends(get_session)) -> list[City]:
    return await CityRepository.get_by_country_id(country_id=country_id, session=session)


@city_router.post(CITIES_URL)
async def create_city(city_dto: CityDTO, session: AsyncSession = Depends(get_session)) -> None:
    try:
        await CityRepository.add(city_dto=city_dto, session=session)
    except DuplicatedObjectException as exc:
        raise HTTPException(status_code=400, detail=exc.message) from exc
