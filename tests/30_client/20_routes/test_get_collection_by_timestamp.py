from datetime import datetime
from typing import Callable

import pytest

from client import PssFleetDataClient
from client.models import CollectionMetadata


@pytest.mark.usefixtures("patch_get_collections_successful_first_try")
@pytest.mark.usefixtures("patch_get_collection")
async def test_get_most_recent_collection_by_timestamp_first_try(
    collection: CollectionMetadata,
    assert_collection_valid: Callable[[CollectionMetadata, bool, bool], None],
    assert_collections_equal: Callable[[CollectionMetadata, CollectionMetadata, bool, bool], None],
    test_client: PssFleetDataClient,
):
    result = await test_client.get_most_recent_collection_by_timestamp(datetime(2024, 1, 1))

    assert_collection_valid(result, True, True)
    assert_collections_equal(collection, result, True, True)


@pytest.mark.usefixtures("patch_get_collections_successful_second_try")
@pytest.mark.usefixtures("patch_get_collection")
async def test_get_most_recent_collection_by_timestamp_second_try(
    collection: CollectionMetadata,
    assert_collection_valid: Callable[[CollectionMetadata, bool, bool], None],
    assert_collections_equal: Callable[[CollectionMetadata, CollectionMetadata, bool, bool], None],
    test_client: PssFleetDataClient,
):
    result = await test_client.get_most_recent_collection_by_timestamp(datetime(2024, 1, 1))

    assert_collection_valid(result, True, True)
    assert_collections_equal(collection, result, True, True)


@pytest.mark.usefixtures("patch_get_collections_successful_third_try")
@pytest.mark.usefixtures("patch_get_collection")
async def test_get_most_recent_collection_by_timestamp_third_try(
    collection: CollectionMetadata,
    assert_collection_valid: Callable[[CollectionMetadata, bool, bool], None],
    assert_collections_equal: Callable[[CollectionMetadata, CollectionMetadata, bool, bool], None],
    test_client: PssFleetDataClient,
):
    result = await test_client.get_most_recent_collection_by_timestamp(datetime(2024, 1, 1))

    assert_collection_valid(result, True, True)
    assert_collections_equal(collection, result, True, True)


@pytest.mark.usefixtures("patch_get_collections_unsuccessful")
async def test_get_most_recent_collection_by_timestamp_unsuccessful(
    test_client: PssFleetDataClient,
):
    result = await test_client.get_most_recent_collection_by_timestamp(datetime(2024, 1, 1))

    assert result is None
