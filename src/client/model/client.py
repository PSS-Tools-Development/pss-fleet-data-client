import json
from dataclasses import dataclass
from datetime import datetime
from io import TextIOWrapper
from typing import Any, Optional, Union

from httpx import AsyncClient, Response
from pssapi.entities import Alliance as PssAlliance
from pssapi.entities import User as PssUser

from ..config import CONFIG
from .api import ApiAllianceHistory, ApiCollection, ApiCollectionMetadata, ApiErrorResponse, ApiUserHistory
from .converters import FromAPI, ToAPI
from .enums import ErrorCode, ParameterInterval
from .exceptions import (
    AllianceNotFoundError,
    ApiError,
    CollectionNotDeletedError,
    CollectionNotFoundError,
    ConflictError,
    FromDateAfterToDateError,
    FromDateTooEarlyError,
    InvalidAllianceIdError,
    InvalidBoolError,
    InvalidCollectionIdError,
    InvalidDateTimeError,
    InvalidDescError,
    InvalidFromDateError,
    InvalidIntervalError,
    InvalidJsonUpload,
    InvalidNumberError,
    InvalidSkipError,
    InvalidTakeError,
    InvalidToDateError,
    InvalidUserIdError,
    MethodNotAllowedError,
    MissingAccessError,
    NonUniqueCollectionIdError,
    NonUniqueTimestampError,
    NotAuthenticatedError,
    NotFoundError,
    ParameterFormatError,
    ParameterValidationError,
    ParameterValueError,
    SchemaVersionMismatch,
    ServerError,
    ToDateTooEarlyError,
    TooManyRequestsError,
    UnsupportedMediaTypeError,
    UnsupportedSchemaError,
    UserNotFoundError,
)
from .models import Collection


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

    async def get_home_page(self) -> str:
        return self.__client.get("/").text

    def edit_config(self, base_url: str = None, api_key: str = None):
        self.__config = ClientConfig(
            api_key=api_key or self.__config.api_key,
            base_url=base_url or self.__config.base_url,
        )

    async def create_collection(self, collection: Collection, api_key: str = None) -> Collection:
        headers = {"Authorization": api_key or self.api_key}
        api_collection = ToAPI.from_collection(collection)
        response = await self._post(
            "/collections",
            json=json.loads(api_collection.model_dump_json()),
            headers=headers,
        )

        api_collection_metadata = ApiCollectionMetadata(**response.json())
        result = Collection(metadata=FromAPI.to_collection_metadata(api_collection_metadata))
        return result

    async def delete_collection(self, collection_id: int, api_key: str = None) -> bool:
        headers = {"Authorization": api_key or self.api_key}
        _ = await self._delete(
            f"/collections/{collection_id}",
            headers=headers,
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
    ) -> list[tuple[Collection, PssAlliance]]:
        parameters = get_parameter_dict(from_date=from_date, to_date=to_date, interval=interval, desc=desc, skip=skip, take=take)
        response = await self._get(
            f"/allianceHistory/{alliance_id}",
            params=parameters,
        )

        api_alliance_histories = [ApiAllianceHistory(**item) for item in response.json()]
        alliance_histories = [FromAPI.to_alliance_history(alliance_history) for alliance_history in api_alliance_histories]
        result = [(alliance_history.collection, alliance_history.alliance) for alliance_history in alliance_histories]
        return result

    async def get_alliance_from_collection(self, collection_id: int, alliance_id: int) -> tuple[Collection, PssAlliance]:
        response = await self._get(
            f"/collections/{collection_id}/alliances/{alliance_id}",
        )

        api_alliance_history = ApiAllianceHistory(**response.json())
        alliance_history = FromAPI.to_alliance_history(api_alliance_history)
        return (alliance_history.collection, alliance_history.alliance)

    async def get_alliances_from_collection(self, collection_id: int) -> tuple[Collection, list[PssAlliance]]:
        response = await self._get(
            f"/collections/{collection_id}/alliances",
        )

        api_collection = ApiCollection(**response.json())
        collection = FromAPI.to_collection(api_collection)
        return (collection.metadata, collection.users)

    async def get_collection(self, collection_id: int) -> Collection:
        response = await self._get(
            f"/collections/{collection_id}",
        )

        api_collection = ApiCollection(**response.json())
        collection = FromAPI.to_collection(api_collection)
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
        parameters = get_parameter_dict(from_date=from_date, to_date=to_date, interval=interval, desc=desc, skip=skip, take=take)
        response = await self._get(
            "/collections/",
            params=parameters,
        )

        api_collections = [ApiCollection(**item) for item in response.json()]
        result = [FromAPI.to_collection(collection) for collection in api_collections]
        return result

    async def get_top_100_users_from_collection(self, collection_id: int) -> tuple[Collection, list[PssUser]]:
        response = await self._get(
            f"/collections/{collection_id}/top100Users",
        )

        api_collection = ApiCollection(**response.json())
        collection = FromAPI.to_collection(api_collection)
        return (collection.collection, collection.users)

    async def get_user_from_collection(self, collection_id: int, user_id: int) -> tuple[Collection, PssUser]:
        response = await self._get(
            f"/collections/{collection_id}/users/{user_id}",
        )

        api_user_history = ApiUserHistory(**response.json())
        user_history = FromAPI.to_user_history(api_user_history)
        return (user_history.collection, user_history.user)

    async def get_users_from_collection(self, collection_id: int) -> tuple[Collection, list[PssUser]]:
        response = await self._get(
            f"/collections/{collection_id}/users",
        )

        api_collection = ApiCollection(**response.json())
        collection = FromAPI.to_collection(api_collection)
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
    ) -> list[tuple[Collection, PssUser]]:
        parameters = get_parameter_dict(from_date=from_date, to_date=to_date, interval=interval, desc=desc, skip=skip, take=take)
        response = await self._get(
            f"/userHistory/{user_id}",
            params=parameters,
        )

        api_user_histories = [ApiUserHistory(**item) for item in response.json()]
        user_histories = [FromAPI.to_user_history(user_history) for user_history in api_user_histories]
        result = [(user_history.collection, user_history.user) for user_history in user_histories]
        return result

    async def upload_collection(self, file: Union[str, TextIOWrapper] = None, api_key: str = None) -> Collection:
        headers = {"Authorization": api_key or self.api_key}
        if isinstance(file, str):
            with open(file, "rb") as fp:
                files = {"collection_file": ("collection", fp, "application/json")}
                response = await self._post(
                    "/collections/upload",
                    files=files,
                    headers=headers,
                )
        else:
            files = {"collection_file": ("collection", file, "application/json")}
            response = await self._post(
                "/collections/upload",
                files=files,
                headers=headers,
            )

        api_collection_metadata = ApiCollectionMetadata(**response.json())
        result = Collection(metadata=FromAPI.to_collection_metadata(api_collection_metadata))
        return result

    async def _delete(self, path: str, params: Optional[dict[str, Any]] = None, headers: Optional[dict[str, Any]] = None) -> Response:
        response = await self.__client.delete(path, params=params, headers=headers)
        raise_if_error(response)
        return response

    async def _get(self, path: str, params: Optional[dict[str, Any]] = None, headers: Optional[dict[str, Any]] = None) -> Response:
        response = await self.__client.get(path, params=params, headers=headers)
        raise_if_error(response)
        return response

    async def _post(
        self,
        path: str,
        json: Optional[dict[str, Any]] = None,
        files: Optional[dict[str, tuple]] = None,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, Any]] = None,
    ) -> Response:
        response = await self.__client.post(path, json=json, files=files, params=params, headers=headers)
        raise_if_error(response)
        return response


