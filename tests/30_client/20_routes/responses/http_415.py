import pytest
from pytest_httpx import HTTPXMock


@pytest.fixture(scope="function")
def mock_response_post_415(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        status_code=415,
        json={
            "code": "UNSUPPORTED_MEDIA_TYPE",
            "message": "The provided media type is not supported.",
            "details": "The media type is not supported.",
            "timestamp": "2024-07-16T10:55:30.614769+00:00",
            "url": "https://example.com",
            "suggestion": "",
            "links": [],
        },
    )
