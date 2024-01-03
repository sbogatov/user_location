from http import HTTPStatus

import pytest
from httpx import Response, AsyncClient

from country.controllers.country_controller import COUNTRIES_URL
from tests.base_test import BaseTest


@pytest.mark.asyncio
class TestCountry(BaseTest):
    async def test_add_country(self, client: AsyncClient) -> None:
        payload: dict = {"id": 1, "name": "Switzerland"}
        response: Response = await client.post(COUNTRIES_URL, params={"name": "Switzerland"})
        assert response.status_code == HTTPStatus.OK

        response: Response = await client.get(COUNTRIES_URL)
        assert response.status_code == HTTPStatus.OK
        assert response.json() == [payload]
