from typing import Callable

import pytest
from pssapi.entities import Alliance as PssAlliance
from pssapi.entities import User as PssUser

from client.models import Collection, CollectionMetadata
from client.models.api_models import ApiAlliance, ApiCollection, ApiCollectionMetadata, ApiUser
from client.models.converters import ToAPI


@pytest.mark.usefixtures("pss_alliance")
@pytest.mark.usefixtures("assert_api_alliance_valid")
def test_from_pss_alliance(pss_alliance: PssAlliance, assert_api_alliance_valid: Callable[[ApiAlliance], None]):
    api_alliance = ToAPI.from_pss_alliance(pss_alliance)

    assert_api_alliance_valid(api_alliance)


@pytest.mark.usefixtures("collection")
@pytest.mark.usefixtures("assert_api_collection_valid")
def test_from_collection(collection: Collection, assert_api_collection_valid: Callable[[ApiCollection], None]):
    api_collection = ToAPI.from_collection(collection)

    assert_api_collection_valid(api_collection)


@pytest.mark.usefixtures("collection_metadata_9")
@pytest.mark.usefixtures("assert_api_collection_metadata_valid")
def test_from_collection_metadata(
    collection_metadata_9: CollectionMetadata, assert_api_collection_metadata_valid: Callable[[ApiCollectionMetadata], None]
):
    api_collection_metadata = ToAPI.from_collection_metadata(collection_metadata_9)

    assert_api_collection_metadata_valid(api_collection_metadata)


@pytest.mark.usefixtures("pss_user")
@pytest.mark.usefixtures("assert_api_user_valid")
def test_from_pss_user(pss_user: PssUser, assert_api_user_valid: Callable[[ApiUser], None]):
    api_user = ToAPI.from_pss_user(pss_user)

    assert_api_user_valid(api_user)
