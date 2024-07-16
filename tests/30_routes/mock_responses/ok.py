import pytest
from pytest_httpx import HTTPXMock

from client.models.api_models import ApiAllianceHistory, ApiCollection


@pytest.fixture(scope="function")
def mock_response_allianceHistory_allianceId_get_200(api_alliance_history: ApiAllianceHistory, get_allianceHistory_1_url: str, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="GET",
        url=get_allianceHistory_1_url,
        text=f"[{api_alliance_history.model_dump_json()}]",
    )


@pytest.fixture(scope="function")
def mock_response_allianceHistory_allianceId_get_200_with_members(
    api_alliance_history_with_members: ApiAllianceHistory, get_allianceHistory_1_url: str, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(
        method="GET",
        url=get_allianceHistory_1_url,
        text=f"[{api_alliance_history_with_members.model_dump_json()}]",
    )


@pytest.fixture(scope="function")
def mock_response_get_collections_200(api_collection: ApiCollection, get_collections_url: str, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="GET",
        url=get_collections_url,
        text=f"[{api_collection.model_dump_json()}]",
    )


@pytest.fixture(scope="function")
def mock_response_collections_collectionId_get_200(api_collection: ApiCollection, get_collection_1_url: str, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="GET",
        url=get_collection_1_url,
        text=api_collection.model_dump_json(),
    )


@pytest.fixture(scope="function")
def mock_response_collections_collectionId_alliances_get_200(api_collection_with_fleets: ApiCollection, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="GET",
        text=api_collection_with_fleets.model_dump_json(),
    )


@pytest.fixture(scope="function")
def mock_response_collections_collectionId_alliances_allianceId_get_200(api_alliance_history: ApiAllianceHistory, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="GET",
        text=api_alliance_history.model_dump_json(),
    )


@pytest.fixture(scope="function")
def mock_response_collections_collectionId_alliances_allianceId_get_200_with_members(
    api_alliance_history_with_members: ApiAllianceHistory, httpx_mock: HTTPXMock
):
    httpx_mock.add_response(
        method="GET",
        text=api_alliance_history_with_members.model_dump_json(),
    )


@pytest.fixture(scope="function")
def mock_response_collections_collectionId_users_get_200(api_collection_with_users: ApiCollection, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="GET",
        text=api_collection_with_users.model_dump_json(),
    )


@pytest.fixture(scope="function")
def mock_response_collections_collectionId_users_userId_get_200(api_user_history: ApiAllianceHistory, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="GET",
        text=api_user_history.model_dump_json(),
    )


@pytest.fixture(scope="function")
def mock_response_collections_collectionId_users_userId_get_200_with_fleet(api_user_history_with_fleet: ApiAllianceHistory, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="GET",
        text=api_user_history_with_fleet.model_dump_json(),
    )
