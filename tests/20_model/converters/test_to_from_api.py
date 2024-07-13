from typing import Callable

import pytest
from pssapi.entities import Alliance as PssAlliance
from pssapi.entities import User as PssUser

from client.model import Collection, CollectionMetadata
from client.model.converters import FromAPI, ToAPI


@pytest.mark.usefixtures("pss_alliance")
@pytest.mark.usefixtures("assert_pss_alliance_valid", "assert_pss_alliances_equal")
def test_to_from_api_alliance(
    pss_alliance: PssAlliance,
    assert_pss_alliance_valid: Callable[[PssAlliance], None],
    assert_pss_alliances_equal: Callable[[PssAlliance, PssAlliance], None],
):
    api_alliance = ToAPI.from_pss_alliance(pss_alliance)
    pss_alliance_after = FromAPI.to_pss_alliance(api_alliance)

    assert_pss_alliance_valid(pss_alliance_after)
    assert_pss_alliances_equal(pss_alliance, pss_alliance_after)


@pytest.mark.usefixtures("collection")
@pytest.mark.usefixtures("assert_collection_valid", "assert_collections_equal")
def test_to_from_api_collection(
    collection: Collection, assert_collection_valid: Callable[[Collection], None], assert_collections_equal: Callable[[Collection, Collection], None]
):
    api_collection = ToAPI.from_collection(collection)
    collection_after = FromAPI.to_collection(api_collection)

    assert_collection_valid(collection_after)

    collection.metadata.collection_id = None
    assert_collections_equal(collection, collection_after)


@pytest.mark.usefixtures("collection_metadata_9")
@pytest.mark.usefixtures("assert_collection_metadata_valid", "assert_collection_metadatas_equal")
def test_to_from_api_collection_metadata(
    collection_metadata_9: CollectionMetadata,
    assert_collection_metadata_valid: Callable[[CollectionMetadata], None],
    assert_collection_metadatas_equal: Callable[[CollectionMetadata, CollectionMetadata], None],
):
    api_collection_metadata = ToAPI.from_collection_metadata(collection_metadata_9)
    collection_metadata_9_after = FromAPI.to_collection_metadata(api_collection_metadata)

    assert_collection_metadata_valid(collection_metadata_9_after)

    collection_metadata_9.collection_id = None
    assert_collection_metadatas_equal(collection_metadata_9, collection_metadata_9_after)


@pytest.mark.usefixtures("pss_user")
@pytest.mark.usefixtures("assert_pss_user_valid", "assert_pss_users_equal")
def test_to_from_api_user(
    pss_user: PssUser, assert_pss_user_valid: Callable[[PssUser], None], assert_pss_users_equal: Callable[[PssUser, PssUser], None]
):
    api_user = ToAPI.from_pss_user(pss_user)
    pss_user_after = FromAPI.to_pss_user(api_user)

    assert_pss_user_valid(pss_user_after)
    assert_pss_users_equal(pss_user, pss_user_after)
