import pytest
from pssapi.entities import Alliance as PssAlliance
from pssapi.entities import User as PssUser

from client import PssFleetDataClient
from client.model import Collection, CollectionMetadata


@pytest.mark.usefixtures("collection", "mock_response_get_collection_200")
async def test_get_collection_200(collection: Collection, test_client: PssFleetDataClient):
    response = await test_client.get_collection(1)
    _assert_collection(response)
    _assert_collections_equal(collection, response)


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


def _assert_collections_equal(collection_1: Collection, collection_2: Collection):
    assert collection_1
    assert collection_2
    assert isinstance(collection_1, Collection)
    assert isinstance(collection_2, Collection)

    _assert_collection_metadatas_equal(collection_1.metadata, collection_2.metadata)

    for i, pss_alliance in enumerate(collection_1.alliances):
        _assert_pss_alliances_equal(pss_alliance, collection_2.alliances[i])

    for i, pss_user in enumerate(collection_1.users):
        _assert_pss_users_equal(pss_user, collection_2.users[i])


def _assert_collection_metadatas_equal(collection_metadata_1: CollectionMetadata, collection_metadata_2: CollectionMetadata):
    assert collection_metadata_1
    assert collection_metadata_2
    assert isinstance(collection_metadata_1, CollectionMetadata)
    assert isinstance(collection_metadata_2, CollectionMetadata)

    assert id(collection_metadata_1) != id(collection_metadata_2)
    assert collection_metadata_1.model_dump() == collection_metadata_2.model_dump()


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
