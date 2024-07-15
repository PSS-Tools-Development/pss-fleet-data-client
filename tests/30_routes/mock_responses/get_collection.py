import pytest

from client.model.api import ApiCollection


@pytest.fixture(scope="function")
def get_collection_1_url(base_url) -> str:
    return f"{base_url}/collections/1"


@pytest.fixture(scope="function")
def mock_response_get_collection_200(api_collection: ApiCollection, get_collection_1_url: str, httpx_mock):
    httpx_mock.add_response(
        method="GET",
        url=get_collection_1_url,
        text=api_collection.model_dump_json(),
    )


@pytest.fixture(scope="function")
def mock_response_get_collection_404(get_collection_1_url: str, httpx_mock):
    httpx_mock.add_response(
        method="GET",
        url=get_collection_1_url,
        status_code=404,
        json={
            "code": "COLLECTION_NOT_FOUND",
            "message": "The requested Collection could not be found.",
            "details": "There is no Collection with the ID '1'.",
            "timestamp": "2024-07-13T14:04:30.696117+00:00",
            "url": get_collection_1_url,
            "suggestion": "Check the provided `collectionId` parameter in the path.",
            "links": [],
        },
    )


@pytest.fixture(scope="function")
def mock_response_get_collection_422(base_url: str, httpx_mock):
    get_collection_url = f"{base_url}/collections/f"
    httpx_mock.add_response(
        method="GET",
        url=get_collection_url,
        status_code=422,
        json={
            "code": "PARAMETER_COLLECTION_ID_INVALID",
            "message": "The provided value for the parameter `collectionId` is invalid.",
            "details": "Input should be a valid integer, unable to parse string as an integer",
            "timestamp": "2024-07-13T14:07:26.955843+00:00",
            "url": get_collection_url,
            "suggestion": "",
            "links": [],
        },
    )
