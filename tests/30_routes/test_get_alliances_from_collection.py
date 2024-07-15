from typing import Callable

import pytest
from pssapi.entities import Alliance as PssAlliance

from client import PssFleetDataClient
from client.model import Collection
from client.model.exceptions import CollectionNotFoundError, InvalidCollectionIdError


@pytest.mark.usefixtures("collection", "mock_response_collections_collectionId_alliances_get_200")
@pytest.mark.usefixtures("assert_collection_metadata_valid", "assert_collection_metadatas_equal")
async def test_get_alliances_from_collection_200(
    collection: Collection,
    test_client: PssFleetDataClient,
    assert_collection_metadata_valid: Callable[[Collection], None],
    assert_collection_metadatas_equal: Callable[[Collection, Collection, bool, bool], None],
    assert_pss_alliance_valid: Callable[[PssAlliance], None],
    assert_pss_alliances_equal: Callable[[PssAlliance, PssAlliance], None],
):
    collection_response, alliances = await test_client.get_alliances_from_collection(1)
    assert_collection_metadata_valid(collection_response)
    assert_collection_metadatas_equal(collection.metadata, collection_response)

    assert alliances
    assert isinstance(alliances, list)
    for alliance in alliances:
        assert_pss_alliance_valid(alliance)

    assert len(alliances) == len(collection.alliances)
    for i, alliance in enumerate(alliances):
        assert_pss_alliances_equal(alliance, collection.alliances[i])


@pytest.mark.usefixtures("mock_response_collection_not_found")
async def test_get_alliances_from_collection_404(test_client: PssFleetDataClient):
    with pytest.raises(CollectionNotFoundError):
        _ = await test_client.get_alliances_from_collection(1)


@pytest.mark.usefixtures("mock_response_collection_id_invalid")
async def test_get_alliances_from_collection_422(test_client: PssFleetDataClient):
    with pytest.raises(InvalidCollectionIdError):
        _ = await test_client.get_alliances_from_collection("f")
