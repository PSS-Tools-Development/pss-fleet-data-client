from typing import Callable

import pytest

from client import PssFleetDataClient
from client.model import Collection


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
