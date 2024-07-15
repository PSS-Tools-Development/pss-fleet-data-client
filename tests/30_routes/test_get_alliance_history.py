from typing import Any, Callable

import pytest
import test_cases
import vcr
from pytest import FixtureRequest

from client import PssFleetDataClient
from client.model import AllianceHistory
from client.model.exceptions import AllianceNotFoundError, ApiError, InvalidAllianceIdError


@pytest.mark.usefixtures("alliance_history", "mock_response_allianceHistory_allianceId_get_200")
@pytest.mark.usefixtures("assert_alliance_history_valid", "assert_alliance_histories_equal")
async def test_get_alliance_history_200(
    alliance_history: AllianceHistory,
    test_client: PssFleetDataClient,
    assert_alliance_history_valid: Callable[[AllianceHistory], None],
    assert_alliance_histories_equal: Callable[[AllianceHistory, AllianceHistory], None],
):
    response = await test_client.get_alliance_history(1)
    assert response
    assert isinstance(response, list)

    assert_alliance_history_valid(response[0])
    assert_alliance_histories_equal(alliance_history, response[0])


@pytest.mark.usefixtures("mock_response_allianceHistory_allianceId_404")
async def test_get_alliance_history_404(test_client: PssFleetDataClient):
    with pytest.raises(AllianceNotFoundError):
        _ = await test_client.get_alliance_history(1)


@pytest.mark.usefixtures("mock_response_allianceHistory_allianceId_422")
async def test_get_alliance_history_invalid_allianceId_422(test_client: PssFleetDataClient):
    with pytest.raises(InvalidAllianceIdError):
        _ = await test_client.get_alliance_history("f")


@pytest.mark.vcr()
@pytest.mark.usefixtures("vcr_config_match_on")
@pytest.mark.parametrize(["parameters", "expected_exception"], test_cases.invalid_filter_parameters)
async def test_get_alliance_history_422(
    parameters: dict[str, Any],
    expected_exception: ApiError,
    vcr_config_match_on: list[str],
    test_client: PssFleetDataClient,
    request: FixtureRequest,
):
    cassette_path = f"tests/30_routes/cassettes/test_get_422_{request.node.callspec.id}.yaml"

    with vcr.use_cassette(cassette_path, match_on=vcr_config_match_on):
        with pytest.raises(expected_exception):
            _ = await test_client.get_alliance_history(1, **parameters)
