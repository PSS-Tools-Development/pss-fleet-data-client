from datetime import datetime, timezone
from typing import Callable

import pytest
from pssapi.entities import Alliance as PssAlliance
from pssapi.entities import User as PssUser

from client import utils
from client.model import AllianceHistory, Collection, CollectionMetadata, UserHistory
from client.model.api import ApiAlliance, ApiAllianceHistory, ApiCollection, ApiCollectionMetadata, ApiUser, ApiUserHistory


### Fixtures

## Objects

# API objects


@pytest.fixture(scope="function")
def api_alliance() -> ApiAlliance:
    return _create_api_alliance()


@pytest.fixture(scope="function")
def api_alliance_history() -> ApiAllianceHistory:
    return (_create_api_collection(), _create_api_alliance())


@pytest.fixture(scope="function")
def api_collection() -> ApiCollection:
    return _create_api_collection()


@pytest.fixture(scope="function")
def api_collection_metadata_3() -> ApiCollectionMetadata:
    return _create_api_collection_metadata_3()


@pytest.fixture(scope="function")
def api_collection_metadata_9() -> ApiCollectionMetadata:
    result = _create_api_collection_metadata_3()
    result.data_version = 9
    result.max_tournament_battle_attempts = 6
    return result


@pytest.fixture(scope="function")
def api_user() -> ApiUser:
    return _create_api_user()


@pytest.fixture(scope="function")
def api_user_history() -> ApiUserHistory:
    return (_create_api_collection(), _create_api_user())


# Client objects


@pytest.fixture(scope="function")
def pss_alliance() -> PssAlliance:
    return _create_pss_alliance()


@pytest.fixture(scope="function")
def alliance_history() -> AllianceHistory:
    return (_create_collection(), _create_pss_alliance())


@pytest.fixture(scope="function")
def collection() -> Collection:
    return _create_collection()


@pytest.fixture(scope="function")
def collection_metadata_3() -> Collection:
    return _create_collection_metadata_3()


@pytest.fixture(scope="function")
def collection_metadata_9() -> Collection:
    result = _create_collection_metadata_3()
    result.data_version = 9
    result.max_tournament_battle_attempts = 6
    return result


@pytest.fixture(scope="function")
def pss_user() -> PssUser:
    return _create_pss_user()


@pytest.fixture(scope="function")
def user_history() -> UserHistory:
    return (_create_collection(), _create_pss_user())


## Assert

# API entities


@pytest.fixture(scope="session")
def assert_api_alliance_valid() -> Callable[[ApiAlliance], None]:
    def _assert_api_alliance_valid(api_alliance: ApiAlliance):
        assert api_alliance
        assert isinstance(api_alliance, tuple)
        assert len(api_alliance) == 8

    return _assert_api_alliance_valid


@pytest.fixture(scope="session")
def assert_api_alliances_equal() -> Callable[[ApiAlliance, ApiAlliance], None]:
    def _assert_api_alliances_equal(api_alliance_1: ApiAlliance, api_alliance_2: ApiAlliance):
        assert api_alliance_1 == api_alliance_2

    return _assert_api_alliances_equal


@pytest.fixture(scope="session")
def assert_api_collection_valid(
    assert_api_alliance_valid: Callable[[ApiAlliance], None],
    assert_api_collection_metadata_valid: Callable[[ApiCollectionMetadata], None],
    assert_api_user_valid: Callable[[ApiUser], None],
) -> Callable[[ApiCollection], None]:
    def _assert_api_collection_valid(api_collection: ApiCollection):
        assert api_collection
        assert isinstance(api_collection, ApiCollection)
        assert_api_collection_metadata_valid(api_collection.metadata)

        assert isinstance(api_collection.fleets, list)
        for fleet in api_collection.fleets:
            assert_api_alliance_valid(fleet)

        assert isinstance(api_collection.users, list)
        for user in api_collection.users:
            assert_api_user_valid(user)

    return _assert_api_collection_valid


