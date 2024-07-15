from typing import Callable

import pytest
from pssapi.entities import Alliance as PssAlliance

from client import PssFleetDataClient
from client.model import CollectionMetadata
from client.model.exceptions import AllianceNotFoundError, CollectionNotFoundError, InvalidAllianceIdError, InvalidCollectionIdError


@pytest.mark.usefixtures("pss_alliance", "mock_response_collections_collectionId_alliances_allianceId_get_200")
async def test_get_alliance_from_collection_200(
    pss_alliance: PssAlliance,
    collection_metadata_9: CollectionMetadata,
    test_client: PssFleetDataClient,
    assert_pss_alliance_valid: Callable[[PssAlliance], None],
    assert_pss_alliances_equal: Callable[[PssAlliance, PssAlliance, bool, bool], None],
    assert_collection_metadata_valid: Callable[[CollectionMetadata], None],
    assert_collection_metadatas_equal: Callable[[CollectionMetadata, CollectionMetadata, bool, bool], None],
):
    collection_metadata, alliance = await test_client.get_alliance_from_collection(1, 1)

    assert_collection_metadata_valid(collection_metadata)
    assert_collection_metadatas_equal(collection_metadata_9, collection_metadata)

    assert_pss_alliance_valid(alliance)
    assert_pss_alliances_equal(pss_alliance, alliance)


@pytest.mark.usefixtures("pss_alliance", "mock_response_collections_collectionId_alliances_allianceId_get_200_with_members")
async def test_get_alliance_from_collection_200_with_members(
    pss_alliance: PssAlliance,
    collection_metadata_9: CollectionMetadata,
    test_client: PssFleetDataClient,
    assert_pss_alliance_valid: Callable[[PssAlliance], None],
    assert_pss_alliances_equal: Callable[[PssAlliance, PssAlliance, bool, bool], None],
    assert_collection_metadata_valid: Callable[[CollectionMetadata], None],
    assert_collection_metadatas_equal: Callable[[CollectionMetadata, CollectionMetadata, bool, bool], None],
):
    collection_metadata, alliance = await test_client.get_alliance_from_collection(1, 1)

    assert_collection_metadata_valid(collection_metadata)
    assert_collection_metadatas_equal(collection_metadata_9, collection_metadata)

    assert_pss_alliance_valid(alliance)
    assert_pss_alliances_equal(pss_alliance, alliance)


@pytest.mark.usefixtures("mock_response_alliance_not_found")
async def test_get_alliance_from_collection_alliance_not_found_404(test_client: PssFleetDataClient):
    with pytest.raises(AllianceNotFoundError):
        _ = await test_client.get_alliance_from_collection(1, 9001)


@pytest.mark.usefixtures("mock_response_collection_not_found")
async def test_get_alliance_from_collection_collection_not_found_404(test_client: PssFleetDataClient):
    with pytest.raises(CollectionNotFoundError):
        _ = await test_client.get_alliance_from_collection(9001, 1)
        _ = await test_client.get_alliance_from_collection(9001, 9001)


@pytest.mark.usefixtures("mock_response_alliance_id_invalid")
async def test_get_alliance_from_collection_alliance_id_invalid_422(test_client: PssFleetDataClient):
    with pytest.raises(InvalidAllianceIdError):
        _ = await test_client.get_alliance_from_collection(1, "f")


@pytest.mark.usefixtures("mock_response_collection_id_invalid")
async def test_get_alliance_from_collection_collection_id_invalid_422(test_client: PssFleetDataClient):
    with pytest.raises(InvalidCollectionIdError):
        _ = await test_client.get_alliance_from_collection("f", 1)
        _ = await test_client.get_alliance_from_collection("f", "f")
