
import pytest
import asyncio
import httpx
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import status

from .app import app


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def test_client():
    async with LifespanManager(app):
        async with httpx.AsyncClient(app=app, base_url="http://app.io") as test_client:
            yield test_client


@pytest.mark.asyncio
async def test_hello_world(test_client: httpx.AsyncClient):
    response = await test_client.get("/")
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json == {"hello": "world"} 


@pytest.mark.asyncio
async def test_invalid(test_client: httpx.AsyncClient):
    payload = {"first_name": "John", "last_name": "Doe"}
    response = await test_client.post("/persons", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    


@pytest.mark.asyncio
async def test_valid(test_client: httpx.AsyncClient):
    payload = {"first_name": "John", "last_name": "Doe", "age": 30}
    response = await test_client.post("/persons", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    json = response.json()
    assert json == payload