import json
from datetime import datetime
from typing import Any, Optional

from httpx import AsyncClient, Response
from pssapi.entities import Alliance as PssAlliance
from pssapi.entities import User as PssUser

from .core import utils
from .core.enums import ParameterInterval
from .models.api_models import ApiErrorResponse
from .models.client_models import AllianceHistory, Collection, CollectionMetadata, UserHistory
from .models.converters import FromAPI, FromResponse, ToAPI


class PssFleetDataClient:
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None, proxy: Optional[str] = None):
        self.__api_key: Optional[str] = api_key
        self.__proxy: Optional[str] = proxy
        self.__http_client = AsyncClient(base_url=base_url, proxy=proxy)

    @property
    def api_key(self) -> Optional[str]:
        return self.__api_key

    @property
    def base_url(self) -> str:
        return self.__http_client.base_url

    @property
    def proxy(self) -> str:
        return self.__proxy

    def change_base_url(self, base_url: str):
        self.__http_client = AsyncClient(base_url=base_url, proxy=self.proxy)

    def change_proxy(self, proxy: str):
        self.__proxy = proxy
        self.__http_client = AsyncClient(base_url=self.base_url, proxy=proxy)

    # Operations

    async def get_home_page(self) -> str:
        response = await self._get("/")
        return response.text

    async def create_collection(self, collection: Collection, api_key: str = None) -> CollectionMetadata:
        api_collection = ToAPI.from_collection(collection)
        request_json = json.loads(api_collection.model_dump_json())
        api_key = api_key or self.api_key

        response = await self._post_with_api_key(
            "/collections",
            api_key=api_key,
            json=request_json,
        )

        result = FromResponse.to_collection_metadata(response)
        return result

    async def delete_collection(self, collection_id: int, api_key: str = None) -> bool:
        api_key = api_key or self.api_key

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
            f"/allianceHistory/{alliance_id}",
            from_date=from_date,
            to_date=to_date,
            interval=interval,
            desc=desc,
            skip=skip,
            take=take,
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

    async def get_most_recent_collection_by_timestamp(self, timestamp: datetime) -> Optional[Collection]:
        for interval in (ParameterInterval.HOURLY, ParameterInterval.DAILY, ParameterInterval.MONTHLY):
            from_date, to_date = utils.get_from_to_date_from_timestamp(timestamp, interval)
            collection_metadatas = await self.get_collections(
                from_date=from_date,
                to_date=to_date,
                interval=ParameterInterval.HOURLY,
                desc=True,
                take=1,
            )
            if collection_metadatas:
                collection = await self.get_collection(collection_metadatas[0].collection_id)
                return collection
        return None

    async def get_collections(
        self,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        interval: Optional[ParameterInterval] = None,
        desc: Optional[bool] = None,
        skip: Optional[int] = None,
        take: Optional[int] = None,
    ) -> list[CollectionMetadata]:
        response = await self._get_with_filter_parameters(
            "/collections/",
            from_date=from_date,
            to_date=to_date,
            interval=interval,
            desc=desc,
            skip=skip,
            take=take,
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
            f"/userHistory/{user_id}",
            from_date=from_date,
            to_date=to_date,
            interval=interval,
            desc=desc,
            skip=skip,
            take=take,
        )
        user_histories = FromResponse.to_user_history_list(response)
        return user_histories

    async def upload_collection(self, file_path: str, api_key: str = None) -> CollectionMetadata:
        if not isinstance(file_path, str):
            raise TypeError("Parameter `file` must be of type `str`.")

        api_key = api_key or self.api_key

        with open(file_path, "rb") as fp:
            files = {"collection_file": ("collection", fp, "application/json")}
            response = await self._post_with_api_key(
                "/collections/upload",
                api_key=api_key,
                files=files,
            )

        result = FromResponse.to_collection_metadata(response)
        return result

    async def _delete(self, path: str, params: Optional[dict[str, Any]] = None, headers: Optional[dict[str, Any]] = None) -> Response:
        request_headers = _create_request_headers(self.__http_client, headers)
        response = await self.__http_client.delete(path, params=params, headers=request_headers)
        _raise_on_error(response)

        return response

    async def _delete_with_api_key(
        self,
        path: str,
        api_key: Optional[str],
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, Any]] = None,
    ) -> Response:
        headers = headers or {}
        headers["Authorization"] = api_key or self.__api_key

        response = await self._delete(
            path,
            params=params,
            headers=headers,
        )
        return response

    async def _get(self, path: str, params: Optional[dict[str, Any]] = None, headers: Optional[dict[str, Any]] = None) -> Response:
        request_headers = _create_request_headers(self.__http_client, headers)
        response = await self.__http_client.get(path, params=params, headers=request_headers)
        _raise_on_error(response)
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
        parameters = utils.create_parameter_dict(from_date=from_date, to_date=to_date, interval=interval, desc=desc, skip=skip, take=take)
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
        request_headers = _create_request_headers(self.__http_client, headers)

        response = await self.__http_client.post(path, json=json, files=files, params=params, headers=request_headers)
        _raise_on_error(response)
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
        headers = headers or {}
        headers["Authorization"] = api_key or self.__api_key

        response = await self._post(path, json=json, files=files, params=params, headers=headers)
        return response


# Helper


def _raise_on_error(response: Response):
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
    PssFleetDataClient.__name__,
]
