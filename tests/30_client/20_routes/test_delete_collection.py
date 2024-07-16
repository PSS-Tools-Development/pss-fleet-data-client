import pytest

from client import PssFleetDataClient
from client.core.exceptions import (
    CollectionNotDeletedError,
    CollectionNotFoundError,
    InvalidCollectionIdError,
    MissingAccessError,
    NotAuthenticatedError,
)


@pytest.mark.usefixtures("mock_response_empty_get_204")
async def test_delete_collection_204(test_client: PssFleetDataClient):
    response = await test_client.delete_collection(1)
    assert response is True


@pytest.mark.usefixtures("mock_response_401")
async def test_delete_collection_401(
    test_client: PssFleetDataClient,
):
    with pytest.raises(NotAuthenticatedError):
        _ = await test_client.delete_collection(1)


@pytest.mark.usefixtures("mock_response_403")
async def test_delete_collection_403(
    test_client: PssFleetDataClient,
):
    with pytest.raises(MissingAccessError):
        _ = await test_client.delete_collection(1)


@pytest.mark.usefixtures("mock_response_collection_not_found")
async def test_delete_collection_404(test_client: PssFleetDataClient):
    with pytest.raises(CollectionNotFoundError):
        _ = await test_client.delete_collection(1)


@pytest.mark.usefixtures("mock_response_collection_id_invalid")
async def test_delete_collection_422(test_client: PssFleetDataClient):
    with pytest.raises(InvalidCollectionIdError):
        _ = await test_client.delete_collection("f")


@pytest.mark.usefixtures("mock_response_collections_collectionId_delete_500")
async def test_delete_collection_500(test_client: PssFleetDataClient):
    with pytest.raises(CollectionNotDeletedError):
        _ = await test_client.delete_collection(1)
