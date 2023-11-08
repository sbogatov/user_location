from http import HTTPStatus

import pytest
from httpx import Response, AsyncClient

from tests.base_test import BaseTest


@pytest.mark.asyncio
class TestCountry(BaseTest):
    async def test_add_country(self, client: AsyncClient) -> None:
        payload: dict = {"id": 1, "name": "Switzerland"}
        response: Response = await client.post("/country", json=payload)
        assert response.status_code == HTTPStatus.OK

        response: Response = await client.get("/country")
        assert response.status_code == HTTPStatus.OK
        assert response.json() == [payload]

        response: Response = await client.post("/country", json=payload)
        assert response.status_code == HTTPStatus.BAD_REQUEST
