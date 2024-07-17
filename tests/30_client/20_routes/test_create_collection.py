from typing import Callable

import pytest

from pss_fleet_data import PssFleetDataClient
from pss_fleet_data.core.exceptions import (
    MissingAccessError,
    NonUniqueTimestampError,
    NotAuthenticatedError,
    SchemaVersionMismatch,
    UnsupportedMediaTypeError,
    UnsupportedSchemaError,
)
from pss_fleet_data.models import Collection, CollectionMetadata


@pytest.mark.usefixtures("mock_response_collections_post_201")
async def test_create_collection_201(
    collection: Collection,
    collection_metadata_9: CollectionMetadata,
    test_client: PssFleetDataClient,
    assert_collection_metadata_valid: Callable[[CollectionMetadata], None],
    assert_collection_metadatas_equal: Callable[[CollectionMetadata, CollectionMetadata, bool, bool], None],
):
    collection_metadata_response = await test_client.create_collection(collection)

    assert_collection_metadata_valid(collection_metadata_response)
    assert_collection_metadatas_equal(collection_metadata_9, collection_metadata_response)


@pytest.mark.usefixtures("mock_response_401")
async def test_create_collection_401(
    collection: Collection,
    test_client: PssFleetDataClient,
):
    with pytest.raises(NotAuthenticatedError):
        _ = await test_client.create_collection(collection)


@pytest.mark.usefixtures("mock_response_403")
async def test_create_collection_403(
    collection: Collection,
    test_client: PssFleetDataClient,
):
    with pytest.raises(MissingAccessError):
        _ = await test_client.create_collection(collection)


@pytest.mark.usefixtures("mock_response_collections_post_409_non_unique_timestamp")
async def test_create_collection_409(
    collection: Collection,
    test_client: PssFleetDataClient,
):
    with pytest.raises(NonUniqueTimestampError):
        _ = await test_client.create_collection(collection)


@pytest.mark.usefixtures("mock_response_post_415")
async def test_create_collection_415(
    collection: Collection,
    test_client: PssFleetDataClient,
):
    with pytest.raises(UnsupportedMediaTypeError):
        _ = await test_client.create_collection(collection)


@pytest.mark.usefixtures("mock_response_post_422_schema_version_mismatch")
async def test_create_collection_422_schema_version_mismatch(
    collection: Collection,
    test_client: PssFleetDataClient,
):
    with pytest.raises(SchemaVersionMismatch):
        _ = await test_client.create_collection(collection)


@pytest.mark.usefixtures("mock_response_post_422_unsupported_schema")
async def test_create_collection_422_unsupported_schema(
    collection: Collection,
    test_client: PssFleetDataClient,
):
    with pytest.raises(UnsupportedSchemaError):
        _ = await test_client.create_collection(collection)
