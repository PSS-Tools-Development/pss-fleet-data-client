import pytest
from pssapi.entities import Alliance as PssAlliance
from pssapi.entities import User as PssUser

from client.model import AllianceHistory, Collection, CollectionMetadata, UserHistory

from .factory import create_collection, create_collection_metadata_3, create_collection_metadata_9, create_pss_alliance, create_pss_user


# Client objects


@pytest.fixture(scope="function")
def pss_alliance() -> PssAlliance:
    return create_pss_alliance()


@pytest.fixture(scope="function")
def alliance_history(collection_metadata_9: CollectionMetadata, pss_alliance: PssAlliance, pss_user: PssUser) -> AllianceHistory:
    return AllianceHistory(
        collection=collection_metadata_9,
        alliance=pss_alliance,
        users=[pss_user],
    )


@pytest.fixture(scope="function")
def collection() -> Collection:
    return create_collection()


@pytest.fixture(scope="function")
def collection_metadata_3() -> CollectionMetadata:
    return create_collection_metadata_3()


@pytest.fixture(scope="function")
def collection_metadata_9() -> Collection:
    return create_collection_metadata_9()


@pytest.fixture(scope="function")
def pss_user() -> PssUser:
    return create_pss_user()


@pytest.fixture(scope="function")
def user_history(collection_metadata_9: CollectionMetadata, pss_alliance: PssAlliance, pss_user: PssUser) -> UserHistory:
    return UserHistory(
        collection=collection_metadata_9,
        user=pss_user,
        alliance=pss_alliance,
    )
