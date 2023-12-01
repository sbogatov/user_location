from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import get_session
from country.models.country_model import Country
from country.dto.country_dto import CountryDTO
from country.repositories.country_repository import CountryRepository
from exceptions import DuplicatedObjectException

country_router = APIRouter()

COUNTRIES_URL = "/countries"


@country_router.get(COUNTRIES_URL, response_model=list[CountryDTO])
async def get_countries(session: AsyncSession = Depends(get_session)) -> list[Country]:
    return await CountryRepository.all(session=session)


@country_router.post(COUNTRIES_URL)
async def create_country(country_dto: CountryDTO, session: AsyncSession = Depends(get_session)) -> None:
    try:
        await CountryRepository.add(country_dto=country_dto, session=session)
    except DuplicatedObjectException as exc:
        raise HTTPException(status_code=400, detail=exc.message) from exc
