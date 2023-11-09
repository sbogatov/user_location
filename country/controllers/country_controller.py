from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import get_session
from country.models.country_model import Country
from country.dto.country_dto import CountryDTO

country_router = APIRouter()


@country_router.get('/country')
async def get_countries(session: AsyncSession = Depends(get_session)):
    countries: Result[Any] = await session.execute(select(Country))
    return countries.scalars().all()


@country_router.post('/country')
async def create_country(country_dto: CountryDTO, session: AsyncSession = Depends(get_session)):
    country: Country = Country(id=country_dto.id, name=country_dto.name)
    session.add(country)
    try:
        await session.commit()
    except IntegrityError as exc:
        raise HTTPException(status_code=400, detail="Duplicated country") from exc
