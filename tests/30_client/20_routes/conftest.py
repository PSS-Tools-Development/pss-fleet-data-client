from unittest.mock import AsyncMock

import pytest
from pytest import MonkeyPatch

from pss_fleet_data import PssFleetDataClient
from pss_fleet_data.models import Collection, CollectionMetadata


@pytest.fixture(scope="function")
def patch_get_collections_successful_first_try(collection_metadata_9: CollectionMetadata, monkeypatch: MonkeyPatch):
    mock_return_result_on_first_try = AsyncMock(side_effect=[[collection_metadata_9]])

    monkeypatch.setattr(PssFleetDataClient, PssFleetDataClient.get_collections.__name__, mock_return_result_on_first_try)


@pytest.fixture(scope="function")
def patch_get_collections_successful_second_try(collection_metadata_9: CollectionMetadata, monkeypatch: MonkeyPatch):
    mock_return_result_on_second_try = AsyncMock(side_effect=[[], [collection_metadata_9]])

    monkeypatch.setattr(PssFleetDataClient, PssFleetDataClient.get_collections.__name__, mock_return_result_on_second_try)


@pytest.fixture(scope="function")
def patch_get_collections_successful_third_try(collection_metadata_9: CollectionMetadata, monkeypatch: MonkeyPatch):
    mock_return_result_on_third_try = AsyncMock(side_effect=[[], [], [collection_metadata_9]])

    monkeypatch.setattr(PssFleetDataClient, PssFleetDataClient.get_collections.__name__, mock_return_result_on_third_try)


@pytest.fixture(scope="function")
def patch_get_collections_unsuccessful(monkeypatch: MonkeyPatch):
    mock_return_result_unsuccessful = AsyncMock(side_effect=[[], [], []])

    monkeypatch.setattr(PssFleetDataClient, PssFleetDataClient.get_collections.__name__, mock_return_result_unsuccessful)


@pytest.fixture(scope="function")
def patch_get_collection(collection: Collection, monkeypatch: MonkeyPatch):
    async def mock_get_collection(*args):
        return collection

    monkeypatch.setattr(PssFleetDataClient, PssFleetDataClient.get_collection.__name__, mock_get_collection)
