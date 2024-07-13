import pytest
from pssapi.entities import Alliance as PssAlliance
from pssapi.entities import User as PssUser

from client.model import Collection, CollectionMetadata
from client.model.api import ApiAlliance, ApiCollection, ApiCollectionMetadata, ApiUser
from client.model.converters import FromAPI


@pytest.mark.usefixtures("api_alliance")
def test_to_pss_alliance(api_alliance: ApiAlliance):
    pss_alliance = FromAPI.to_pss_alliance(api_alliance)
    _check_pss_alliance(pss_alliance)


@pytest.mark.usefixtures("api_collection")
def test_to_collection(api_collection: ApiCollection):
    collection = FromAPI.to_collection(api_collection)
    _check_collection(collection)


@pytest.mark.usefixtures("api_collection_metadata_3")
def test_to_collection_metadata_3(api_collection_metadata_3: ApiCollectionMetadata):
    collection_metadata = FromAPI.to_collection_metadata(api_collection_metadata_3)
    _check_collection_metadata(collection_metadata)


@pytest.mark.usefixtures("api_collection_metadata_9")
def test_to_collection_metadata_9(api_collection_metadata_9: ApiCollectionMetadata):
    collection_metadata = FromAPI.to_collection_metadata(api_collection_metadata_9)
    _check_collection_metadata(collection_metadata)


@pytest.mark.usefixtures("api_user")
def test_to_pss_user(api_user: ApiUser):
    pss_user = FromAPI.to_pss_user(api_user)
    _check_pss_user(pss_user)


# Helpers


def _check_pss_alliance(pss_alliance: PssAlliance):
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


def _check_collection(collection: Collection):
    assert collection
    assert isinstance(collection, Collection)

    _check_collection_metadata(collection.metadata)

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


def _check_collection_metadata(metadata: CollectionMetadata):
    assert metadata.timestamp is not None
    assert metadata.duration is not None
    assert metadata.fleet_count is not None
    assert metadata.user_count is not None
    assert metadata.tournament_running is not None
    assert metadata.schema_version is not None
    assert metadata.data_version is not None

    if metadata.data_version == 9:
        assert metadata.max_tournament_battle_attempts is not None


def _check_pss_user(pss_user: PssUser):
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
