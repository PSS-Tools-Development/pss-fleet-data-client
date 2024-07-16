from typing import Any, Callable

import pytest
import routes_test_cases

from client import PssFleetDataClient
from client.core.exceptions import (
    MissingAccessError,
    NonUniqueTimestampError,
    NotAuthenticatedError,
    SchemaVersionMismatch,
    UnsupportedMediaTypeError,
    UnsupportedSchemaError,
)
from client.models import Collection, CollectionMetadata


@pytest.mark.usefixtures("mock_response_collections_post_201")
async def test_upload_collection_201_from_file_path(
    upload_test_file_path: str,
    collection_metadata_9: Collection,
    test_client: PssFleetDataClient,
    assert_collection_metadata_valid: Callable[[CollectionMetadata], None],
    assert_collection_metadatas_equal: Callable[[CollectionMetadata, CollectionMetadata, bool, bool], None],
):
    collection_metadata_response = await test_client.upload_collection(upload_test_file_path)

    assert_collection_metadata_valid(collection_metadata_response)
    assert_collection_metadatas_equal(collection_metadata_9, collection_metadata_response)


@pytest.mark.usefixtures("mock_response_401")
async def test_upload_collection_401(
    upload_test_file_path: str,
    test_client: PssFleetDataClient,
):
    with pytest.raises(NotAuthenticatedError):
        _ = await test_client.upload_collection(upload_test_file_path)


@pytest.mark.usefixtures("mock_response_403")
async def test_upload_collection_403(
    upload_test_file_path: str,
    test_client: PssFleetDataClient,
):
    with pytest.raises(MissingAccessError):
        _ = await test_client.upload_collection(upload_test_file_path)


@pytest.mark.usefixtures("mock_response_collections_post_409_non_unique_timestamp")
async def test_upload_collection_409(
    upload_test_file_path: str,
    test_client: PssFleetDataClient,
):
    with pytest.raises(NonUniqueTimestampError):
        _ = await test_client.upload_collection(upload_test_file_path)


@pytest.mark.usefixtures("mock_response_post_415")
async def test_upload_collection_415(
    upload_test_file_path: str,
    test_client: PssFleetDataClient,
):
    with pytest.raises(UnsupportedMediaTypeError):
        _ = await test_client.upload_collection(upload_test_file_path)


@pytest.mark.usefixtures("mock_response_post_422_schema_version_mismatch")
async def test_upload_collection_422_schema_version_mismatch(
    upload_test_file_path: str,
    test_client: PssFleetDataClient,
):
    with pytest.raises(SchemaVersionMismatch):
        _ = await test_client.upload_collection(upload_test_file_path)


@pytest.mark.usefixtures("mock_response_post_422_unsupported_schema")
async def test_upload_collection_422_unsupported_schema(
    upload_test_file_path: str,
    test_client: PssFleetDataClient,
):
    with pytest.raises(UnsupportedSchemaError):
        _ = await test_client.upload_collection(upload_test_file_path)


@pytest.mark.parametrize(["value"], routes_test_cases.invalid_parameter_types("str"))
async def test_upload_collection_invalid_file_path_type(
    value: Any,
    test_client: PssFleetDataClient,
):
    with pytest.raises(TypeError):
        _ = await test_client.upload_collection(value)
