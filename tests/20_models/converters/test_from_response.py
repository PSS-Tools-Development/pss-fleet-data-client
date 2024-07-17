from typing import Callable

from httpx import Response

from pss_fleet_data.models import AllianceHistory, Collection, UserHistory
from pss_fleet_data.models.converters import FromResponse


async def test_to_alliance_history(
    response_alliance_history: Response,
    alliance_history: AllianceHistory,
    assert_alliance_history_valid: Callable[[AllianceHistory], None],
    assert_alliance_histories_equal: Callable[[AllianceHistory, AllianceHistory], None],
):
    alliance_history_response = FromResponse.to_alliance_history(response_alliance_history)

    assert_alliance_history_valid(alliance_history_response)
    assert_alliance_histories_equal(alliance_history, alliance_history_response)


async def test_to_alliance_history_with_members(
    response_alliance_history_with_members: Response,
    alliance_history_with_members: AllianceHistory,
    assert_alliance_history_with_members_valid: Callable[[AllianceHistory], None],
    assert_alliance_histories_equal: Callable[[AllianceHistory, AllianceHistory], None],
):
    alliance_history_response = FromResponse.to_alliance_history(response_alliance_history_with_members)

    assert_alliance_history_with_members_valid(alliance_history_response)
    assert_alliance_histories_equal(alliance_history_with_members, alliance_history_response)


async def test_to_alliance_history_list(
    response_alliance_history_list: Response,
    alliance_history: AllianceHistory,
    assert_alliance_history_valid: Callable[[AllianceHistory], None],
    assert_alliance_histories_equal: Callable[[AllianceHistory, AllianceHistory], None],
):
    alliance_history_list_response = FromResponse.to_alliance_history_list(response_alliance_history_list)

    assert alliance_history_list_response
    assert isinstance(alliance_history_list_response, list)

    assert_alliance_history_valid(alliance_history_list_response[0])
    assert_alliance_histories_equal(alliance_history, alliance_history_list_response[0])


async def test_to_alliance_history_list_with_members(
    response_alliance_history_list_with_members: Response,
    alliance_history_with_members: AllianceHistory,
    assert_alliance_history_with_members_valid: Callable[[AllianceHistory], None],
    assert_alliance_histories_equal: Callable[[AllianceHistory, AllianceHistory], None],
):
    alliance_history_list_response = FromResponse.to_alliance_history_list(response_alliance_history_list_with_members)

    assert alliance_history_list_response
    assert isinstance(alliance_history_list_response, list)

    assert_alliance_history_with_members_valid(alliance_history_list_response[0])
    assert_alliance_histories_equal(alliance_history_with_members, alliance_history_list_response[0])


async def test_to_collection(
    response_collection: Response,
    collection: Collection,
    assert_collection_valid: Callable[[Collection], None],
    assert_collections_equal: Callable[[Collection, Collection], None],
):
    collection_response = FromResponse.to_collection(response_collection)

    assert_collection_valid(collection_response, True, True)
    assert_collections_equal(collection, collection_response, True, True)


async def test_to_collection_metadata_200(
    response_collection_metadata_200: Response,
    collection_metadata_9: Collection,
    assert_collection_metadata_valid: Callable[[Collection], None],
    assert_collection_metadatas_equal: Callable[[Collection, Collection], None],
):
    collection_metadata_response = FromResponse.to_collection_metadata(response_collection_metadata_200)

    assert_collection_metadata_valid(collection_metadata_response)
    assert_collection_metadatas_equal(collection_metadata_9, collection_metadata_response)


async def test_to_collection_metadata_201(
    response_collection_metadata_201: Response,
    collection_metadata_9: Collection,
    assert_collection_metadata_valid: Callable[[Collection], None],
    assert_collection_metadatas_equal: Callable[[Collection, Collection], None],
):
    collection_metadata_response = FromResponse.to_collection_metadata(response_collection_metadata_201)

    assert_collection_metadata_valid(collection_metadata_response)
    assert_collection_metadatas_equal(collection_metadata_9, collection_metadata_response)


async def test_to_collection_metadata_list(
    response_collection_metadata_list: Response,
    collection_metadata_9: Collection,
    assert_collection_metadata_valid: Callable[[Collection], None],
    assert_collection_metadatas_equal: Callable[[Collection, Collection], None],
):
    collection_metadata_list_response = FromResponse.to_collection_metadata_list(response_collection_metadata_list)

    assert collection_metadata_list_response
    assert isinstance(collection_metadata_list_response, list)

    assert_collection_metadata_valid(collection_metadata_list_response[0])
    assert_collection_metadatas_equal(collection_metadata_9, collection_metadata_list_response[0])


async def test_to_user_history(
    response_user_history: Response,
    user_history: UserHistory,
    assert_user_history_valid: Callable[[UserHistory], None],
    assert_user_histories_equal: Callable[[UserHistory, UserHistory], None],
):
    user_history_response = FromResponse.to_user_history(response_user_history)

    assert_user_history_valid(user_history_response)
    assert_user_histories_equal(user_history, user_history_response)


async def test_to_user_history_with_fleet(
    response_user_history_with_fleet: Response,
    user_history_with_alliance: UserHistory,
    assert_user_history_with_alliance_valid: Callable[[UserHistory], None],
    assert_user_histories_equal: Callable[[UserHistory, UserHistory], None],
):
    user_history_response = FromResponse.to_user_history(response_user_history_with_fleet)

    assert_user_history_with_alliance_valid(user_history_response)
    assert_user_histories_equal(user_history_with_alliance, user_history_response)


async def test_to_user_history_list(
    response_user_history_list: Response,
    user_history: UserHistory,
    assert_user_history_valid: Callable[[UserHistory], None],
    assert_user_histories_equal: Callable[[UserHistory, UserHistory], None],
):
    user_history_list_response = FromResponse.to_user_history_list(response_user_history_list)

    assert user_history_list_response
    assert isinstance(user_history_list_response, list)

    assert_user_history_valid(user_history_list_response[0])
    assert_user_histories_equal(user_history, user_history_list_response[0])


async def test_to_user_history_list_with_fleet(
    response_user_history_list_with_fleet: Response,
    user_history_with_alliance: UserHistory,
    assert_user_history_with_alliance_valid: Callable[[UserHistory], None],
    assert_user_histories_equal: Callable[[UserHistory, UserHistory], None],
):
    user_history_list_response = FromResponse.to_user_history_list(response_user_history_list_with_fleet)

    assert user_history_list_response
    assert isinstance(user_history_list_response, list)

    assert_user_history_with_alliance_valid(user_history_list_response[0])
    assert_user_histories_equal(user_history_with_alliance, user_history_list_response[0])
