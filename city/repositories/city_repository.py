from sqlalchemy import Select, select, Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from city.dto.city_dto import CityDTO
from city.models.city_model import City
from exceptions import DuplicatedObjectException


class CityRepository:
    @staticmethod
    async def get_by_country_id(country_id: int, session: AsyncSession) -> list[City]:
        query: Select = select(City).where(City.country_id == country_id)
        result: Result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def add(city_dto: CityDTO, session: AsyncSession) -> None:
        city: City = City(id=city_dto.id, name=city_dto.name, country_id=city_dto.country_id)
        session.add(city)
        try:
            await session.commit()
        except IntegrityError as exc:
            raise DuplicatedObjectException from exc
