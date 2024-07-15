from datetime import datetime, timezone
from typing import Callable

import pytest
from pssapi.entities import Alliance as PssAlliance
from pssapi.entities import User as PssUser

from client import utils
from client.model import AllianceHistory, Collection, CollectionMetadata, UserHistory
from client.model.api import ApiAlliance, ApiAllianceHistory, ApiCollection, ApiCollectionMetadata, ApiUser, ApiUserHistory


# Equal


@pytest.fixture(scope="session")
def assert_api_alliances_equal() -> Callable[[ApiAlliance, ApiAlliance], None]:
    def _assert_api_alliances_equal(api_alliance_1: ApiAlliance, api_alliance_2: ApiAlliance):
        assert api_alliance_1 == api_alliance_2

    return _assert_api_alliances_equal


@pytest.fixture(scope="session")
def assert_api_collections_equal(
    assert_api_alliances_equal: Callable[[ApiAlliance, ApiAlliance], None],
    assert_api_collection_metadatas_equal: Callable[[ApiCollectionMetadata, ApiCollectionMetadata], None],
    assert_api_users_equal: Callable[[ApiUser, ApiUser], None],
) -> Callable[[ApiCollection, ApiCollection], None]:
    def _assert_api_collections_equal(api_collection_1: ApiCollection, api_collection_2: ApiCollection):
        assert api_collection_1
        assert api_collection_2
        assert isinstance(api_collection_1, ApiCollection)
        assert isinstance(api_collection_2, ApiCollection)

        assert id(api_collection_1) != id(api_collection_2)
        assert api_collection_1.model_dump() == api_collection_2.model_dump()

        assert_api_collection_metadatas_equal(api_collection_1.metadata, api_collection_2.metadata)

        assert len(api_collection_1.fleets) == len(api_collection_2.fleets)
        for i, pss_alliance in enumerate(api_collection_1.fleets):
            assert_api_alliances_equal(pss_alliance, api_collection_2.fleets[i])

        assert len(api_collection_1.users) == len(api_collection_2.users)
        for i, pss_user in enumerate(api_collection_1.users):
            assert_api_users_equal(pss_user, api_collection_2.users[i])

    return _assert_api_collections_equal


@pytest.fixture(scope="session")
def assert_api_collection_metadatas_equal() -> Callable[[ApiCollectionMetadata, ApiCollectionMetadata], None]:
    def _assert_api_collection_metadatas_equal(api_collection_metadata_1: ApiCollectionMetadata, api_collection_metadata_2: ApiCollectionMetadata):
        assert id(api_collection_metadata_1) != id(api_collection_metadata_2)
        assert api_collection_metadata_1.model_dump() == api_collection_metadata_2.model_dump()

    return _assert_api_collection_metadatas_equal


@pytest.fixture(scope="session")
def assert_api_users_equal() -> Callable[[ApiUser, ApiUser], None]:
    def _assert_api_users_equal(api_user_1: ApiUser, api_user_2: ApiUser):
        assert api_user_1 == api_user_2

    return _assert_api_users_equal


# Valid


@pytest.fixture(scope="session")
def assert_api_alliance_valid() -> Callable[[ApiAlliance], None]:
    def _assert_api_alliance_valid(api_alliance: ApiAlliance):
        assert api_alliance
        assert isinstance(api_alliance, tuple)
        assert len(api_alliance) == 8

    return _assert_api_alliance_valid


@pytest.fixture(scope="session")
def assert_api_collection_valid(
    assert_api_alliance_valid: Callable[[ApiAlliance], None],
    assert_api_collection_metadata_valid: Callable[[ApiCollectionMetadata], None],
    assert_api_user_valid: Callable[[ApiUser], None],
) -> Callable[[ApiCollection], None]:
    def _assert_api_collection_valid(api_collection: ApiCollection):
        assert api_collection
        assert isinstance(api_collection, ApiCollection)
        assert_api_collection_metadata_valid(api_collection.metadata)

        assert isinstance(api_collection.fleets, list)
        for fleet in api_collection.fleets:
            assert_api_alliance_valid(fleet)

        assert isinstance(api_collection.users, list)
        for user in api_collection.users:
            assert_api_user_valid(user)

    return _assert_api_collection_valid


@pytest.fixture(scope="session")
def assert_api_collection_metadata_valid() -> Callable[[ApiCollectionMetadata], None]:
    def _assert_api_collection_metadata_valid(api_collection_metadata: ApiCollectionMetadata):
        assert api_collection_metadata
        assert isinstance(api_collection_metadata, ApiCollectionMetadata)
        assert api_collection_metadata.timestamp.tzinfo == timezone.utc

    return _assert_api_collection_metadata_valid


@pytest.fixture(scope="session")
def assert_api_user_valid() -> Callable[[ApiUser], None]:
    def _assert_api_user_valid(api_user: ApiUser):
        assert api_user
        assert isinstance(api_user, tuple)
        assert len(api_user) == 20

    return _assert_api_user_valid
