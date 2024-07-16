import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

from httpx import AsyncClient, Response
from pssapi.entities import Alliance as PssAlliance
from pssapi.entities import User as PssUser

from .core.config import CONFIG
from .core.enums import ParameterInterval
from .models.api_models import ApiCollectionMetadata, ApiErrorResponse
from .models.client_models import AllianceHistory, Collection, CollectionMetadata, UserHistory
from .models.converters import FromAPI, FromResponse, ToAPI


@dataclass(frozen=True)
class ClientConfig:
    api_key: str
    base_url: str


class PssFleetDataClient:
    def __init__(self, base_url: str = None, api_key: str = None):
        self.__config = ClientConfig(
            api_key=api_key,
            base_url=base_url or CONFIG.default_base_url,
        )
        self.__client = AsyncClient(base_url=base_url)

    @property
    def api_key(self) -> Optional[str]:
        return self.__config.api_key

    @property
    def base_url(self) -> str:
        return self.__config.base_url

    def edit_config(self, base_url: str = None, api_key: str = None):
        self.__config = ClientConfig(
            api_key=api_key or self.__config.api_key,
            base_url=base_url or self.__config.base_url,
        )

    async def get_home_page(self) -> str:
        response = await self._get("/")
        return response.text

    async def create_collection(self, collection: Collection, api_key: str = None) -> CollectionMetadata:
        api_collection = ToAPI.from_collection(collection)
        request_json = json.loads(api_collection.model_dump_json())
        response = await self._post_with_api_key(
            "/collections",
            api_key=api_key,
            json=request_json,
        )

        api_collection_metadata = ApiCollectionMetadata(**response.json())
        result = FromAPI.to_collection_metadata(api_collection_metadata)
        return result

    async def delete_collection(self, collection_id: int, api_key: str = None) -> bool:
        _ = await self._delete_with_api_key(
            f"/collections/{collection_id}",
            api_key=api_key,
        )
        return True

    async def get_alliance_history(
        self,
        alliance_id: int,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        interval: Optional[ParameterInterval] = None,
        desc: Optional[bool] = None,
        skip: Optional[int] = None,
        take: Optional[int] = None,
    ) -> list[AllianceHistory]:
        response = await self._get_with_filter_parameters(
            f"/allianceHistory/{alliance_id}", from_date=from_date, to_date=to_date, interval=interval, desc=desc, skip=skip, take=take
        )
        alliance_histories = FromResponse.to_alliance_history_list(response)
        return alliance_histories

    async def get_alliance_from_collection(self, collection_id: int, alliance_id: int) -> tuple[CollectionMetadata, PssAlliance]:
        response = await self._get(f"/collections/{collection_id}/alliances/{alliance_id}")
        alliance_history = FromResponse.to_alliance_history(response)
        return (alliance_history.collection, alliance_history.alliance)

    async def get_alliances_from_collection(self, collection_id: int) -> tuple[Optional[CollectionMetadata], list[PssAlliance]]:
        response = await self._get(f"/collections/{collection_id}/alliances")
        collection = FromResponse.to_collection(response)

        if not collection:
            return None, []

        return (collection.metadata, collection.alliances)

    async def get_collection(self, collection_id: int) -> Collection:
        response = await self._get(f"/collections/{collection_id}")
        collection = FromResponse.to_collection(response)
        return collection

    async def get_collections(
        self,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        interval: Optional[ParameterInterval] = None,
        desc: Optional[bool] = None,
        skip: Optional[int] = None,
        take: Optional[int] = None,
    ) -> list[Collection]:
        response = await self._get_with_filter_parameters(
            "/collections/", from_date=from_date, to_date=to_date, interval=interval, desc=desc, skip=skip, take=take
        )
        collections = FromResponse.to_collection_metadata_list(response)
        return collections

    async def get_top_100_users_from_collection(self, collection_id: int) -> tuple[Collection, list[PssUser]]:
        response = await self._get(f"/collections/{collection_id}/top100Users")
        collection = FromResponse.to_collection(response)

        if not collection:
            return None, []

        return (collection.metadata, collection.users)

    async def get_user_from_collection(self, collection_id: int, user_id: int) -> UserHistory:
        response = await self._get(f"/collections/{collection_id}/users/{user_id}")
        user_history = FromResponse.to_user_history(response)
        return user_history

    async def get_users_from_collection(self, collection_id: int) -> tuple[Collection, list[PssUser]]:
        response = await self._get(f"/collections/{collection_id}/users")
        collection = FromResponse.to_collection(response)

        if not collection:
            return None, []

        return (collection.metadata, collection.users)

    async def get_user_history(
        self,
        user_id: int,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        interval: Optional[ParameterInterval] = None,
        desc: Optional[bool] = None,
        skip: Optional[int] = None,
        take: Optional[int] = None,
    ) -> list[UserHistory]:
        response = await self._get_with_filter_parameters(
            f"/userHistory/{user_id}", from_date=from_date, to_date=to_date, interval=interval, desc=desc, skip=skip, take=take
        )
        user_histories = FromResponse.to_user_history_list(response)
        return user_histories

    async def upload_collection(self, file_path: str, api_key: str = None) -> CollectionMetadata:
        if not isinstance(file_path, str):
            raise TypeError("Parameter `file` must be of type `str`.")

        with open(file_path, "rb") as fp:
            files = {"collection_file": ("collection", fp, "application/json")}
            response = await self._post_with_api_key(
                "/collections/upload",
                api_key=api_key,
                files=files,
            )

        api_collection_metadata = ApiCollectionMetadata(**response.json())
        result = FromAPI.to_collection_metadata(api_collection_metadata)
        return result

    async def _delete(self, path: str, params: Optional[dict[str, Any]] = None, headers: Optional[dict[str, Any]] = None) -> Response:
        request_headers = _create_request_headers(self.__client, headers)
        response = await self.__client.delete(path, params=params, headers=request_headers)
        _raise_if_error(response)

        return response

    async def _delete_with_api_key(
        self, path: str, api_key: Optional[str] = None, params: Optional[dict[str, Any]] = None, headers: Optional[dict[str, Any]] = None
    ) -> Response:
        headers = {"Authorization": api_key or self.api_key}
        response = await self._delete(
            path,
            params=params,
            headers=headers,
        )
        return response

    async def _get(self, path: str, params: Optional[dict[str, Any]] = None, headers: Optional[dict[str, Any]] = None) -> Response:
        request_headers = _create_request_headers(self.__client, headers)
        response = await self.__client.get(path, params=params, headers=request_headers)
        _raise_if_error(response)
        return response

    async def _get_with_filter_parameters(
        self,
        path: str,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        interval: Optional[ParameterInterval] = None,
        desc: Optional[bool] = None,
        skip: Optional[int] = None,
        take: Optional[int] = None,
    ) -> Response:
        parameters = _get_parameter_dict(from_date=from_date, to_date=to_date, interval=interval, desc=desc, skip=skip, take=take)
        response = await self._get(path, params=parameters)
        return response

    async def _post(
        self,
        path: str,
        json: Optional[dict[str, Any]] = None,
        files: Optional[dict[str, tuple]] = None,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, Any]] = None,
    ) -> Response:
        request_headers = _create_request_headers(self.__client, headers)

        response = await self.__client.post(path, json=json, files=files, params=params, headers=request_headers)
        _raise_if_error(response)
        return response

    async def _post_with_api_key(
        self,
        path: str,
        api_key: Optional[str] = None,
        json: Optional[dict[str, Any]] = None,
        files: Optional[dict[str, tuple]] = None,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, Any]] = None,
    ) -> Response:
        headers = {"Authorization": api_key or self.api_key}
        response = await self._post(path, json=json, files=files, params=params, headers=headers)
        return response


