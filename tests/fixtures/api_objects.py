from datetime import datetime, timezone
from typing import Callable

import pytest
from pssapi.entities import Alliance as PssAlliance
from pssapi.entities import User as PssUser

from client import utils
from client.model import AllianceHistory, Collection, CollectionMetadata, UserHistory
from client.model.api import ApiAlliance, ApiAllianceHistory, ApiCollection, ApiCollectionMetadata, ApiUser, ApiUserHistory

from .factory import (
    create_api_alliance,
    create_api_collection,
    create_api_collection_metadata_3,
    create_api_collection_metadata_9,
    create_api_user,
    create_collection,
    create_collection_metadata_3,
    create_collection_metadata_9,
    create_pss_alliance,
    create_pss_user,
)


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
    return create_api_collection()


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
