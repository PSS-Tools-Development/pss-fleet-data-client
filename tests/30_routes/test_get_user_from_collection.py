from typing import Callable

import pytest

from client import PssAlliance, PssFleetDataClient, PssUser
from client.core.exceptions import CollectionNotFoundError, InvalidCollectionIdError, InvalidUserIdError, UserNotFoundError
from client.models import CollectionMetadata


@pytest.mark.usefixtures("mock_response_collections_collectionId_users_userId_get_200")
async def test_get_user_from_collection_200(
    pss_user: PssUser,
    collection_metadata_9: CollectionMetadata,
    test_client: PssFleetDataClient,
    assert_pss_user_valid: Callable[[PssUser], None],
    assert_pss_users_equal: Callable[[PssUser, PssUser, bool, bool], None],
    assert_collection_metadata_valid: Callable[[CollectionMetadata], None],
    assert_collection_metadatas_equal: Callable[[CollectionMetadata, CollectionMetadata, bool, bool], None],
):
    user_history = await test_client.get_user_from_collection(1, 1)

    assert_collection_metadata_valid(user_history.collection)
    assert_collection_metadatas_equal(collection_metadata_9, user_history.collection)

    assert_pss_user_valid(user_history.user)
    assert_pss_users_equal(pss_user, user_history.user)

    assert user_history.alliance is None


@pytest.mark.usefixtures("mock_response_collections_collectionId_users_userId_get_200_with_fleet")
async def test_get_user_from_collection_200_with_fleet(
    collection_metadata_9: CollectionMetadata,
    pss_alliance: PssUser,
    pss_user: PssUser,
    test_client: PssFleetDataClient,
    assert_collection_metadata_valid: Callable[[CollectionMetadata], None],
    assert_collection_metadatas_equal: Callable[[CollectionMetadata, CollectionMetadata, bool, bool], None],
    assert_pss_alliance_valid: Callable[[PssAlliance], None],
    assert_pss_alliances_equal: Callable[[PssAlliance, PssAlliance, bool, bool], None],
    assert_pss_user_valid: Callable[[PssUser], None],
    assert_pss_users_equal: Callable[[PssUser, PssUser, bool, bool], None],
):
    user_history = await test_client.get_user_from_collection(1, 1)

    assert_collection_metadata_valid(user_history.collection)
    assert_collection_metadatas_equal(collection_metadata_9, user_history.collection)

    assert_pss_user_valid(user_history.user)
    assert_pss_users_equal(pss_user, user_history.user)

    assert_pss_alliance_valid(user_history.alliance)
    assert_pss_alliances_equal(pss_alliance, user_history.alliance)


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
