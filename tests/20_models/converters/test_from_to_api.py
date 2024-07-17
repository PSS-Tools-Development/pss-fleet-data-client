from typing import Callable

import pytest

from pss_fleet_data.models.api_models import ApiAlliance, ApiCollection, ApiCollectionMetadata, ApiUser
from pss_fleet_data.models.converters import FromAPI, ToAPI


@pytest.mark.usefixtures("api_alliance")
@pytest.mark.usefixtures("assert_api_alliance_valid")
def test_from_to_api_alliance(api_alliance: ApiAlliance, assert_api_alliance_valid: Callable[[ApiAlliance], None]):
    pss_alliance = FromAPI.to_pss_alliance(api_alliance)
    api_alliance_after = ToAPI.from_pss_alliance(pss_alliance)
    assert_api_alliance_valid(api_alliance_after)
    assert api_alliance == api_alliance_after


@pytest.mark.usefixtures("api_collection")
@pytest.mark.usefixtures("assert_api_collection_valid")
def test_from_to_api_collection(api_collection: ApiCollection, assert_api_collection_valid: Callable[[ApiCollection], None]):
    collection = FromAPI.to_collection(api_collection)
    api_collection_after = ToAPI.from_collection(collection)
    assert_api_collection_valid(api_collection_after)

    api_collection.metadata.collection_id = None
    assert api_collection.model_dump() == api_collection_after.model_dump()


@pytest.mark.usefixtures("api_collection_metadata_3")
@pytest.mark.usefixtures("assert_api_collection_metadata_valid")
def test_from_to_api_collection_metadata_3(
    api_collection_metadata_3: ApiCollectionMetadata, assert_api_collection_metadata_valid: Callable[[ApiCollectionMetadata], None]
):
    collection_metadata = FromAPI.to_collection_metadata(api_collection_metadata_3)
    api_collection_metadata_3_after = ToAPI.from_collection_metadata(collection_metadata)
    assert_api_collection_metadata_valid(api_collection_metadata_3_after)

    api_collection_metadata_3.collection_id = None
    assert api_collection_metadata_3.model_dump() == api_collection_metadata_3_after.model_dump()


@pytest.mark.usefixtures("api_collection_metadata_9")
@pytest.mark.usefixtures("assert_api_collection_metadata_valid")
def test_from_to_collection_metadata_9(
    api_collection_metadata_9: ApiCollectionMetadata, assert_api_collection_metadata_valid: Callable[[ApiCollectionMetadata], None]
):
    collection_metadata = FromAPI.to_collection_metadata(api_collection_metadata_9)
    api_collection_metadata_9_after = ToAPI.from_collection_metadata(collection_metadata)
    assert_api_collection_metadata_valid(api_collection_metadata_9_after)

    api_collection_metadata_9.collection_id = None
    assert api_collection_metadata_9.model_dump() == api_collection_metadata_9_after.model_dump()


@pytest.mark.usefixtures("api_user")
@pytest.mark.usefixtures("assert_api_user_valid")
def test_from_to_pss_user(api_user: ApiUser, assert_api_user_valid: Callable[[ApiUser], None]):
    pss_user = FromAPI.to_pss_user(api_user)
    api_user_after = ToAPI.from_pss_user(pss_user)
    assert_api_user_valid(api_user_after)

    assert api_user == api_user_after
