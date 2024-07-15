from fixtures import *  # noqa: F401,F403


@pytest.fixture(scope="function")
def get_allianceHistory_1_url(base_url) -> str:
    return f"{base_url}/allianceHistory/1"


@pytest.fixture(scope="function")
def get_collection_1_url(base_url) -> str:
    return f"{base_url}/collections/1"


@pytest.fixture(scope="function")
def get_collections_url(base_url: str) -> str:
    return f"{base_url}/collections/"
