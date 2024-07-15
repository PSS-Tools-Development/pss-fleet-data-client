from typing import Callable

import pytest
from pssapi.entities import User as PssUser

from client import PssFleetDataClient
from client.model import Collection
from client.model.exceptions import CollectionNotFoundError, InvalidCollectionIdError


@pytest.mark.usefixtures("collection", "mock_response_collections_collectionId_users_get_200")
@pytest.mark.usefixtures("assert_collection_metadata_valid", "assert_collection_metadatas_equal")
async def test_get_top_100_users_from_collection_200(
    collection: Collection,
    test_client: PssFleetDataClient,
    assert_collection_metadata_valid: Callable[[Collection], None],
    assert_collection_metadatas_equal: Callable[[Collection, Collection, bool, bool], None],
    assert_pss_user_valid: Callable[[PssUser], None],
    assert_pss_users_equal: Callable[[PssUser, PssUser], None],
):
    response_collection, users = await test_client.get_top_100_users_from_collection(1)
    assert_collection_metadata_valid(response_collection)
    assert_collection_metadatas_equal(collection.metadata, response_collection)

    assert users
    assert isinstance(users, list)
    for user in users:
        assert_pss_user_valid(user)

    assert len(users) == len(collection.users)
    for user_1, user_2 in zip(users, collection.users, strict=True):
        assert_pss_users_equal(user_1, user_2)


@pytest.mark.usefixtures("collection", "mock_response_empty_collection_get_204")
async def test_get_top_100_users_from_collection_204(
    test_client: PssFleetDataClient,
):
    collection_response, users = await test_client.get_top_100_users_from_collection(1)
    assert collection_response is None
    assert not users
    assert isinstance(users, list)


@pytest.mark.usefixtures("mock_response_collection_not_found")
async def test_get_top_100_users_from_collection_404(test_client: PssFleetDataClient):
    with pytest.raises(CollectionNotFoundError):
        _ = await test_client.get_top_100_users_from_collection(1)


@pytest.mark.usefixtures("mock_response_collection_id_invalid")
async def test_get_top_100_users_from_collection_422(test_client: PssFleetDataClient):
    with pytest.raises(InvalidCollectionIdError):
        _ = await test_client.get_top_100_users_from_collection("f")
