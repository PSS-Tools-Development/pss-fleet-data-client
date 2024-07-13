from datetime import timezone

import pytest

from client.model.api import ApiAlliance, ApiCollection, ApiCollectionMetadata, ApiUser
from client.model.converters import FromAPI, ToAPI


@pytest.mark.usefixtures("api_alliance")
def test_from_to_api_alliance(api_alliance: ApiAlliance):
    pss_alliance = FromAPI.to_pss_alliance(api_alliance)
    api_alliance_after = ToAPI.from_pss_alliance(pss_alliance)
    _check_api_alliance(api_alliance_after)
    assert api_alliance == api_alliance_after


@pytest.mark.usefixtures("api_collection")
def test_from_to_api_collection(api_collection: ApiCollection):
    collection = FromAPI.to_collection(api_collection)
    api_collection_after = ToAPI.from_collection(collection)
    _check_api_collection(api_collection_after)

    api_collection.metadata.collection_id = None
    assert api_collection.model_dump() == api_collection_after.model_dump()


@pytest.mark.usefixtures("api_collection_metadata_3")
def test_from_to_api_collection_metadata_3(api_collection_metadata_3: ApiCollectionMetadata):
    collection_metadata = FromAPI.to_collection_metadata(api_collection_metadata_3)
    api_collection_metadata_3_after = ToAPI.from_collection_metadata(collection_metadata)
    _check_api_collection_metadata(api_collection_metadata_3_after)

    api_collection_metadata_3.collection_id = None
    assert api_collection_metadata_3.model_dump() == api_collection_metadata_3_after.model_dump()


@pytest.mark.usefixtures("api_collection_metadata_9")
def test_to_collection_metadata_9(api_collection_metadata_9: ApiCollectionMetadata):
    collection_metadata = FromAPI.to_collection_metadata(api_collection_metadata_9)
    api_collection_metadata_9_after = ToAPI.from_collection_metadata(collection_metadata)
    _check_api_collection_metadata(api_collection_metadata_9_after)

    api_collection_metadata_9.collection_id = None
    assert api_collection_metadata_9.model_dump() == api_collection_metadata_9_after.model_dump()


@pytest.mark.usefixtures("api_user")
def test_to_pss_user(api_user: ApiUser):
    pss_user = FromAPI.to_pss_user(api_user)
    api_user_after = ToAPI.from_pss_user(pss_user)
    _check_api_user(api_user_after)

    assert api_user == api_user_after


# Helpers


def _check_api_alliance(api_alliance: ApiAlliance):
    assert api_alliance
    assert isinstance(api_alliance, tuple)
    assert len(api_alliance) == 8


def _check_api_collection(api_collection: ApiCollection):
    assert api_collection
    assert isinstance(api_collection, ApiCollection)
    _check_api_collection_metadata(api_collection.metadata)

    assert isinstance(api_collection.fleets, list)
    for fleet in api_collection.fleets:
        _check_api_alliance(fleet)

    assert isinstance(api_collection.users, list)
    for user in api_collection.users:
        _check_api_user(user)


def _check_api_collection_metadata(api_collection_metadata: ApiCollectionMetadata):
    assert api_collection_metadata
    assert isinstance(api_collection_metadata, ApiCollectionMetadata)
    assert api_collection_metadata.timestamp.tzinfo == timezone.utc


def _check_api_user(api_user: ApiUser):
    assert api_user
    assert isinstance(api_user, tuple)
    assert len(api_user) == 20
