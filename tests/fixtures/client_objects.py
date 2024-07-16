from datetime import datetime, timezone

import pytest
from pssapi.entities import Alliance as PssAlliance
from pssapi.entities import User as PssUser

from client import utils
from client.model import AllianceHistory, Collection, CollectionMetadata, UserHistory


# Client objects


@pytest.fixture(scope="function")
def pss_alliance() -> PssAlliance:
    return PssAlliance(
        {
            "AllianceId": 1,
            "AllianceName": "A1",
            "Score": 0,
            "DivisionDesignId": 0,
            "Trophy": 5000,
            "ChampionshipScore": 0,
            "NumberOfMembers": 1,
            "NumberOfApprovedMembers": 0,
        }
    )


@pytest.fixture(scope="function")
def alliance_history(collection_metadata_9: CollectionMetadata, pss_alliance: PssAlliance) -> AllianceHistory:
    return AllianceHistory(
        collection=collection_metadata_9,
        alliance=pss_alliance,
        users=[],
    )


@pytest.fixture(scope="function")
def alliance_history_with_members(collection_metadata_9: CollectionMetadata, pss_alliance: PssAlliance, pss_user: PssUser) -> AllianceHistory:
    return AllianceHistory(
        collection=collection_metadata_9,
        alliance=pss_alliance,
        users=[pss_user],
    )


@pytest.fixture(scope="function")
def collection(collection_metadata_9: CollectionMetadata, pss_alliance: PssAlliance, pss_user: PssUser) -> Collection:
    return Collection(
        metadata=collection_metadata_9,
        alliances=[pss_alliance],
        users=[pss_user],
    )


@pytest.fixture(scope="function")
def collection_metadata_3() -> CollectionMetadata:
    return CollectionMetadata(
        collection_id=1,
        timestamp=datetime(2016, 1, 6, 23, 59, tzinfo=timezone.utc),
        duration=11.2,
        fleet_count=1,
        user_count=1,
        tournament_running=False,
        schema_version=9,
        data_version=3,
    )


@pytest.fixture(scope="function")
def collection_metadata_9(collection_metadata_3: CollectionMetadata) -> Collection:
    collection_metadata_3.data_version = 9
    collection_metadata_3.max_tournament_battle_attempts = 6
    return collection_metadata_3


@pytest.fixture(scope="function")
def pss_user() -> PssUser:
    return PssUser(
        {
            "Id": 1,
            "Name": "U1",
            "AllianceId": 1,
            "Trophy": 1000,
            "AllianceScore": 0,
            "AllianceMembership": "FleetAdmiral",
            "AllianceJoinDate": utils.format_datetime(datetime(2016, 1, 6, 8, 12, 34)),
            "LastLoginDate": utils.format_datetime(datetime(2016, 1, 6, 23, 58)),
            "LastHeartBeatDate": utils.format_datetime(datetime(2016, 1, 6, 23, 58)),
            "CrewDonated": 0,
            "CrewReceived": 0,
            "PVPAttackWins": 5,
            "PVPAttackLosses": 2,
            "PVPAttackDraws": 1,
            "PVPDefenceWins": 1,
            "PVPDefenceLosses": 8,
            "PVPDefenceDraws": 0,
            "ChampionshipScore": 0,
            "HighestTrophy": 1000,
            "TournamentBonusScore": 0,
        }
    )


@pytest.fixture(scope="function")
def user_history(collection_metadata_9: CollectionMetadata, pss_alliance: PssAlliance, pss_user: PssUser) -> UserHistory:
    return UserHistory(
        collection=collection_metadata_9,
        user=pss_user,
        alliance=pss_alliance,
    )
