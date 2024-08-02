import pytest

from pss_fleet_data import PssFleetDataClient


@pytest.mark.usefixtures("mock_response_ping_get_200")
async def test_ping(test_client: PssFleetDataClient):
    result = await test_client.ping()
    assert result == "Pong!"
