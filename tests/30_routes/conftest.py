import pytest

from client import PssFleetDataClient
from client.model.api import ApiCollection


@pytest.fixture(scope="function")
def response_get_collection_200(api_collection: ApiCollection):
    return api_collection.model_dump_json()


@pytest.fixture(scope="session", autouse=True)
def test_client(base_url):
    client = PssFleetDataClient(
        base_url=base_url,
        api_key="123456",
    )
    yield client


@pytest.fixture(scope="session")
def base_url() -> str:
    return "https://fleetdata.dolores2.xyz"


@pytest.fixture(scope="function")
def get_collection_url(base_url) -> str:
    return f"{base_url}/collections/1"


@pytest.fixture(scope="function")
def mock_response_get_collection_200(api_collection: ApiCollection, httpx_mock):
    httpx_mock.add_response(
        method="GET",
        url="https://fleetdata.dolores2.xyz/collections/1",
        text=api_collection.model_dump_json(),
    )


@pytest.fixture(scope="function")
def mock_response_get_collection_404(api_collection: ApiCollection, httpx_mock):
    httpx_mock.add_response(
        method="GET",
        url="https://fleetdata.dolores2.xyz/collections/1",
        status_code=404,
        json={
            "code": "COLLECTION_NOT_FOUND",
            "message": "The requested Collection could not be found.",
            "details": "There is no Collection with the ID '1'.",
            "timestamp": "2024-07-13T14:04:30.696117+00:00",
            "url": "http://fleetdata.dolores2.xyz/collections/1",
            "suggestion": "Check the provided `collectionId` parameter in the path.",
            "links": [],
        },
    )


@pytest.fixture(scope="function")
def mock_response_get_collection_422(api_collection: ApiCollection, httpx_mock):
    httpx_mock.add_response(
        method="GET",
        url="https://fleetdata.dolores2.xyz/collections/f",
        status_code=422,
        json={
            "code": "PARAMETER_COLLECTION_ID_INVALID",
            "message": "The provided value for the parameter `collectionId` is invalid.",
            "details": "Input should be a valid integer, unable to parse string as an integer",
            "timestamp": "2024-07-13T14:07:26.955843+00:00",
            "url": "http://fleetdata.dolores2.xyz/collections/f",
            "suggestion": "",
            "links": [],
        },
    )
