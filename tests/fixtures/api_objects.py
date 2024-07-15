from typing import Callable

import pytest

from client.model.api import ApiAlliance, ApiAllianceHistory, ApiCollection, ApiCollectionMetadata, ApiUser, ApiUserHistory

from .factory import create_api_alliance, create_api_collection_9, create_api_collection_metadata_3, create_api_collection_metadata_9, create_api_user


@pytest.fixture(scope="function")
def api_alliance() -> ApiAlliance:
    return create_api_alliance()


@pytest.fixture(scope="function")
def api_alliance_history(api_collection_metadata_9: ApiCollectionMetadata, api_alliance: ApiAlliance, api_user: ApiUser) -> ApiAllianceHistory:
    return ApiAllianceHistory(
        collection=api_collection_metadata_9,
        fleet=api_alliance,
        users=[api_user],
    )


@pytest.fixture(scope="function")
def api_collection() -> ApiCollection:
    return create_api_collection_9()


@pytest.fixture(scope="function")
def api_collection_with_fleets() -> ApiCollection:
    return ApiCollection(
        metadata=create_api_collection_metadata_9(),
        fleets=[create_api_alliance()],
    )


@pytest.fixture(scope="function")
def api_collection_with_users() -> ApiCollection:
    return ApiCollection(
        metadata=create_api_collection_metadata_9(),
        users=[create_api_user()],
    )


@pytest.fixture(scope="function")
def api_collection_metadata_3() -> ApiCollectionMetadata:
    return create_api_collection_metadata_3()


@pytest.fixture(scope="function")
def api_collection_metadata_9() -> ApiCollectionMetadata:
    return create_api_collection_metadata_9()


@pytest.fixture(scope="function")
def api_user() -> ApiUser:
    return create_api_user()


@pytest.fixture(scope="function")
def api_user_history(api_collection_metadata_9: Callable[[], ApiCollectionMetadata], api_alliance: ApiAlliance, api_user: ApiUser) -> ApiUserHistory:
    return ApiUserHistory(
        collection=api_collection_metadata_9,
        user=api_user,
        fleet=api_alliance,
    )
