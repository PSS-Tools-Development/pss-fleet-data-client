import json

import pytest
from httpx import Response

from client.models.api_models import ApiAllianceHistory, ApiCollection, ApiUserHistory


@pytest.fixture(scope="function")
def response_alliance_history(api_alliance_history: ApiAllianceHistory) -> Response:
    return Response(200, json=json.loads(api_alliance_history.model_dump_json()))


@pytest.fixture(scope="function")
def response_alliance_history_with_members(api_alliance_history_with_members: ApiAllianceHistory) -> Response:
    return Response(200, json=json.loads(api_alliance_history_with_members.model_dump_json()))


@pytest.fixture(scope="function")
def response_alliance_history_list(api_alliance_history: ApiAllianceHistory) -> Response:
    return Response(200, json=[json.loads(api_alliance_history.model_dump_json())])


@pytest.fixture(scope="function")
def response_alliance_history_list_with_members(api_alliance_history_with_members: ApiAllianceHistory) -> Response:
    return Response(200, json=[json.loads(api_alliance_history_with_members.model_dump_json())])


@pytest.fixture(scope="function")
def response_collection(api_collection: ApiCollection) -> Response:
    return Response(200, json=json.loads(api_collection.model_dump_json()))


@pytest.fixture(scope="function")
def response_collection_metadata_200(api_collection_metadata_9: ApiCollection) -> Response:
    return Response(200, json=json.loads(api_collection_metadata_9.model_dump_json()))


@pytest.fixture(scope="function")
def response_collection_metadata_201(api_collection_metadata_9: ApiCollection) -> Response:
    return Response(201, json=json.loads(api_collection_metadata_9.model_dump_json()))


@pytest.fixture(scope="function")
def response_collection_metadata_list(api_collection_metadata_9: ApiCollection) -> Response:
    return Response(200, json=[json.loads(api_collection_metadata_9.model_dump_json())])


@pytest.fixture(scope="function")
def response_user_history(api_user_history: ApiUserHistory) -> Response:
    return Response(200, json=json.loads(api_user_history.model_dump_json()))


@pytest.fixture(scope="function")
def response_user_history_with_fleet(api_user_history_with_fleet: ApiUserHistory) -> Response:
    return Response(200, json=json.loads(api_user_history_with_fleet.model_dump_json()))


@pytest.fixture(scope="function")
def response_user_history_list(api_user_history: ApiUserHistory) -> Response:
    return Response(200, json=[json.loads(api_user_history.model_dump_json())])


@pytest.fixture(scope="function")
def response_user_history_list_with_fleet(api_user_history_with_fleet: ApiUserHistory) -> Response:
    return Response(200, json=[json.loads(api_user_history_with_fleet.model_dump_json())])
