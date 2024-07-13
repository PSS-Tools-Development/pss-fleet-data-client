from datetime import timezone

import pytest
from pssapi.entities import Alliance as PssAlliance
from pssapi.entities import User as PssUser

from client.model import Collection, CollectionMetadata
from client.model.api import ApiAlliance, ApiCollection, ApiCollectionMetadata, ApiUser
from client.model.converters import ToAPI


@pytest.mark.usefixtures("pss_alliance")
def test_from_pss_alliance(pss_alliance: PssAlliance):
    api_alliance = ToAPI.from_pss_alliance(pss_alliance)

    _check_api_alliance(api_alliance)


@pytest.mark.usefixtures("collection")
def test_from_collection(collection: Collection):
    api_collection = ToAPI.from_collection(collection)

    _check_api_collection(api_collection)


@pytest.mark.usefixtures("collection_metadata_9")
def test_from_collection_metadata(collection_metadata_9: CollectionMetadata):
    api_collection_metadata = ToAPI.from_collection_metadata(collection_metadata_9)

    _check_api_collection_metadata(api_collection_metadata)


@pytest.mark.usefixtures("pss_user")
def test_from_pss_user(pss_user: PssUser):
    api_user = ToAPI.from_pss_user(pss_user)

    _check_api_user(api_user)


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
