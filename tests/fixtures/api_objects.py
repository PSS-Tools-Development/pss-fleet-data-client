from datetime import datetime, timezone
from typing import Callable

import pytest

from client.core import utils
from client.models.api_models import ApiAlliance, ApiAllianceHistory, ApiCollection, ApiCollectionMetadata, ApiUser, ApiUserHistory


@pytest.fixture(scope="function")
def api_alliance() -> ApiAlliance:
    return (1, "A1", 0, 0, 5000, 0, 1, 0)


@pytest.fixture(scope="function")
def api_alliance_history(api_collection_metadata_9: ApiCollectionMetadata, api_alliance: ApiAlliance) -> ApiAllianceHistory:
    return ApiAllianceHistory(
        collection=api_collection_metadata_9,
        fleet=api_alliance,
        users=[],
    )


@pytest.fixture(scope="function")
def api_alliance_history_with_members(
    api_collection_metadata_9: ApiCollectionMetadata, api_alliance: ApiAlliance, api_user: ApiUser
) -> ApiAllianceHistory:
    return ApiAllianceHistory(
        collection=api_collection_metadata_9,
        fleet=api_alliance,
        users=[api_user],
    )


@pytest.fixture(scope="function")
def api_collection(api_collection_metadata_9: ApiCollectionMetadata, api_alliance: ApiAlliance, api_user: ApiUser) -> ApiCollection:
    return ApiCollection(
        metadata=api_collection_metadata_9,
        fleets=[api_alliance],
        users=[
            api_user,
        ],
    )


@pytest.fixture(scope="function")
def api_collection_with_fleets(api_collection_metadata_9: ApiCollectionMetadata, api_alliance: ApiAlliance) -> ApiCollection:
    return ApiCollection(
        metadata=api_collection_metadata_9,
        fleets=[api_alliance],
    )


@pytest.fixture(scope="function")
def api_collection_with_users(api_collection_metadata_9: ApiCollectionMetadata, api_user: ApiUser) -> ApiCollection:
    return ApiCollection(
        metadata=api_collection_metadata_9,
        users=[api_user],
    )


@pytest.fixture(scope="function")
def api_collection_metadata_3() -> ApiCollectionMetadata:
    return ApiCollectionMetadata(
        collection_id=1,
        timestamp=datetime(2016, 1, 6, 23, 59, tzinfo=timezone.utc),
        duration=11.2,
        fleet_count=1,
        user_count=1,
        tourney_running=False,
        schema_version=9,
        max_tournament_battle_attempts=6,
        data_version=3,
    )


@pytest.fixture(scope="function")
def api_collection_metadata_9(api_collection_metadata_3: ApiCollectionMetadata) -> ApiCollectionMetadata:
    api_collection_metadata_3.data_version = 9
    api_collection_metadata_3.max_tournament_battle_attempts = 6
    return api_collection_metadata_3


@pytest.fixture(scope="function")
def api_user() -> ApiUser:
    return (
        1,
        "U1",
        1,
        1000,
        0,
        0,
        utils.convert_datetime_to_seconds(datetime(2016, 1, 6, 8, 12, 34)),
        utils.convert_datetime_to_seconds(datetime(2016, 1, 6, 23, 58)),
        utils.convert_datetime_to_seconds(datetime(2016, 1, 6, 23, 58)),
        0,
        0,
        5,
        2,
        1,
        1,
        8,
        0,
        0,
        1000,
        0,
    )


@pytest.fixture(scope="function")
def api_user_history(api_collection_metadata_9: Callable[[], ApiCollectionMetadata], api_user: ApiUser) -> ApiUserHistory:
    return ApiUserHistory(
        collection=api_collection_metadata_9,
        user=api_user,
        fleet=None,
    )


@pytest.fixture(scope="function")
def api_user_history_with_fleet(
    api_collection_metadata_9: Callable[[], ApiCollectionMetadata], api_alliance: ApiAlliance, api_user: ApiUser
) -> ApiUserHistory:
    return ApiUserHistory(
        collection=api_collection_metadata_9,
        user=api_user,
        fleet=api_alliance,
    )