@pytest.fixture(scope="session")
def assert_api_collections_equal(
    assert_api_alliances_equal: Callable[[ApiAlliance, ApiAlliance], None],
    assert_api_collection_metadatas_equal: Callable[[ApiCollectionMetadata, ApiCollectionMetadata], None],
    assert_api_users_equal: Callable[[ApiUser, ApiUser], None],
) -> Callable[[ApiCollection, ApiCollection], None]:
    def _assert_api_collections_equal(api_collection_1: ApiCollection, api_collection_2: ApiCollection):
        assert api_collection_1
        assert api_collection_2
        assert isinstance(api_collection_1, ApiCollection)
        assert isinstance(api_collection_2, ApiCollection)

        assert id(api_collection_1) != id(api_collection_2)
        assert api_collection_1.model_dump() == api_collection_2.model_dump()

        assert_api_collection_metadatas_equal(api_collection_1.metadata, api_collection_2.metadata)

        assert len(api_collection_1.fleets) == len(api_collection_2.fleets)
        for i, pss_alliance in enumerate(api_collection_1.fleets):
            assert_api_alliances_equal(pss_alliance, api_collection_2.fleets[i])

        assert len(api_collection_1.users) == len(api_collection_2.users)
        for i, pss_user in enumerate(api_collection_1.users):
            assert_api_users_equal(pss_user, api_collection_2.users[i])

    return _assert_api_collections_equal


@pytest.fixture(scope="session")
def assert_api_collection_metadata_valid() -> Callable[[ApiCollectionMetadata], None]:
    def _assert_api_collection_metadata_valid(api_collection_metadata: ApiCollectionMetadata):
        assert api_collection_metadata
        assert isinstance(api_collection_metadata, ApiCollectionMetadata)
        assert api_collection_metadata.timestamp.tzinfo == timezone.utc

    return _assert_api_collection_metadata_valid


@pytest.fixture(scope="session")
def assert_api_collection_metadatas_equal() -> Callable[[ApiCollectionMetadata, ApiCollectionMetadata], None]:
    def _assert_api_collection_metadatas_equal(api_collection_metadata_1: ApiCollectionMetadata, api_collection_metadata_2: ApiCollectionMetadata):
        assert id(api_collection_metadata_1) != id(api_collection_metadata_2)
        assert api_collection_metadata_1.model_dump() == api_collection_metadata_2.model_dump()

    return _assert_api_collection_metadatas_equal


@pytest.fixture(scope="session")
def assert_api_user_valid() -> Callable[[ApiUser], None]:
    def _assert_api_user_valid(api_user: ApiUser):
        assert api_user
        assert isinstance(api_user, tuple)
        assert len(api_user) == 20

    return _assert_api_user_valid


@pytest.fixture(scope="session")
def assert_api_users_equal() -> Callable[[ApiUser, ApiUser], None]:
    def _assert_api_users_equal(api_user_1: ApiUser, api_user_2: ApiUser):
        assert api_user_1 == api_user_2

    return _assert_api_users_equal


# Local entities


@pytest.fixture(scope="function")
def assert_collection_valid(assert_collection_metadata_valid: Callable[[CollectionMetadata], None]) -> Callable[[Collection], None]:
    def _assert_collection_valid(collection: Collection):
        assert collection
        assert isinstance(collection, Collection)

        assert_collection_metadata_valid(collection.metadata)

        assert collection.alliances
        assert isinstance(collection.alliances, list)
        for alliance in collection.alliances:
            assert alliance
            assert isinstance(alliance, PssAlliance)

        assert collection.users
        assert isinstance(collection.users, list)
        for user in collection.users:
            assert user
            assert isinstance(user, PssUser)

    return _assert_collection_valid


