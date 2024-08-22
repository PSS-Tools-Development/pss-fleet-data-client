from typing import Callable

import pytest
from pssapi.entities import Alliance as PssAlliance

from pss_fleet_data.models import Collection
from pss_fleet_data.models.api_models import ApiAlliance, ApiCollection, ApiCollectionMetadata, ApiUser
from pss_fleet_data.models.converters import FromAPI


@pytest.mark.usefixtures("api_alliance")
@pytest.mark.usefixtures("assert_pss_alliance_valid")
def test_to_pss_alliance(api_alliance: ApiAlliance, assert_pss_alliance_valid: Callable[[PssAlliance], None]):
    pss_alliance = FromAPI.to_pss_alliance(api_alliance)
    assert_pss_alliance_valid(pss_alliance)

    pss_alliance = FromAPI.to_pss_alliance(None)
    assert pss_alliance is None


@pytest.mark.usefixtures("api_collection")
@pytest.mark.usefixtures("assert_collection_valid")
def test_to_collection(api_collection: ApiCollection, assert_collection_valid: Callable[[Collection], None]):
    collection = FromAPI.to_collection(api_collection)
    assert_collection_valid(collection, True, True)


@pytest.mark.usefixtures("api_collection_metadata_3")
@pytest.mark.usefixtures("assert_collection_metadata_valid")
def test_to_collection_metadata_3(api_collection_metadata_3: ApiCollectionMetadata, assert_collection_metadata_valid: Callable[[Collection], None]):
    collection_metadata = FromAPI.to_collection_metadata(api_collection_metadata_3)
    assert_collection_metadata_valid(collection_metadata)


@pytest.mark.usefixtures("api_collection_metadata_9")
@pytest.mark.usefixtures("assert_collection_metadata_valid")
def test_to_collection_metadata_9(api_collection_metadata_9: ApiCollectionMetadata, assert_collection_metadata_valid: Callable[[Collection], None]):
    collection_metadata = FromAPI.to_collection_metadata(api_collection_metadata_9)
    assert_collection_metadata_valid(collection_metadata)


@pytest.mark.usefixtures("api_user")
@pytest.mark.usefixtures("assert_pss_user_valid")
def test_to_pss_user(api_user: ApiUser, assert_pss_user_valid: Callable[[PssAlliance], None]):
    pss_user = FromAPI.to_pss_user(api_user)
    assert_pss_user_valid(pss_user)

    pss_user = FromAPI.to_pss_user(None)
    assert pss_user is None
