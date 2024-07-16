from typing import Generator

import pytest
import vcr
import vcr.request
from responses import *  # noqa: F401,F403

from client import PssFleetDataClient


_DEFAULT_API_KEY = "123456"


@pytest.fixture(scope="function", autouse=True)
def default_api_key() -> str:
    return _DEFAULT_API_KEY


@pytest.fixture(scope="function", autouse=True)
def test_client(base_url: str, default_api_key: str) -> Generator[PssFleetDataClient, None, None]:
    client = PssFleetDataClient(
        base_url=base_url,
        api_key=default_api_key,
    )
    yield client


@pytest.fixture(scope="session")
def base_url() -> str:
    return "https://fleetdata.dolores2.xyz"
    # return "http://127.0.0.1:8000"


@pytest.fixture(scope="function")
def upload_test_file_path() -> str:
    return "tests/files/upload_test_data_schema_9.json"


@pytest.fixture(scope="module")
def vcr_config(vcr_config_match_on: list[str]):
    return {
        "match_on": vcr_config_match_on,
        "record_mode": "once",
        # "record_mode": "rewrite",  # Use this record mode to create new cassettes while testing, when an endpoint has their parameters or responses updated.
        "filter_query_parameters": [],
        "filter_post_data_parameters": [],
        "record_on_exception": False,
        "before_record_request": _before_record_request,
        "before_record_response": _before_record_response,
        "decode_compressed_response": True,
    }


@pytest.fixture(scope="session")
def vcr_config_match_on() -> list[str]:
    return ["method", "query"]


def _before_record_request(request: vcr.request.Request):
    request.headers["Authorization"] = ""
    return request


def _before_record_response(response):
    return response
