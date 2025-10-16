"""
The test_me_endpoint_returns_expected_shape function tests
that the /me endpoint returns a JSON response with the expected shape.
"""
import os
import sys
import pytest
from httpx import AsyncClient, ASGITransport
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import app


@pytest.mark.asyncio
async def test_me_endpoint_returns_expected_shape():    
    """
    Tests that the /me endpoint returns a JSON response with the expected shape.

    The response should have the following structure:
    {
        "status": "success",
        "user": {
            "email": str,
            "name": str,
            "stack": str
        },
        "timestamp": str (ISO 8601 timestamp with timezone),
        "fact": str
    }
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/me")

    assert resp.status_code == 200
    data = resp.json()

    assert data.get("status") == "success"
    assert "user" in data
    assert "timestamp" in data
    assert "fact" in data

    user = data["user"]
    assert isinstance(user.get("email"), str) and user.get("email")
    assert isinstance(user.get("name"), str) and user.get("name")
    assert isinstance(user.get("stack"), str) and user.get("stack")

    assert data["timestamp"].endswith("Z") or data["timestamp"].endswith("+00:00")

    assert isinstance(data["fact"], str)
