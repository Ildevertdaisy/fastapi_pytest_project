
import pytest
import asyncio
import httpx
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import status

from fastapi_pytest_project.app import app

