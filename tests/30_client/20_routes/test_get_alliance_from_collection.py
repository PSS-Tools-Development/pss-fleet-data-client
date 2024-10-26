from typing import Callable

import pytest
from pssapi.entities import Alliance as PssAlliance

from pss_fleet_data import PssFleetDataClient
from pss_fleet_data.core.exceptions import AllianceNotFoundError, CollectionNotFoundError, InvalidAllianceIdError, InvalidCollectionIdError
from pss_fleet_data.models import AllianceHistory


@pytest.mark.usefixtures("mock_response_collections_collectionId_alliances_allianceId_get_200")
async def test_get_alliance_from_collection_200(
    alliance_history: PssAlliance,
    test_client: PssFleetDataClient,
    assert_alliance_history_valid: Callable[[AllianceHistory], None],
    assert_alliance_histories_equal: Callable[[AllianceHistory, AllianceHistory], None],
):
    alliance_history_response = await test_client.get_alliance_from_collection(1, 1)

    assert_alliance_history_valid(alliance_history_response)
    assert_alliance_histories_equal(alliance_history, alliance_history_response)


@pytest.mark.usefixtures("mock_response_collections_collectionId_alliances_allianceId_get_200_with_members")
async def test_get_alliance_from_collection_200_with_members(
    alliance_history_with_members: PssAlliance,
    test_client: PssFleetDataClient,
    assert_alliance_history_valid: Callable[[AllianceHistory], None],
    assert_alliance_histories_equal: Callable[[AllianceHistory, AllianceHistory], None],
):
    alliance_history_response = await test_client.get_alliance_from_collection(1, 1)

    assert_alliance_history_valid(alliance_history_response)
    assert_alliance_histories_equal(alliance_history_response, alliance_history_with_members)


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
