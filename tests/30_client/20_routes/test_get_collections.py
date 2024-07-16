from typing import Any, Callable

import pytest
import test_cases
import vcr
from pytest import FixtureRequest

from client import PssFleetDataClient
from client.core.exceptions import ApiError
from client.models import CollectionMetadata


@pytest.mark.usefixtures("mock_response_get_collections_200")
async def test_get_collections_200(
    collection_metadata_9: CollectionMetadata,
    test_client: PssFleetDataClient,
    assert_collection_metadata_valid: Callable[[CollectionMetadata], None],
    assert_collection_metadatas_equal: Callable[[CollectionMetadata, CollectionMetadata, bool, bool], None],
):
    collection_metadatas = await test_client.get_collections()
    assert collection_metadatas
    assert isinstance(collection_metadatas, list)

    assert_collection_metadata_valid(collection_metadatas[0])
    assert_collection_metadatas_equal(collection_metadata_9, collection_metadatas[0])


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
    cassette_path = f"tests/cassettes/test_get_422_{request.node.callspec.id}.yaml"

    with vcr.use_cassette(cassette_path, match_on=vcr_config_match_on):
        with pytest.raises(expected_exception):
            _ = await test_client.get_collections(**parameters)