def _get_parameter_dict(
    *,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    interval: Optional[ParameterInterval] = None,
    desc: Optional[bool] = None,
    skip: Optional[int] = None,
    take: Optional[int] = None,
) -> dict[str, Any]:
    parameters = {}
    if from_date is not None:
        parameters["fromDate"] = from_date
    if to_date is not None:
        parameters["toDate"] = to_date
    if interval is not None:
        parameters["interval"] = interval
    if desc is not None:
        parameters["desc"] = desc
    if skip is not None:
        parameters["skip"] = skip
    if take is not None:
        parameters["take"] = take
    return parameters


def _raise_if_error(response: Response):
    if response.status_code not in (401, 403, 404, 405, 409, 415, 422, 429, 500):
        return

    api_error = ApiErrorResponse(**response.json())
    exception = FromAPI.to_error(api_error)

    raise exception


def _create_request_headers(client: AsyncClient, headers: dict[str, str]) -> dict[str, str]:
    """Takes the default headers configured in the `client` and updates them with the additionally specified `headers`.

    Args:
        client (AsyncClient): The client to take the default headers from.
        headers (dict[str, Any]): The additional headers to add or to overwrite default headers with.

    Returns:
        dict[str, str]: A collection of headers to be sent with a request.
    """
    if not client.headers:
        return headers

    request_headers = dict(client.headers)

    if headers:
        request_headers.update(headers)

    return request_headers


__all__ = [
    ClientConfig.__name__,
    PssFleetDataClient.__name__,
]
