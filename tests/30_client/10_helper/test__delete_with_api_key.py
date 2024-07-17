import helper_test_cases
import pytest
from httpx import Response

from client import PssFleetDataClient


@pytest.mark.usefixtures("mock_response_empty_get_204")
@pytest.mark.parametrize(["api_key_sent", "api_key_expected"], helper_test_cases.api_keys)
async def test_delete_collection_with_api_key(
    api_key_sent: str,
    api_key_expected: str,
    test_client: PssFleetDataClient,
):
    response: Response = await test_client._delete_with_api_key("/collections/1", api_key=api_key_sent)
    authorization_header = response.request.headers.get("Authorization")
    assert authorization_header == api_key_expected
