from typing import Callable

import pytest
from pssapi.entities import User as PssUser

from client import PssFleetDataClient
from client.model import CollectionMetadata
from client.model.exceptions import CollectionNotFoundError, InvalidCollectionIdError, InvalidUserIdError, UserNotFoundError


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
    collection_metadata, user = await test_client.get_user_from_collection(1, 1)

    assert_collection_metadata_valid(collection_metadata)
    assert_collection_metadatas_equal(collection_metadata_9, collection_metadata)

    assert_pss_user_valid(user)
    assert_pss_users_equal(pss_user, user)


@pytest.mark.usefixtures("mock_response_collections_collectionId_users_userId_get_200_with_fleet")
async def test_get_user_from_collection_200_with_fleet(
    pss_user: PssUser,
    collection_metadata_9: CollectionMetadata,
    test_client: PssFleetDataClient,
    assert_pss_user_valid: Callable[[PssUser], None],
    assert_pss_users_equal: Callable[[PssUser, PssUser, bool, bool], None],
    assert_collection_metadata_valid: Callable[[CollectionMetadata], None],
    assert_collection_metadatas_equal: Callable[[CollectionMetadata, CollectionMetadata, bool, bool], None],
):
    collection_metadata, user = await test_client.get_user_from_collection(1, 1)

    assert_collection_metadata_valid(collection_metadata)
    assert_collection_metadatas_equal(collection_metadata_9, collection_metadata)

    assert_pss_user_valid(user)
    assert_pss_users_equal(pss_user, user)


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
