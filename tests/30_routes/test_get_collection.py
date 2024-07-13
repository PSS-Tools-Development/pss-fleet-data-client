from typing import Callable

import pytest

from client import PssFleetDataClient
from client.model import Collection
from client.model.exceptions import CollectionNotFoundError, InvalidCollectionIdError


@pytest.mark.usefixtures("collection", "mock_response_get_collection_200")
@pytest.mark.usefixtures("assert_collection_valid", "assert_collections_equal")
async def test_get_collection_200(
    collection: Collection,
    test_client: PssFleetDataClient,
    assert_collection_valid: Callable[[Collection], None],
    assert_collections_equal: Callable[[Collection, Collection], None],
):
    response = await test_client.get_collection(1)
    assert_collection_valid(response)
    assert_collections_equal(collection, response)


@pytest.mark.usefixtures("mock_response_get_collection_404")
async def test_get_collection_404(
    test_client: PssFleetDataClient,
):
    with pytest.raises(CollectionNotFoundError):
        _ = await test_client.get_collection(1)


@pytest.mark.usefixtures("mock_response_get_collection_422")
async def test_get_collection_422(
    test_client: PssFleetDataClient,
):
    with pytest.raises(InvalidCollectionIdError):
        _ = await test_client.get_collection("f")
