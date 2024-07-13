import pytest
from pssapi.entities import Alliance as PssAlliance
from pssapi.entities import User as PssUser

from client.model import Collection, CollectionMetadata
from client.model.converters import FromAPI, ToAPI


@pytest.mark.usefixtures("pss_alliance")
def test_to_from_api_alliance(pss_alliance: PssAlliance):
    api_alliance = ToAPI.from_pss_alliance(pss_alliance)
    pss_alliance_after = FromAPI.to_pss_alliance(api_alliance)

    _assert_pss_alliance(pss_alliance_after)
    _assert_pss_alliances_equal(pss_alliance, pss_alliance_after)


@pytest.mark.usefixtures("collection")
def test_to_from_api_collection(collection: Collection):
    api_collection = ToAPI.from_collection(collection)
    collection_after = FromAPI.to_collection(api_collection)

    _assert_collection(collection_after)

    collection.metadata.collection_id = None
    assert id(collection) != id(collection_after)
    assert collection.model_dump() == collection_after.model_dump()


@pytest.mark.usefixtures("collection_metadata_9")
def test_to_from_api_collection_metadata(collection_metadata_9: CollectionMetadata):
    api_collection_metadata = ToAPI.from_collection_metadata(collection_metadata_9)
    collection_metadata_9_after = FromAPI.to_collection_metadata(api_collection_metadata)

    _assert_collection_metadata(collection_metadata_9_after)

    collection_metadata_9.collection_id = None
    assert id(collection_metadata_9) != id(collection_metadata_9_after)
    assert collection_metadata_9.model_dump() == collection_metadata_9_after.model_dump()


@pytest.mark.usefixtures("pss_user")
def test_to_from_api_user(pss_user: PssUser):
    api_user = ToAPI.from_pss_user(pss_user)
    pss_user_after = FromAPI.to_pss_user(api_user)

    _assert_pss_user(pss_user_after)
    _assert_pss_users_equal(pss_user, pss_user_after)


# Helpers


def _assert_pss_alliance(pss_alliance: PssAlliance):
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


def _assert_pss_alliances_equal(pss_alliance_1: PssAlliance, pss_alliance_2: PssAlliance):
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


def _assert_collection(collection: Collection):
    assert collection
    assert isinstance(collection, Collection)

    _assert_collection_metadata(collection.metadata)

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


def _assert_collection_metadata(metadata: CollectionMetadata):
    assert metadata.timestamp is not None
    assert metadata.duration is not None
    assert metadata.fleet_count is not None
    assert metadata.user_count is not None
    assert metadata.tournament_running is not None
    assert metadata.schema_version is not None
    assert metadata.data_version is not None

    if metadata.data_version == 9:
        assert metadata.max_tournament_battle_attempts is not None


def _assert_pss_user(pss_user: PssUser):
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
