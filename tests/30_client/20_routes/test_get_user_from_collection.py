from typing import Callable

import pytest

from pss_fleet_data import PssFleetDataClient
from pss_fleet_data.core.exceptions import CollectionNotFoundError, InvalidCollectionIdError, InvalidUserIdError, UserNotFoundError
from pss_fleet_data.models import UserHistory


@pytest.mark.usefixtures("mock_response_collections_collectionId_users_userId_get_200")
async def test_get_user_from_collection_200(
    user_history: UserHistory,
    test_client: PssFleetDataClient,
    assert_user_history_valid: Callable[[UserHistory], None],
    assert_user_histories_equal: Callable[[UserHistory, UserHistory], None],
):
    user_history_response = await test_client.get_user_from_collection(1, 1)

    assert_user_history_valid(user_history_response)
    assert_user_histories_equal(user_history, user_history_response)


@pytest.mark.usefixtures("mock_response_collections_collectionId_users_userId_get_200_with_fleet")
async def test_get_user_from_collection_200_with_fleet(
    user_history_with_alliance: UserHistory,
    test_client: PssFleetDataClient,
    assert_user_history_with_alliance_valid: Callable[[UserHistory], None],
    assert_user_histories_equal: Callable[[UserHistory, UserHistory], None],
):
    user_history_response = await test_client.get_user_from_collection(1, 1)

    assert_user_history_with_alliance_valid(user_history_response)
    assert_user_histories_equal(user_history_with_alliance, user_history_response)


@pytest.mark.usefixtures("mock_response_collection_not_found")
async def test_get_user_from_collection_collection_not_found_404(test_client: PssFleetDataClient):
    with pytest.raises(CollectionNotFoundError):
        _ = await test_client.get_user_from_collection(9001, 1)
        _ = await test_client.get_user_from_collection(9001, 9001)


@pytest.mark.usefixtures("mock_response_user_not_found")
async def test_get_user_from_collection_user_not_found_404(test_client: PssFleetDataClient):
    with pytest.raises(UserNotFoundError):
        _ = await test_client.get_user_from_collection(1, 9001)


@pytest.mark.usefixtures("mock_response_collection_id_invalid")
async def test_get_user_from_collection_collection_id_invalid_422(test_client: PssFleetDataClient):
    with pytest.raises(InvalidCollectionIdError):
        _ = await test_client.get_user_from_collection("f", 1)
        _ = await test_client.get_user_from_collection("f", "f")


@pytest.mark.usefixtures("mock_response_user_id_invalid")
async def test_get_user_from_collection_user_id_invalid_422(test_client: PssFleetDataClient):
    with pytest.raises(InvalidUserIdError):
        _ = await test_client.get_user_from_collection(1, "f")
