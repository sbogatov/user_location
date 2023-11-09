from http import HTTPStatus

import pytest
from httpx import Response, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from country.models.country_model import Country
from tests.base_test import BaseTest


@pytest.mark.asyncio
class TestCity(BaseTest):
    async def test_add_city(self, client: AsyncClient, test_db_session: AsyncSession) -> None:
        test_db_session.add(Country(id=0, name="Russia"))
        await test_db_session.commit()

        payload: dict = {"id": 0, "country_id": 0, "name": "Moscow"}
        response: Response = await client.post("/city", json=payload)
        assert response.status_code == HTTPStatus.OK

        response: Response = await client.get("/city")
        assert response.status_code == HTTPStatus.OK
        assert response.json() == [payload]

        response: Response = await client.post("/city", json=payload)
        assert response.status_code == HTTPStatus.BAD_REQUEST
