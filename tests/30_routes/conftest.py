import pytest
import vcr
import vcr.request
from responses import *  # noqa: F401,F403

from client import PssFleetDataClient


@pytest.fixture(scope="function", autouse=True)
def test_client(base_url):
    client = PssFleetDataClient(
        base_url=base_url,
        api_key="123456",
    )
    yield client


@pytest.fixture(scope="session")
def base_url() -> str:
    return "https://fleetdata.dolores2.xyz"
    # return "http://127.0.0.1:8000"


@pytest.fixture(scope="session")
def vcr_config_match_on() -> list[str]:
    return ["method", "query"]


@pytest.fixture(scope="module")
def vcr_config(vcr_config_match_on: list[str]):
    return {
        "match_on": vcr_config_match_on,
        "record_mode": "once",
        # "record_mode": "rewrite",  # Use this record mode to create new cassettes while testing, when an endpoint has their parameters or responses updated.
        "filter_query_parameters": [],
        "filter_post_data_parameters": [],
        "record_on_exception": False,
        "before_record_request": before_record_request,
        "before_record_response": before_record_response,
        "decode_compressed_response": True,
    }


def before_record_request(request: vcr.request.Request):
    request.headers["Authorization"] = ""
    return request


def before_record_response(response):
    return response