@pytest.fixture(scope="function")
def assert_collections_equal(
    assert_collection_metadatas_equal: Callable[[CollectionMetadata, CollectionMetadata], None],
    assert_pss_alliances_equal: Callable[[PssAlliance, PssAlliance], None],
    assert_pss_users_equal: Callable[[PssUser, PssUser], None],
) -> Callable[[Collection, Collection], None]:
    def _assert_collections_equal(collection_1: Collection, collection_2: Collection):
        assert collection_1
        assert collection_2
        assert isinstance(collection_1, Collection)
        assert isinstance(collection_2, Collection)

        assert id(collection_1) != id(collection_2)
        assert collection_1.model_dump() == collection_2.model_dump()

        assert_collection_metadatas_equal(collection_1.metadata, collection_2.metadata)

        assert len(collection_1.alliances) == len(collection_2.alliances)
        for i, pss_alliance in enumerate(collection_1.alliances):
            assert_pss_alliances_equal(pss_alliance, collection_2.alliances[i])

        assert len(collection_1.users) == len(collection_2.users)
        for i, pss_user in enumerate(collection_1.users):
            assert_pss_users_equal(pss_user, collection_2.users[i])

    return _assert_collections_equal


@pytest.fixture(scope="function")
def assert_collection_metadata_valid() -> Callable[[CollectionMetadata], None]:
    def _assert_collection_metadata_valid(metadata: CollectionMetadata):
        assert metadata.timestamp is not None
        assert metadata.duration is not None
        assert metadata.fleet_count is not None
        assert metadata.user_count is not None
        assert metadata.tournament_running is not None
        assert metadata.schema_version is not None
        assert metadata.data_version is not None

        if metadata.data_version == 9:
            assert metadata.max_tournament_battle_attempts is not None

    return _assert_collection_metadata_valid


@pytest.fixture(scope="function")
def assert_collection_metadatas_equal() -> Callable[[CollectionMetadata, CollectionMetadata], None]:
    def _assert_collection_metadatas_equal(collection_metadata_1: CollectionMetadata, collection_metadata_2: CollectionMetadata):
        assert id(collection_metadata_1) != id(collection_metadata_2)
        assert collection_metadata_1.model_dump() == collection_metadata_2.model_dump()

    return _assert_collection_metadatas_equal


@pytest.fixture(scope="session")
def assert_pss_alliance_valid() -> Callable[[PssAlliance], None]:
    def _assert_pss_alliance_valid(pss_alliance: PssAlliance):
        assert pss_alliance
        assert isinstance(pss_alliance, PssAlliance)

        assert pss_alliance.alliance_id is not None
        assert pss_alliance.alliance_name is not None
        assert pss_alliance.score is not None
        assert pss_alliance.division_design_id is not None
        assert pss_alliance.trophy is not None
        assert pss_alliance.championship_score is not None
        assert pss_alliance.number_of_members is not None
        assert pss_alliance.number_of_approved_members is not None

    return _assert_pss_alliance_valid


@pytest.fixture(scope="function")
def assert_pss_alliances_equal() -> Callable[[PssAlliance, PssAlliance], None]:
    def _assert_pss_alliance_valids_equal(pss_alliance_1: PssAlliance, pss_alliance_2: PssAlliance):
        assert pss_alliance_1
        assert pss_alliance_2
        assert isinstance(pss_alliance_1, PssAlliance)
        assert isinstance(pss_alliance_2, PssAlliance)
        assert id(pss_alliance_1) != id(pss_alliance_2)

        assert pss_alliance_1.alliance_id == pss_alliance_2.alliance_id
        assert pss_alliance_1.alliance_name == pss_alliance_2.alliance_name
        assert pss_alliance_1.score == pss_alliance_2.score
        assert pss_alliance_1.division_design_id == pss_alliance_2.division_design_id
        assert pss_alliance_1.trophy == pss_alliance_2.trophy
        assert pss_alliance_1.championship_score == pss_alliance_2.championship_score
        assert pss_alliance_1.number_of_members == pss_alliance_2.number_of_members
        assert pss_alliance_1.number_of_approved_members == pss_alliance_2.number_of_approved_members

    return _assert_pss_alliance_valids_equal


