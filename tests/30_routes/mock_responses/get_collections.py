import pytest

from client.model.api import ApiCollection


@pytest.fixture(scope="function")
def mock_response_get_collections_200(api_collection: ApiCollection, base_url: str, httpx_mock):
    httpx_mock.add_response(
        method="GET",
        url=f"{base_url}/collections/",
        text=f"[{api_collection.model_dump_json()}]",
    )
