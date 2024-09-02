from pathlib import Path
from typing import Any, Callable, Union

import pytest
import routes_test_cases

from pss_fleet_data import PssFleetDataClient
from pss_fleet_data.core.exceptions import (
    ConflictError,
    MissingAccessError,
    NotAuthenticatedError,
    SchemaVersionMismatch,
    UnsupportedMediaTypeError,
    UnsupportedSchemaError,
)
from pss_fleet_data.models import Collection, CollectionMetadata


@pytest.mark.parametrize("file_path", routes_test_cases.upload_test_file_paths)
@pytest.mark.usefixtures("mock_response_collections_post_201")
async def test_update_collection_200_from_file_path(
    file_path: Union[Path, str],
    collection_metadata_9: Collection,
    test_client: PssFleetDataClient,
    assert_collection_metadata_valid: Callable[[CollectionMetadata], None],
    assert_collection_metadatas_equal: Callable[[CollectionMetadata, CollectionMetadata, bool, bool], None],
):
    collection_metadata_response = await test_client.update_collection(1, file_path)

    assert_collection_metadata_valid(collection_metadata_response)
    assert_collection_metadatas_equal(collection_metadata_9, collection_metadata_response)


@pytest.mark.usefixtures("mock_response_401")
async def test_update_collection_401(
    upload_test_file_path: str,
    test_client: PssFleetDataClient,
):
    with pytest.raises(NotAuthenticatedError):
        _ = await test_client.update_collection(1, upload_test_file_path)


@pytest.mark.usefixtures("mock_response_403")
async def test_update_collection_403(
    upload_test_file_path: str,
    test_client: PssFleetDataClient,
):
    with pytest.raises(MissingAccessError):
        _ = await test_client.update_collection(1, upload_test_file_path)


@pytest.mark.usefixtures("mock_response_collections_post_409_timestamps_not_match")
async def test_update_collection_409(
    upload_test_file_path: str,
    test_client: PssFleetDataClient,
):
    with pytest.raises(ConflictError):
        _ = await test_client.update_collection(1, upload_test_file_path)


@pytest.mark.usefixtures("mock_response_post_415")
async def test_update_collection_415(
    upload_test_file_path: str,
    test_client: PssFleetDataClient,
):
    with pytest.raises(UnsupportedMediaTypeError):
        _ = await test_client.update_collection(1, upload_test_file_path)


@pytest.mark.usefixtures("mock_response_post_422_schema_version_mismatch")
async def test_update_collection_422_schema_version_mismatch(
    upload_test_file_path: str,
    test_client: PssFleetDataClient,
):
    with pytest.raises(SchemaVersionMismatch):
        _ = await test_client.update_collection(1, upload_test_file_path)


@pytest.mark.usefixtures("mock_response_post_422_unsupported_schema")
async def test_update_collection_422_unsupported_schema(
    upload_test_file_path: str,
    test_client: PssFleetDataClient,
):
    with pytest.raises(UnsupportedSchemaError):
        _ = await test_client.update_collection(1, upload_test_file_path)


@pytest.mark.parametrize(["value"], routes_test_cases.invalid_parameter_types("str"))
async def test_update_collection_invalid_file_path_type(
    value: Any,
    test_client: PssFleetDataClient,
):
    with pytest.raises(TypeError):
        _ = await test_client.update_collection(1, value)