@pytest.fixture(scope="session")
def assert_pss_user_valid() -> Callable[[PssUser], None]:
    def _assert_pss_user_valid(pss_user: PssUser):
        assert pss_user
        assert isinstance(pss_user, PssUser)

        assert pss_user.id is not None
        assert pss_user.name is not None
        assert pss_user.alliance_id is not None
        assert pss_user.trophy is not None
        assert pss_user.alliance_score is not None
        assert pss_user.alliance_membership is not None
        assert pss_user.alliance_join_date is not None
        assert pss_user.last_login_date is not None
        assert pss_user.crew_donated is not None
        assert pss_user.crew_received is not None
        assert pss_user.pvp_attack_wins is not None
        assert pss_user.pvp_attack_losses is not None
        assert pss_user.pvp_attack_draws is not None
        assert pss_user.pvp_defence_wins is not None
        assert pss_user.pvp_defence_losses is not None
        assert pss_user.pvp_defence_draws is not None
        assert pss_user.championship_score is not None
        assert pss_user.highest_trophy is not None
        assert pss_user.tournament_bonus_score is not None

    return _assert_pss_user_valid


@pytest.fixture(scope="function")
def assert_pss_users_equal() -> Callable[[PssUser, PssUser], None]:
    def _assert_pss_users_equal(pss_user_1: PssUser, pss_user_2: PssUser):
        assert pss_user_1
        assert pss_user_2
        assert isinstance(pss_user_1, PssUser)
        assert isinstance(pss_user_2, PssUser)
        assert id(pss_user_1) != id(pss_user_2)

        assert pss_user_1.id == pss_user_2.id
        assert pss_user_1.name == pss_user_2.name
        assert pss_user_1.alliance_id == pss_user_2.alliance_id
        assert pss_user_1.trophy == pss_user_2.trophy
        assert pss_user_1.alliance_score == pss_user_2.alliance_score
        assert pss_user_1.alliance_membership == pss_user_2.alliance_membership
        assert pss_user_1.alliance_join_date == pss_user_2.alliance_join_date
        assert pss_user_1.last_login_date == pss_user_2.last_login_date
        assert pss_user_1.crew_donated == pss_user_2.crew_donated
        assert pss_user_1.crew_received == pss_user_2.crew_received
        assert pss_user_1.pvp_attack_wins == pss_user_2.pvp_attack_wins
        assert pss_user_1.pvp_attack_losses == pss_user_2.pvp_attack_losses
        assert pss_user_1.pvp_attack_draws == pss_user_2.pvp_attack_draws
        assert pss_user_1.pvp_defence_wins == pss_user_2.pvp_defence_wins
        assert pss_user_1.pvp_defence_losses == pss_user_2.pvp_defence_losses
        assert pss_user_1.pvp_defence_draws == pss_user_2.pvp_defence_draws
        assert pss_user_1.championship_score == pss_user_2.championship_score
        assert pss_user_1.highest_trophy == pss_user_2.highest_trophy
        assert pss_user_1.tournament_bonus_score == pss_user_2.tournament_bonus_score

    return _assert_pss_users_equal


## Helpers

# API objects


def _create_api_alliance() -> ApiAlliance:
    return (1, "A1", 0, 0, 5000, 0, 1, 0)


def _create_api_collection() -> ApiCollection:
    return ApiCollection(
        metadata=_create_api_collection_metadata_3(),
        fleets=[_create_api_alliance()],
        users=[
            _create_api_user(),
        ],
    )


def _create_api_collection_metadata_3() -> ApiCollectionMetadata:
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


def _create_api_user() -> ApiUser:
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


def _create_pss_alliance() -> PssAlliance:
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


def _create_collection() -> Collection:
    return Collection(
        metadata=_create_collection_metadata_3(),
        alliances=[_create_pss_alliance()],
        users=[_create_pss_user()],
    )


def _create_collection_metadata_3() -> CollectionMetadata:
    return CollectionMetadata(
        collection_id=1,
        timestamp=datetime(2016, 1, 6, 23, 59, tzinfo=timezone.utc),
        duration=11.2,
        fleet_count=1,
        user_count=1,
        tournament_running=False,
        schema_version=9,
        max_tournament_battle_attempts=6,
        data_version=3,
    )


def _create_pss_user() -> PssUser:
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
