from typing import Any, Callable

import pytest
import test_cases
import vcr
from pytest import FixtureRequest

from client import PssFleetDataClient
from client.model import Collection
from client.model.exceptions import AllianceNotFoundError, CollectionNotFoundError, InvalidAllianceIdError, InvalidCollectionIdError


@pytest.mark.usefixtures("alliance", "mock_response_collections_collectionId_alliances_allianceId_get_200")
@pytest.mark.usefixtures("assert_collection_valid", "assert_collections_equal")
async def test_get_alliance_from_collection_200(
    alliance: Collection,
    test_client: PssFleetDataClient,
    assert_pss_alliance_valid: Callable[[Collection], None],
    assert_pss_alliances_equal: Callable[[Collection, Collection, bool, bool], None],
):
    response = await test_client.get_alliance_from_collection(1, 1)
    assert_pss_alliance_valid(response)
    assert_pss_alliances_equal(alliance, response)


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
