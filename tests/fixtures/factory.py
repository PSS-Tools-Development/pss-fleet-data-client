from datetime import datetime, timezone

from pssapi.entities import Alliance as PssAlliance
from pssapi.entities import User as PssUser

from client import utils
from client.model import Collection, CollectionMetadata
from client.model.api import ApiAlliance, ApiCollection, ApiCollectionMetadata, ApiUser


# API objects


def create_api_alliance() -> ApiAlliance:
    return (1, "A1", 0, 0, 5000, 0, 1, 0)


def create_api_collection_9() -> ApiCollection:
    return ApiCollection(
        metadata=create_api_collection_metadata_9(),
        fleets=[create_api_alliance()],
        users=[
            create_api_user(),
        ],
    )


def create_api_collection_metadata_3() -> ApiCollectionMetadata:
    return ApiCollectionMetadata(
        collection_id=1,
        timestamp=datetime(2016, 1, 6, 23, 59),
        duration=11.2,
        fleet_count=1,
        user_count=1,
        tourney_running=False,
        schema_version=9,
        max_tournament_battle_attempts=6,
        data_version=3,
    )


def create_api_collection_metadata_9() -> ApiCollectionMetadata:
    result = create_api_collection_metadata_3()
    result.data_version = 9
    result.max_tournament_battle_attempts = 6
    return result


def create_api_user() -> ApiUser:
    return (
        1,
        "U1",
        1,
        1000,
        0,
        0,
        int((datetime(2016, 1, 6, 8, 12, 34) - datetime(2016, 1, 6)).total_seconds()),
        int((datetime(2016, 1, 6, 23, 58) - datetime(2016, 1, 6)).total_seconds()),
        int((datetime(2016, 1, 6, 23, 58) - datetime(2016, 1, 6)).total_seconds()),
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


# Client objects


def create_pss_alliance() -> PssAlliance:
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


def create_collection_9() -> Collection:
    return Collection(
        metadata=create_collection_metadata_9(),
        alliances=[create_pss_alliance()],
        users=[create_pss_user()],
    )


def create_collection_metadata_3() -> CollectionMetadata:
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


def create_collection_metadata_9() -> CollectionMetadata:
    result = create_collection_metadata_3()
    result.data_version = 9
    result.max_tournament_battle_attempts = 6
    return result


def create_pss_user() -> PssUser:
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
