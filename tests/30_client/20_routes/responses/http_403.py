import pytest
from pytest_httpx import HTTPXMock


@pytest.fixture(scope="function")
def mock_response_403(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        status_code=403,
        json={
            "code": "FORBIDDEN",
            "message": "You don't have the required permissions to access this endpoint.",
            "details": "You're not allowed to use the method 'POST' on the endpoint '/collections/upload'.",
            "timestamp": "2024-07-16T10:59:03.192672+00:00",
            "url": "http://testserver/collections/upload",
            "suggestion": "",
            "links": [],
        },
    )