def get_parameter_dict(
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


def raise_if_error(response: Response):
    if response.status_code not in (401, 403, 404, 405, 409, 415, 422, 429, 500):
        return

    api_error = ApiErrorResponse(**response.json())
    args = (api_error.code, api_error.message, api_error.details, api_error.timestamp, api_error.suggestion, api_error.links)

    match api_error.code:
        case ErrorCode.ALLIANCE_NOT_FOUND:
            raise AllianceNotFoundError(*args)
        case ErrorCode.COLLECTION_NOT_DELETED:
            raise CollectionNotDeletedError(*args)
        case ErrorCode.COLLECTION_NOT_FOUND:
            raise CollectionNotFoundError(*args)
        case ErrorCode.CONFLICT:
            raise ConflictError(*args)
        case ErrorCode.FORBIDDEN:
            raise MissingAccessError(*args)
        case ErrorCode.FROM_DATE_AFTER_TO_DATE:
            raise FromDateAfterToDateError(*args)
        case ErrorCode.INVALID_BOOL:
            raise InvalidBoolError(*args)
        case ErrorCode.INVALID_DATETIME:
            raise InvalidDateTimeError(*args)
        case ErrorCode.INVALID_JSON_FORMAT:
            return InvalidJsonUpload
        case ErrorCode.INVALID_NUMBER:
            raise InvalidNumberError(*args)
        case ErrorCode.INVALID_PARAMETER:
            raise ParameterValidationError(*args)
        case ErrorCode.INVALID_PARAMETER_FORMAT:
            raise ParameterFormatError(*args)
        case ErrorCode.INVALID_PARAMETER_VALUE:
            raise ParameterValueError(*args)
        case ErrorCode.METHOD_NOT_ALLOWED:
            raise MethodNotAllowedError(*args)
        case ErrorCode.NON_UNIQUE_COLLECTION_ID:
            raise NonUniqueCollectionIdError(*args)
        case ErrorCode.NON_UNIQUE_TIMESTAMP:
            raise NonUniqueTimestampError(*args)
        case ErrorCode.NOT_AUTHENTICATED:
            raise NotAuthenticatedError(*args)
        case ErrorCode.NOT_FOUND:
            raise NotFoundError(*args)
        case ErrorCode.PARAMETER_ALLIANCE_ID_INVALID:
            raise InvalidAllianceIdError(*args)
        case ErrorCode.PARAMETER_COLLECTION_ID_INVALID:
            raise InvalidCollectionIdError(*args)
        case ErrorCode.PARAMETER_DESC_INVALID:
            raise InvalidDescError(*args)
        case ErrorCode.PARAMETER_FROM_DATE_INVALID:
            raise InvalidFromDateError(*args)
        case ErrorCode.PARAMETER_FROM_DATE_TOO_EARLY:
            raise FromDateTooEarlyError(*args)
        case ErrorCode.PARAMETER_INTERVAL_INVALID:
            raise InvalidIntervalError(*args)
        case ErrorCode.PARAMETER_SKIP_INVALID:
            raise InvalidSkipError(*args)
        case ErrorCode.PARAMETER_TAKE_INVALID:
            raise InvalidTakeError(*args)
        case ErrorCode.PARAMETER_TO_DATE_INVALID:
            raise InvalidToDateError(*args)
        case ErrorCode.PARAMETER_TO_DATE_TOO_EARLY:
            raise ToDateTooEarlyError(*args)
        case ErrorCode.PARAMETER_USER_ID_INVALID:
            raise InvalidUserIdError(*args)
        case ErrorCode.RATE_LIMITED:
            raise TooManyRequestsError(*args)
        case ErrorCode.SCHEMA_VERSION_MISMATCH:
            return SchemaVersionMismatch
        case ErrorCode.SERVER_ERROR:
            raise ServerError(*args)
        case ErrorCode.UNSUPPORTED_MEDIA_TYPE:
            raise UnsupportedMediaTypeError(*args)
        case ErrorCode.UNSUPPORTED_SCHEMA:
            raise UnsupportedSchemaError(*args)
        case ErrorCode.USER_NOT_FOUND:
            raise UserNotFoundError(*args)  #

    raise ApiError(*args)
