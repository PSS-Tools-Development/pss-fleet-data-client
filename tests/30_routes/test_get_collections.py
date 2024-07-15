from typing import Any, Callable

import pytest
import test_cases

from client import PssFleetDataClient
from client.model import Collection
from client.model.exceptions import ApiError


@pytest.mark.usefixtures("collection", "mock_response_get_collections_200")
@pytest.mark.usefixtures("assert_collection_valid", "assert_collections_equal")
async def test_get_collections_200(
    collection: Collection,
    test_client: PssFleetDataClient,
    assert_collection_valid: Callable[[Collection], None],
    assert_collections_equal: Callable[[Collection, Collection], None],
):
    response = await test_client.get_collections()
    assert response
    assert isinstance(response, list)

    assert_collection_valid(response[0])
    assert_collections_equal(collection, response[0])


@pytest.mark.usefixtures("mock_response_get_collections_204")
async def test_get_collections_204(
    test_client: PssFleetDataClient,
):
    response = await test_client.get_collections()
    assert isinstance(response, list)
    assert len(response) == 0


@pytest.mark.vcr()
@pytest.mark.parametrize(["parameters", "expected_exception"], test_cases.invalid_filter_parameters)
async def test_get_collections_422(
    parameters: dict[str, Any],
    expected_exception: ApiError,
    test_client: PssFleetDataClient,
):
    with pytest.raises(expected_exception):
        _ = await test_client.get_collections(**parameters)
