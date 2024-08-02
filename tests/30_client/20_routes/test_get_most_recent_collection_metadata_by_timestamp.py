from datetime import datetime
from typing import Callable

import pytest

from pss_fleet_data import PssFleetDataClient
from pss_fleet_data.models import CollectionMetadata


@pytest.mark.usefixtures("patch_get_collections_successful_first_try")
async def test_get_most_recent_collection_by_timestamp_first_try(
    collection_metadata_9: CollectionMetadata,
    assert_collection_metadata_valid: Callable[[CollectionMetadata], None],
    assert_collection_metadatas_equal: Callable[[CollectionMetadata, CollectionMetadata], None],
    test_client: PssFleetDataClient,
):
    result = await test_client.get_most_recent_collection_metadata_by_timestamp(datetime(2024, 1, 1))

    assert_collection_metadata_valid(result)
    assert_collection_metadatas_equal(collection_metadata_9, result)


@pytest.mark.usefixtures("patch_get_collections_successful_second_try")
async def test_get_most_recent_collection_by_timestamp_second_try(
    collection_metadata_9: CollectionMetadata,
    assert_collection_metadata_valid: Callable[[CollectionMetadata], None],
    assert_collection_metadatas_equal: Callable[[CollectionMetadata, CollectionMetadata], None],
    test_client: PssFleetDataClient,
):
    result = await test_client.get_most_recent_collection_metadata_by_timestamp(datetime(2024, 1, 1))

    assert_collection_metadata_valid(result)
    assert_collection_metadatas_equal(collection_metadata_9, result)


@pytest.mark.usefixtures("patch_get_collections_successful_third_try")
async def test_get_most_recent_collection_by_timestamp_third_try(
    collection_metadata_9: CollectionMetadata,
    assert_collection_metadata_valid: Callable[[CollectionMetadata], None],
    assert_collection_metadatas_equal: Callable[[CollectionMetadata, CollectionMetadata], None],
    test_client: PssFleetDataClient,
):
    result = await test_client.get_most_recent_collection_metadata_by_timestamp(datetime(2024, 1, 1))

    assert_collection_metadata_valid(result)
    assert_collection_metadatas_equal(collection_metadata_9, result)


@pytest.mark.usefixtures("patch_get_collections_unsuccessful")
async def test_get_most_recent_collection_by_timestamp_unsuccessful(
    test_client: PssFleetDataClient,
):
    result = await test_client.get_most_recent_collection_metadata_by_timestamp(datetime(2024, 1, 1))

    assert result is None
