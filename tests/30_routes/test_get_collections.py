from typing import Any, Callable

import pytest
import test_cases
import vcr
from pytest import FixtureRequest

from client import PssFleetDataClient
from client.core.exceptions import ApiError
from client.models import Collection


@pytest.mark.usefixtures("mock_response_get_collections_200")
async def test_get_collections_200(
    collection: Collection,
    test_client: PssFleetDataClient,
    assert_collection_valid: Callable[[Collection], None],
    assert_collections_equal: Callable[[Collection, Collection, bool, bool], None],
):
    response = await test_client.get_collections()
    assert response
    assert isinstance(response, list)

    assert_collection_valid(response[0], True, True)
    assert_collections_equal(collection, response[0], True, True)


@pytest.mark.usefixtures("mock_response_empty_collection_get_204")
async def test_get_collections_204(test_client: PssFleetDataClient):
    response = await test_client.get_collections()
    assert isinstance(response, list)
    assert len(response) == 0


@pytest.mark.vcr()
@pytest.mark.usefixtures("vcr_config_match_on")
@pytest.mark.parametrize(["parameters", "expected_exception"], test_cases.invalid_filter_parameters)
async def test_get_collections_422(
    parameters: dict[str, Any],
    expected_exception: ApiError,
    vcr_config_match_on: list[str],
    test_client: PssFleetDataClient,
    request: FixtureRequest,
):
    cassette_path = f"tests/30_routes/cassettes/test_get_422_{request.node.callspec.id}.yaml"

    with vcr.use_cassette(cassette_path, match_on=vcr_config_match_on):
        with pytest.raises(expected_exception):
            _ = await test_client.get_collections(**parameters)
