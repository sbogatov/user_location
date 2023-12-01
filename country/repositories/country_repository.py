from typing import Any

from sqlalchemy import Result, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from country.dto.country_dto import CountryDTO
from country.models.country_model import Country
from exceptions import DuplicatedObjectException


class CountryRepository:
    @staticmethod
    async def all(session: AsyncSession) -> list[Country]:
        countries: Result[Any] = await session.execute(select(Country))
        return countries.scalars().all()

    @staticmethod
    async def add(country_dto: CountryDTO, session: AsyncSession) -> None:
        country: Country = Country(id=country_dto.id, name=country_dto.name)
        session.add(country)
        try:
            await session.commit()
        except IntegrityError as exc:
            raise DuplicatedObjectException from exc
