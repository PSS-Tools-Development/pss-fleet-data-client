from typing import Callable

import pytest

from client import PssFleetDataClient
from client.core.exceptions import CollectionNotFoundError, InvalidCollectionIdError
from client.models import Collection


@pytest.mark.usefixtures("mock_response_collections_collectionId_get_200")
async def test_get_collection_200(
    collection: Collection,
    test_client: PssFleetDataClient,
    assert_collection_valid: Callable[[Collection], None],
    assert_collections_equal: Callable[[Collection, Collection, bool, bool], None],
):
    response = await test_client.get_collection(1)
    assert_collection_valid(response, True, True)
    assert_collections_equal(collection, response, True, True)


@pytest.mark.usefixtures("mock_response_collection_not_found")
async def test_get_collection_404(test_client: PssFleetDataClient):
    with pytest.raises(CollectionNotFoundError):
        _ = await test_client.get_collection(1)


@pytest.mark.usefixtures("mock_response_collection_id_invalid")
async def test_get_collection_422(test_client: PssFleetDataClient):
    with pytest.raises(InvalidCollectionIdError):
        _ = await test_client.get_collection("f")
