import pytest
from pytest_httpx import HTTPXMock


@pytest.fixture(scope="function")
def mock_response_401(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        status_code=401,
        json={
            "code": "NOT_AUTHENTICATED",
            "message": "You are not authenticated.",
            "details": "'Authorization' header not found in request.",
            "timestamp": "2024-07-16T10:56:05.618203+00:00",
            "url": "http://127.0.0.1:8000/collections/",
            "suggestion": "Add an 'Authorization' header to the request with an authorized api key.",
            "links": [],
        },
    )
