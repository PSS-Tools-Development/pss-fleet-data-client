import pytest
from pytest_httpx import HTTPXMock

from client.model.api import ApiAllianceHistory


@pytest.fixture(scope="function")
def get_allianceHistory_1_url(base_url) -> str:
    return f"{base_url}/allianceHistory/1"


@pytest.fixture(scope="function")
def mock_response_allianceHistory_allianceId_get_200(api_alliance_history: ApiAllianceHistory, get_allianceHistory_1_url: str, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="GET",
        url=get_allianceHistory_1_url,
        text=f"[{api_alliance_history.model_dump_json()}]",
    )


@pytest.fixture(scope="function")
def mock_response_allianceHistory_allianceId_404(get_allianceHistory_1_url: str, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=get_allianceHistory_1_url,
        status_code=404,
        json={
            "code": "ALLIANCE_NOT_FOUND",
            "message": "The requested Alliance could not be found.",
            "details": "There is no Alliance with the ID '1'.",
            "timestamp": "2024-07-13T14:04:30.696117+00:00",
            "url": get_allianceHistory_1_url,
            "suggestion": "Check the provided `allianceId` parameter in the path.",
            "links": [],
        },
    )


@pytest.fixture(scope="function")
def mock_response_allianceHistory_allianceId_422(base_url: str, httpx_mock: HTTPXMock):
    get_collection_url = f"{base_url}/allianceHistory/f"
    httpx_mock.add_response(
        url=get_collection_url,
        status_code=422,
        json={
            "code": "PARAMETER_ALLIANCE_ID_INVALID",
            "message": "The provided value for the parameter `allianceId` is invalid.",
            "details": "Input should be a valid integer, unable to parse string as an integer",
            "timestamp": "2024-07-13T14:07:26.955843+00:00",
            "url": get_collection_url,
            "suggestion": "",
            "links": [],
        },
    )
