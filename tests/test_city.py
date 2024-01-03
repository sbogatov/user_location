from http import HTTPStatus

import pytest
from httpx import Response, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from city.controllers.city_controller import CITIES_URL
from country.models.country_model import Country
from tests.base_test import BaseTest


@pytest.mark.asyncio
class TestCity(BaseTest):
    async def test_add_city(self, client: AsyncClient, test_db_session: AsyncSession) -> None:
        test_db_session.add(Country(id=0, name="Russia"))
        await test_db_session.commit()

        payload: dict = {"id": 1, "country_id": 0, "name": "Moscow"}
        response: Response = await client.post(CITIES_URL, params={"country_id": 0, "name": "Moscow"})
        assert response.status_code == HTTPStatus.OK

        response: Response = await client.get(CITIES_URL, params={'country_id': 0})
        assert response.status_code == HTTPStatus.OK
        assert response.json() == [payload]
