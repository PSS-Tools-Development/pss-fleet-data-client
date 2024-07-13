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
