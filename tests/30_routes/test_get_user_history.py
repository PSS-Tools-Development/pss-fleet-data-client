from typing import Any, Callable

import pytest
import test_cases
import vcr
from pytest import FixtureRequest

from client import PssFleetDataClient
from client.core.exceptions import ApiError, InvalidUserIdError, UserNotFoundError
from client.models import UserHistory


@pytest.mark.usefixtures("mock_response_userHistory_userId_get_200")
async def test_get_user_history_200(
    user_history: UserHistory,
    test_client: PssFleetDataClient,
    assert_user_history_valid: Callable[[UserHistory], None],
    assert_user_histories_equal: Callable[[UserHistory, UserHistory], None],
):
    response = await test_client.get_user_history(1)
    assert response
    assert isinstance(response, list)

    assert_user_history_valid(response[0])
    assert_user_histories_equal(user_history, response[0])


@pytest.mark.usefixtures("mock_response_userHistory_userId_get_200_with_members")
async def test_get_user_history_200_with_members(
    user_history_with_alliance: UserHistory,
    test_client: PssFleetDataClient,
    assert_user_history_with_alliance_valid: Callable[[UserHistory], None],
    assert_user_histories_equal: Callable[[UserHistory, UserHistory], None],
):
    response = await test_client.get_user_history(1)
    assert response
    assert isinstance(response, list)

    assert_user_history_with_alliance_valid(response[0])
    assert_user_histories_equal(user_history_with_alliance, response[0])


@pytest.mark.usefixtures("mock_response_empty_collection_get_204")
async def test_get_user_history_204(test_client: PssFleetDataClient):
    response = await test_client.get_user_history(1)
    assert isinstance(response, list)
    assert len(response) == 0


@pytest.mark.usefixtures("mock_response_user_not_found")
async def test_get_user_history_404(test_client: PssFleetDataClient):
    with pytest.raises(UserNotFoundError):
        _ = await test_client.get_user_history(1)


@pytest.mark.usefixtures("mock_response_user_id_invalid")
async def test_get_user_history_invalid_userId_422(test_client: PssFleetDataClient):
    with pytest.raises(InvalidUserIdError):
        _ = await test_client.get_user_history("f")


@pytest.mark.vcr()
@pytest.mark.usefixtures("vcr_config_match_on")
@pytest.mark.parametrize(["parameters", "expected_exception"], test_cases.invalid_filter_parameters)
async def test_get_user_history_422(
    parameters: dict[str, Any],
    expected_exception: ApiError,
    vcr_config_match_on: list[str],
    test_client: PssFleetDataClient,
    request: FixtureRequest,
):
    cassette_path = f"tests/30_routes/cassettes/test_get_422_{request.node.callspec.id}.yaml"

    with vcr.use_cassette(cassette_path, match_on=vcr_config_match_on):
        with pytest.raises(expected_exception):
            _ = await test_client.get_user_history(1, **parameters)
