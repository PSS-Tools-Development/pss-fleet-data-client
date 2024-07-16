from typing import Callable, Optional

import pytest
from pssapi.entities import Alliance as PssAlliance
from pssapi.entities import User as PssUser

from client.models import AllianceHistory, Collection, CollectionMetadata


# Equal


@pytest.fixture(scope="function")
def assert_alliance_histories_equal(
    assert_collection_metadatas_equal: Callable[[CollectionMetadata, CollectionMetadata], None],
    assert_pss_alliances_equal: Callable[[PssAlliance, PssAlliance], None],
    assert_pss_users_equal: Callable[[PssUser, PssUser], None],
) -> Callable[[Collection], None]:
    def _assert_alliance_histories_equal(alliance_history_1: AllianceHistory, alliance_history_2: AllianceHistory):
        assert alliance_history_1
        assert alliance_history_2
        assert isinstance(alliance_history_1, AllianceHistory)
        assert isinstance(alliance_history_2, AllianceHistory)

        assert id(alliance_history_1) != id(alliance_history_2)
        assert alliance_history_1.model_dump() == alliance_history_2.model_dump()

        assert_collection_metadatas_equal(alliance_history_1.collection, alliance_history_2.collection)
        assert_pss_alliances_equal(alliance_history_1.alliance, alliance_history_2.alliance)

        assert len(alliance_history_1.users) == len(alliance_history_2.users)
        for i, pss_user in enumerate(alliance_history_1.users):
            assert_pss_users_equal(pss_user, alliance_history_2.users[i])

    return _assert_alliance_histories_equal


@pytest.fixture(scope="function")
def assert_collections_equal(
    assert_collection_metadatas_equal: Callable[[CollectionMetadata, CollectionMetadata], None],
    assert_pss_alliances_equal: Callable[[PssAlliance, PssAlliance], None],
    assert_pss_users_equal: Callable[[PssUser, PssUser], None],
) -> Callable[[Collection, Collection, Optional[bool], Optional[bool]], None]:
    def _assert_collections_equal(
        collection_1: Collection, collection_2: Collection, skip_fleets: Optional[bool] = False, skip_users: Optional[bool] = False
    ):
        assert collection_1
        assert collection_2
        assert isinstance(collection_1, Collection)
        assert isinstance(collection_2, Collection)

        assert id(collection_1) != id(collection_2)
        assert collection_1.model_dump() == collection_2.model_dump()

        assert_collection_metadatas_equal(collection_1.metadata, collection_2.metadata)

        if not skip_fleets:
            assert len(collection_1.alliances) == len(collection_2.alliances)
            for i, pss_alliance in enumerate(collection_1.alliances):
                assert_pss_alliances_equal(pss_alliance, collection_2.alliances[i])

        if not skip_users:
            assert len(collection_1.users) == len(collection_2.users)
            for i, pss_user in enumerate(collection_1.users):
                assert_pss_users_equal(pss_user, collection_2.users[i])

    return _assert_collections_equal


@pytest.fixture(scope="function")
def assert_collection_metadatas_equal() -> Callable[[CollectionMetadata, CollectionMetadata], None]:
    def _assert_collection_metadatas_equal(collection_metadata_1: CollectionMetadata, collection_metadata_2: CollectionMetadata):
        assert id(collection_metadata_1) != id(collection_metadata_2)
        assert collection_metadata_1.model_dump() == collection_metadata_2.model_dump()

    return _assert_collection_metadatas_equal


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


# Valid


@pytest.fixture(scope="function")
def assert_alliance_history_valid(
    assert_collection_metadata_valid: Callable[[CollectionMetadata], None],
    assert_pss_alliance_valid: Callable[[PssAlliance], None],
) -> Callable[[Collection], None]:
    def _assert_alliance_history_valid(alliance_history: AllianceHistory):
        assert alliance_history
        assert isinstance(alliance_history, AllianceHistory)

        assert_collection_metadata_valid(alliance_history.collection)
        assert_pss_alliance_valid(alliance_history.alliance)

        assert not alliance_history.users
        assert isinstance(alliance_history.users, list)

    return _assert_alliance_history_valid


@pytest.fixture(scope="function")
def assert_alliance_history_with_members_valid(
    assert_collection_metadata_valid: Callable[[CollectionMetadata], None],
    assert_pss_alliance_valid: Callable[[PssAlliance], None],
    assert_pss_user_valid: Callable[[PssUser], None],
) -> Callable[[Collection], None]:
    def _assert_alliance_history_valid(alliance_history: AllianceHistory):
        assert alliance_history
        assert isinstance(alliance_history, AllianceHistory)

        assert_collection_metadata_valid(alliance_history.collection)
        assert_pss_alliance_valid(alliance_history.alliance)

        assert alliance_history.users
        assert isinstance(alliance_history.users, list)
        for user in alliance_history.users:
            assert_pss_user_valid(user)

    return _assert_alliance_history_valid


@pytest.fixture(scope="function")
def assert_collection_valid(assert_collection_metadata_valid: Callable[[CollectionMetadata], None]) -> Callable[[Collection, bool, bool], None]:
    def _assert_collection_valid(collection: Collection, assert_fleets: bool, assert_users: bool):
        assert collection
        assert isinstance(collection, Collection)

        assert_collection_metadata_valid(collection.metadata)

        if assert_fleets:
            assert collection.alliances
            assert isinstance(collection.alliances, list)
            for alliance in collection.alliances:
                assert alliance
                assert isinstance(alliance, PssAlliance)

        if assert_users:
            assert collection.users
            assert isinstance(collection.users, list)
            for user in collection.users:
                assert user
                assert isinstance(user, PssUser)

    return _assert_collection_valid


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

        if metadata.data_version >= 9:
            assert metadata.max_tournament_battle_attempts is not None

    return _assert_collection_metadata_valid


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
