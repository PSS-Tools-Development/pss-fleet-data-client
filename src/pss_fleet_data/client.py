import json
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Union

from httpx import URL, AsyncClient, Response, Timeout
from pssapi.entities import Alliance as PssAlliance
from pssapi.entities import User as PssUser

from . import utils
from .core.config import get_config
from .models.api_models import ApiErrorResponse
from .models.client_models import AllianceHistory, Collection, CollectionMetadata, UserHistory
from .models.converters import FromAPI, FromResponse, ToAPI
from .models.enums import ParameterInterval


class PssFleetDataClient:
    """Represents a PSS Fleet Data API client."""

    def __init__(
        self,
        base_url: Optional[Union[str, URL]] = None,
        api_key: Optional[str] = None,
        proxy: Optional[Union[str, URL]] = None,
        request_timeout: Optional[float] = None,
        connect_timeout: Optional[float] = None,
    ):
        """Initializes a PSS Fleet Data API client.

        Args:
            base_url (str | httpx.URL, optional): The base URL of the API server to work with. Defaults to `https://fleetdata.dolores2.xyz`.
            api_key (str, optional): The API key to send with DELETE and POST requests. Defaults to `None`.
            proxy (str | httpx.URL, optional): The proxy server to send the requests through. Defaults to `None`.
            request_timeout (float | int, optional): The request timeout in seconds after which any request gets cancelled. Defaults to `None` (no request timeout).
            connect_timeout (float | int, optional): The connection timeout in seconds after which a connection attempt gets cancelled. Increase, if the connection is bad. Defaults to `5.0`.
        """
        base_url = utils.ensure.str_or_url(base_url, "base_url", default=get_config().default_base_url)
        self.__api_key = utils.ensure.str_(api_key, "api_key")
        self.__proxy = utils.ensure.str_or_url(proxy, "proxy")
        self.__connect_timeout = utils.ensure.positive_float_or_int(connect_timeout, "connect_timeout", default=5.0)
        self.__request_timeout = utils.ensure.positive_float_or_int(request_timeout, "request_timeout")

        timeout_config = Timeout(self.request_timeout, connect=self.connect_timeout)
        self.__http_client = AsyncClient(base_url=base_url, proxy=self.proxy, timeout=timeout_config)

    @property
    def api_key(self) -> Optional[str]:
        """
        The API key set at client creation. Is required to access certain endpoints that use the DELETE or POST methods.
        The respective methods also accept an `api_key` to override the one passed at creation time.
        """
        return self.__api_key

    @property
    def base_url(self) -> str:
        """
        The base URL of the API server to work with.
        """
        return self.__http_client.base_url

    @property
    def connect_timeout(self) -> float:
        """
        The connection timeout in seconds after which a connection attempt gets cancelled. Increase, if the connection is bad.
        """
        return float(self.__connect_timeout)

    @property
    def proxy(self) -> Optional[str]:
        """
        The proxy URL passed to the client at creation. Any requests will be sent through this server.
        """
        return self.__proxy

    @property
    def request_timeout(self) -> Optional[float]:
        """
        The request timeout in seconds after which any request gets cancelled.
        """
        return float(self.__request_timeout) if self.__request_timeout is not None else None

    # Operations

    async def get_home_page(self) -> str:
        """Return the home page of the API.

        Returns:
            str: The HTML documnet representing the home page of the API.
        """
        response = await self._get("/")
        return response.text

    async def create_collection(self, collection: Collection, api_key: Optional[str] = None) -> CollectionMetadata:
        """Add a `Collection` of the latest schema version (version 9) to the API.

        Args:
            collection (Collection): The `Collection` of schema version 9 to be added.
            api_key (str, optional): The API key to send for authorization. Defaults to the `api_key` passed to the constructor of `PssFleetDataClient`.

        Raises:
            InvalidBoolError: Raised, if a parameter expecting a value of type `bool` received a value that can't be parsed to `bool`. Can also be part of a body parameter.\n
            InvalidDateTimeError: Raised, if a parameter expecting a value of type `datetime` received a value that can't be parsed to `datetime`. Can also be part of a body parameter.\n
            InvalidJsonUpload: Raised, if the uploaded JSON file is invalid.\n
            InvalidNumberError: Raised, if a parameter expecting a value of type `int` or `float` received a value that can't be parsed to `int` or `float`. Can also be part of a body parameter.\n
            MissingAccessError: Raised, if the client is not allowed to access the requested endpoint.\n
            NonUniqueCollectionIdError: Raised, if a `Collection` with its `collection_id` already exists in the database.\n
            NonUniqueTimestampError: Raised, if a `Collection` with its `timestamp` already exists in the database.\n
            NotAuthenticatedError: Raised, if the requested endpojnt requires authentication, but the client is not authenticated.\n
            ParameterValidationError: Raised, if a body, path or query parameter or header received an invalid value.\n
            ParameterValueError: Raised, if a body, path or query parameter or header received an invalid value.\n
            TooManyRequestsError: Raised, if the client is sending too many requests and is getting rate-limited.\n
            SchemaVersionMismatch: Raised, if the request contains a `Collection` in a schema that doesn't match the expected or specified `schema_version`.\n
            ServerError: Raised, if an internal server error occurs.\n
            UnsupportedMediaTypeError: Raised, if the requested endpoint received a body parameter of an unsupported media type.\n
            UnsupportedSchemaError: Raised, if the requested endpoint received a `Collection` of an unknown schema.

        Returns:
            CollectionMetadata: The metadata of the newly created `Collection`.
        """
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

    async def delete_collection(self, collection_id: int, api_key: Optional[str] = None) -> bool:
        """Deletes the `Collection` with the given `collection_id`.

        Args:
            collection_id (int): The `collection_id` of the `Collection` to be deleted.
            api_key (str, optional): The API key to send for authorization. Defaults to the `api_key` passed to the constructor of `PssFleetDataClient`.

        Raises:
            CollectionNotDeletedError: Raised, if the requested `Collection` could not be deleted due to an internal server error.\n
            CollectionNotFoundError: Raised, if a `Collection` with the provided `collection_id` was not found.\n
            InvalidCollectionIdError: Raised, if the path parameter `collection_id` received a value that can't be parsed to `int`.\n
            MissingAccessError: Raised, if the client is not allowed to access the requested endpoint.\n
            NotAuthenticatedError: Raised, if the requested endpojnt requires authentication, but the client is not authenticated.\n
            TooManyRequestsError: Raised, if the client is sending too many requests and is getting rate-limited.\n
            ServerError: Raised, if an internal server error occurs.

        Returns:
            bool: `True`, if the `Collection` was deleted.
        """
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
        interval: Optional[ParameterInterval] = ParameterInterval.MONTHLY,
        desc: Optional[bool] = False,
        skip: Optional[int] = 0,
        take: Optional[int] = 100,
    ) -> list[AllianceHistory]:
        """Retrieves the history of the `Alliance` with the specified `alliance_id`.

        Args:
            alliance_id (int): The `AllianceId` of the `Alliance` to be retrieved.
            from_date (datetime, optional): The earliest date for which to return results. Defaults to `None`.
            to_date (datetime, optional): The latest date for which to return results. Defaults to `None`.
            interval (ParameterInterval, optional): The interval of the data to return, either hourly, end of day or end of month. Defaults to `ParameterInterval.MONTHLY`.
            desc (bool, optional): Determines, if the results should be returned in descending order. Defaults to `False`.
            skip (int, optional): The number of results to skip in the response. Defaults to `0`.
            take (int, optional): The number of results to be returned. Defaults to `100`.

        Raises:
            AllianceNotFoundError: Raised, if an `Alliance` with the provided `alliance_id` was not found.\n
            FromDateAfterToDateError: Raised, if the parameters `fromDate` and `toDate` have been specified and `fromDate` is greater than `toDate`.\n
            FromDateTooEarlyError: Raised, if the parameter `fromDate` is lower than the PSS start date.\n
            InvalidAllianceIdError: Raised, if the path parameter `alliance_id` received a value that can't be parsed to `int`.\n
            InvalidDescError: Raised, if the query parameter `desc` received a value that can't be parsed to `bool`.\n
            InvalidFromDateError: Raised, if the query parameter `fromDate` received a value that can't be parsed to `datetime`.\n
            InvalidIntervalError: Raised, if the query parameter `interval` received a value that can't be parsed to `ParameterInterval`.\n
            InvalidSkipError: Raised, if the query parameter `skip` received a value that can't be parsed to `int`.\n
            InvalidTakeError: Raised, if the query parameter `take` received a value that can't be parsed to `int`.\n
            InvalidToDateError: Raised, if the query parameter `toDate` received a value that can't be parsed to `datetime`.\n
            ToDateTooEarlyError: Raised, if the parameter `toDate` is lower than the PSS start date.\n
            TooManyRequestsError: Raised, if the client is sending too many requests and is getting rate-limited.\n
            ServerError: Raised, if an internal server error occurs.

        Returns:
            list[AllianceHistory]: A list of objects representing `Alliance` data at specific points in time.
        """
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

    async def get_alliance_from_collection(self, collection_id: int, alliance_id: int) -> AllianceHistory:
        """Retrieves data of a specific `Alliance` from a specific `Collection`. Includes the `Alliance`'s members, if applicable.

        Args:
            collection_id (int): The `collection_id` of the `Collection` to obtain the data from.
            alliance_id (int): The `AllianceId` of the `Alliance` to obtain.

        Raises:
            AllianceNotFoundError: Raised, if an `Alliance` with the provided `alliance_id` was not found in the `Collection`.\n
            CollectionNotFoundError: Raised, if a `Collection` with the provided `collection_id` was not found.\n
            InvalidAllianceIdError: Raised, if the path parameter `alliance_id` received a value that can't be parsed to `int`.\n
            InvalidCollectionIdError: Raised, if the path parameter `collection_id` received a value that can't be parsed to `int`.\n
            TooManyRequestsError: Raised, if the client is sending too many requests and is getting rate-limited.\n
            ServerError: Raised, if an internal server error occurs.

        Returns:
            AllianceHistory: An object containing the metadata of the `Collection`, the `Alliance` data and optional `User`s data.
        """
        response = await self._get(f"/collections/{collection_id}/alliances/{alliance_id}")
        alliance_history = FromResponse.to_alliance_history(response)
        return alliance_history

    async def get_alliances_from_collection(self, collection_id: int) -> tuple[Optional[CollectionMetadata], list[PssAlliance]]:
        """Retrieves all `Alliance` data from a the specified `Collection` without their members.

        Args:
            collection_id (int): The `collection_id` of the the `Collection` to be retrieved.

        Raises:
            CollectionNotFoundError: Raised, if a `Collection` with the provided `collection_id` was not found.\n
            InvalidCollectionIdError: Raised, if the path parameter `collection_id` received a value that can't be parsed to `int`.\n
            TooManyRequestsError: Raised, if the client is sending too many requests and is getting rate-limited.\n
            ServerError: Raised, if an internal server error occurs.

        Returns:
            tuple[CollectionMetadata, list[pssapi.entities.Alliance]]: The metadata of the requested `Collection` and its `Alliance` data. Does not include any `User` data.
        """
        response = await self._get(f"/collections/{collection_id}/alliances")
        collection = FromResponse.to_collection(response)

        if not collection:
            return None, []

        return (collection.metadata, collection.alliances)

    async def get_collection(self, collection_id: int) -> Collection:
        """Retrieves all data from the `Collection` with the specified `collection_id`.

        Args:
            collection_id (int): The `collection_id` of the the `Collection` to be retrieved.

        Raises:
            CollectionNotFoundError: Raised, if a `Collection` with the provided `collection_id` was not found.\n
            InvalidCollectionIdError: Raised, if the path parameter `collection_id` received a value that can't be parsed to `int`.\n
            TooManyRequestsError: Raised, if the client is sending too many requests and is getting rate-limited.\n
            ServerError: Raised, if an internal server error occurs.

        Returns:
            Collection: The requested `Collection`.
        """
        response = await self._get(f"/collections/{collection_id}")
        collection = FromResponse.to_collection(response)
        return collection

    async def get_collections(
        self,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        interval: Optional[ParameterInterval] = ParameterInterval.MONTHLY,
        desc: Optional[bool] = False,
        skip: Optional[int] = 0,
        take: Optional[int] = 100,
    ) -> list[CollectionMetadata]:
        """Retrieves a list of metadatas of `Collections` meeting the specified criteria.

        Args:
            from_date (datetime, optional): The earliest date for which to return results. Defaults to `None`.
            to_date (datetime, optional): The latest date for which to return results. Defaults to `None`.
            interval (ParameterInterval, optional): The interval of the data to return, either hourly, end of day or end of month. Defaults to `ParameterInterval.MONTHLY`.
            desc (bool, optional): Determines, if the results should be returned in descending order. Defaults to `False`.
            skip (int, optional): The number of results to skip in the response. Defaults to `0`.
            take (int, optional): The number of results to be returned. Defaults to `100`.

        Raises:
            FromDateAfterToDateError: Raised, if the parameters `fromDate` and `toDate` have been specified and `fromDate` is greater than `toDate`.\n
            FromDateTooEarlyError: Raised, if the parameter `fromDate` is lower than the PSS start date.\n
            InvalidDescError: Raised, if the query parameter `desc` received a value that can't be parsed to `bool`.\n
            InvalidFromDateError: Raised, if the query parameter `fromDate` received a value that can't be parsed to `datetime`.\n
            InvalidIntervalError: Raised, if the query parameter `interval` received a value that can't be parsed to `ParameterInterval`.\n
            InvalidSkipError: Raised, if the query parameter `skip` received a value that can't be parsed to `int`.\n
            InvalidTakeError: Raised, if the query parameter `take` received a value that can't be parsed to `int`.\n
            InvalidToDateError: Raised, if the query parameter `toDate` received a value that can't be parsed to `datetime`.\n
            ToDateTooEarlyError: Raised, if the parameter `toDate` is lower than the PSS start date.\n
            TooManyRequestsError: Raised, if the client is sending too many requests and is getting rate-limited.\n
            ServerError: Raised, if an internal server error occurs.

        Returns:
            list[CollectionMetadata]: A list of metadatas of `Collections` meeting the specified criteria. Might be empty.
        """
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

    async def get_most_recent_collection_by_timestamp(self, timestamp: datetime) -> Optional[Collection]:
        """Retrieves the most recent `Collection` that was recorded before or at the given `timestamp`.
        Checks, if there's one been recorded within an hour before the given `timestamp`.
        If not, checks if there's one been recorded at the most recent end of the day before the given `timestamp`.
        If not, checks if there's one been recorded at the most recent end of the month before the given `timestamp`.\n
        NOTE: Makes 2 to 4 requests to the API.

        Args:
            timestamp (datetime): The point in time to get the most recent `Collection` for.

        Raises:
            TooManyRequestsError: Raised, if the client is sending too many requests and is getting rate-limited.\n
            ServerError: Raised, if an internal server error occurs.

        Returns:
            Optional[Collection]: The `Collection` recorded within an hour before the given `timestamp`.
            If there's none, the `Collection` recorded at the most recent end of the day before the given `timestamp`.
            If there's none, the `Collection` recorded at the most recent end of the month before the given `timestamp`.
            If there's none, `None`.
        """
        collection_metadata = await self.get_most_recent_collection_metadata_by_timestamp(timestamp)
        if collection_metadata:
            collection = await self.get_collection(collection_metadata.collection_id)
            return collection
        return None

    async def get_most_recent_collection_metadata_by_timestamp(self, timestamp: datetime) -> Optional[CollectionMetadata]:
        """Retrieves the metadata of the most recent `Collection` that was recorded before or at the given `timestamp`.
        Checks, if there's one been recorded within an hour before the given `timestamp`.
        If not, checks if there's one been recorded at the most recent end of the day before the given `timestamp`.
        If not, checks if there's one been recorded at the most recent end of the month before the given `timestamp`.\n
        NOTE: Makes 1 to 3 requests to the API.

        Args:
            timestamp (datetime): The point in time to get the most recent `CollectionMetadata` for.

        Raises:
            TooManyRequestsError: Raised, if the client is sending too many requests and is getting rate-limited.\n
            ServerError: Raised, if an internal server error occurs.

        Returns:
            Optional[CollectionMetadata]: The metadata of the `Collection` recorded within an hour before the given `timestamp`.
            If there's none, the metadata of the `Collection` recorded at the most recent end of the day before the given `timestamp`.
            If there's none, the metadata of the `Collection` recorded at the most recent end of the month before the given `timestamp`.
            If there's none, `None`.
        """
        for interval in (ParameterInterval.HOURLY, ParameterInterval.DAILY, ParameterInterval.MONTHLY):
            from_date, to_date = utils.get_most_recent_from_to_date_from_timestamp(timestamp, interval)
            collection_metadatas = await self.get_collections(
                from_date=from_date,
                to_date=to_date,
                interval=ParameterInterval.HOURLY,
                desc=True,
                take=1,
            )
            if collection_metadatas:
                return collection_metadatas[0]
        return None

    async def get_top_100_users_from_collection(
        self,
        collection_id: int,
        skip: Optional[int] = 0,
        take: Optional[int] = 100,
    ) -> tuple[Collection, list[PssUser]]:
        """Retrieves the `User` data of the top 100 players from a the specified `Collection` without their `Alliance`s.\n
        NOTE: For `Collection`s recorded before Jan 25th, 2021, this list is not be accurate, because top 100 players not in a fleet weren't recorded.

        Args:
            collection_id (int): The `collection_id` of the the `Collection` to be retrieved.
            skip (int, optional): The number of results to skip in the response. Defaults to `0`.
            take (int, optional): The number of results to be returned. Defaults to `100`.

        Raises:
            CollectionNotFoundError: Raised, if a `Collection` with the provided `collection_id` was not found.\n
            InvalidCollectionIdError: Raised, if the path parameter `collection_id` received a value that can't be parsed to `int`.\n
            InvalidSkipError: Raised, if the query parameter `skip` received a value that can't be parsed to `int`.\n
            InvalidTakeError: Raised, if the query parameter `take` received a value that can't be parsed to `int`.\n
            TooManyRequestsError: Raised, if the client is sending too many requests and is getting rate-limited.\n
            ServerError: Raised, if an internal server error occurs.

        Returns:
            tuple[CollectionMetadata, list[pssapi.entities.User]]: The metadata of the requested `Collection` and its top 100 `User` data. Does not include any `Alliance` data.
        """
        response = await self._get_with_filter_parameters(f"/collections/{collection_id}/top100Users", skip=skip, take=take)
        collection = FromResponse.to_collection(response)

        if not collection:
            return None, []

        return (collection.metadata, collection.users)

    async def get_user_from_collection(self, collection_id: int, user_id: int) -> UserHistory:
        """Retrieves data of a specific `User` from a specific `Collection`. Includes the `User`'s `Alliance`, if applicable.

        Args:
            collection_id (int): The `collection_id` of the `Collection` to obtain the data from.
            user_id (int): The `Id` of the `User` to obtain.

        Raises:
            CollectionNotFoundError: Raised, if a `Collection` with the provided `collection_id` was not found.\n
            InvalidCollectionIdError: Raised, if the path parameter `collection_id` received a value that can't be parsed to `int`.\n
            InvalidUserIdError: Raised, if the path parameter `user_id` received a value that can't be parsed to `int`.\n
            TooManyRequestsError: Raised, if the client is sending too many requests and is getting rate-limited.\n
            ServerError: Raised, if an internal server error occurs.\n
            UserNotFoundError: Raised, if a `User` with the provided `user_id` was not found in the `Collection`.

        Returns:
            UserHistory: An object containing the metadata of the `Collection`, the `User` data and optional `Alliance` data.
        """
        response = await self._get(f"/collections/{collection_id}/users/{user_id}")
        user_history = FromResponse.to_user_history(response)
        return user_history

    async def get_users_from_collection(self, collection_id: int) -> tuple[CollectionMetadata, list[PssUser]]:
        """Retrieves all `User` data from a the specified `Collection` without their `Alliance`s.

        Args:
            collection_id (int): The `collection_id` of the the `Collection` to be retrieved.

        Raises:
            CollectionNotFoundError: Raised, if a `Collection` with the provided `collection_id` was not found.\n
            InvalidCollectionIdError: Raised, if the path parameter `collection_id` received a value that can't be parsed to `int`.\n
            TooManyRequestsError: Raised, if the client is sending too many requests and is getting rate-limited.\n
            ServerError: Raised, if an internal server error occurs.

        Returns:
            tuple[CollectionMetadata, list[pssapi.entities.User]]: The metadata of the requested `Collection` and its `User` data. Does not include any `Alliance` data.
        """
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
        interval: Optional[ParameterInterval] = ParameterInterval.MONTHLY,
        desc: Optional[bool] = False,
        skip: Optional[int] = 0,
        take: Optional[int] = 100,
    ) -> list[UserHistory]:
        """Retrieves the history of the `User` with the specified `user_id`.

        Args:
            user_id (int): The `Id` of the `User` to be retrieved.
            from_date (datetime, optional): The earliest date for which to return results. Defaults to `None`.
            to_date (datetime, optional): The latest date for which to return results. Defaults to `None`.
            interval (ParameterInterval, optional): The interval of the data to return, either hourly, end of day or end of month. Defaults to `ParameterInterval.MONTHLY`.
            desc (bool, optional): Determines, if the results should be returned in descending order. Defaults to `False`.
            skip (int, optional): The number of results to skip in the response. Defaults to `0`.
            take (int, optional): The number of results to be returned. Defaults to `100`.

        Raises:
            FromDateAfterToDateError: Raised, if the parameters `fromDate` and `toDate` have been specified and `fromDate` is greater than `toDate`.\n
            FromDateTooEarlyError: Raised, if the parameter `fromDate` is lower than the PSS start date.\n
            InvalidDescError: Raised, if the query parameter `desc` received a value that can't be parsed to `bool`.\n
            InvalidFromDateError: Raised, if the query parameter `fromDate` received a value that can't be parsed to `datetime`.\n
            InvalidIntervalError: Raised, if the query parameter `interval` received a value that can't be parsed to `ParameterInterval`.\n
            InvalidSkipError: Raised, if the query parameter `skip` received a value that can't be parsed to `int`.\n
            InvalidTakeError: Raised, if the query parameter `take` received a value that can't be parsed to `int`.\n
            InvalidToDateError: Raised, if the query parameter `toDate` received a value that can't be parsed to `datetime`.\n
            InvalidUserIdError: Raised, if the path parameter `user_id` received a value that can't be parsed to `int`.\n
            ToDateTooEarlyError: Raised, if the parameter `toDate` is lower than the PSS start date.\n
            TooManyRequestsError: Raised, if the client is sending too many requests and is getting rate-limited.\n
            ServerError: Raised, if an internal server error occurs.\n
            UserNotFoundError: Raised, if a `User` with the provided `user_id` was not found.

        Returns:
            list[UserHistory]: A list of objects representing `User` data at specific points in time.
        """
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

    async def ping(self) -> str:
        """Sends a ping to the API.

        Returns:
            str: Pong!
        """
        response = await self._get("/ping")
        return response.json()["ping"]

    async def update_collection(self, collection_id: int, file_path: Union[str, Path], api_key: Optional[str] = None) -> CollectionMetadata:
        """Uploads the `Collection` at the given `file_path` to overwrite the data of the specified `collection_id`.

        Args:
            colection_id (int): The `collectionId` of the `Collection` file to be updated.
            file_path (str | Path): The path to the `Collection` file to be uploaded.
            api_key (str, optional): The API key to send for authorization. Defaults to the `api_key` passed to the constructor of `PssFleetDataClient`.

        Raises:
            ConflictError: Raised, if the `timestamp` of the file to be uploaded differs from the `timestamp` of the `Collection` to be updated.\n
            InvalidBoolError: Raised, if a parameter expecting a value of type `bool` received a value that can't be parsed to `bool`. Can also be part of a body parameter.\n
            InvalidDateTimeError: Raised, if a parameter expecting a value of type `datetime` received a value that can't be parsed to `datetime`. Can also be part of a body parameter.\n
            InvalidJsonUpload: Raised, if the uploaded JSON file is invalid.\n
            InvalidNumberError: Raised, if a parameter expecting a value of type `int` or `float` received a value that can't be parsed to `int` or `float`. Can also be part of a body parameter.\n
            MissingAccessError: Raised, if the client is not allowed to access the requested endpoint.\n
            NonUniqueCollectionIdError: Raised, if a `Collection` with its `collection_id` already exists in the database.\n
            NotAuthenticatedError: Raised, if the requested endpojnt requires authentication, but the client is not authenticated.\n
            ParameterValidationError: Raised, if a body, path or query parameter or header received an invalid value.\n
            ParameterValueError: Raised, if a body, path or query parameter or header received an invalid value.\n
            TooManyRequestsError: Raised, if the client is sending too many requests and is getting rate-limited.\n
            SchemaVersionMismatch: Raised, if the request contains a `Collection` in a schema that doesn't match the expected or specified `schema_version`.\n
            ServerError: Raised, if an internal server error occurs.\n
            UnsupportedMediaTypeError: Raised, if the requested endpoint received a body parameter of an unsupported media type.\n
            UnsupportedSchemaError: Raised, if the requested endpoint received a `Collection` of an unknown schema.

        Returns:
            CollectionMetadata: The metadata of the `Collection` created.
        """
        if not isinstance(file_path, (str, Path)):
            raise TypeError("Parameter `file` must be of type `str`.")

        api_key = api_key or self.api_key

        with open(file_path, "rb") as fp:
            files = {"collection_file": ("collection", fp, "application/json")}
            response = await self._put_with_api_key(
                f"/collections/upload/{collection_id}",
                api_key=api_key,
                files=files,
            )

        result = FromResponse.to_collection_metadata(response)
        return result

    async def upload_collection(self, file_path: Union[str, Path], api_key: Optional[str] = None) -> CollectionMetadata:
        """Uploads the `Collection` at the given `file_path`.

        Args:
            file_path (str | Path): The path to the `Collection` file to be uploaded.
            api_key (str, optional): The API key to send for authorization. Defaults to the `api_key` passed to the constructor of `PssFleetDataClient`.

        Raises:
            InvalidBoolError: Raised, if a parameter expecting a value of type `bool` received a value that can't be parsed to `bool`. Can also be part of a body parameter.\n
            InvalidDateTimeError: Raised, if a parameter expecting a value of type `datetime` received a value that can't be parsed to `datetime`. Can also be part of a body parameter.\n
            InvalidJsonUpload: Raised, if the uploaded JSON file is invalid.\n
            InvalidNumberError: Raised, if a parameter expecting a value of type `int` or `float` received a value that can't be parsed to `int` or `float`. Can also be part of a body parameter.\n
            MissingAccessError: Raised, if the client is not allowed to access the requested endpoint.\n
            NonUniqueCollectionIdError: Raised, if a `Collection` with its `collection_id` already exists in the database.\n
            NonUniqueTimestampError: Raised, if a `Collection` with its `timestamp` already exists in the database.\n
            NotAuthenticatedError: Raised, if the requested endpojnt requires authentication, but the client is not authenticated.\n
            ParameterValidationError: Raised, if a body, path or query parameter or header received an invalid value.\n
            ParameterValueError: Raised, if a body, path or query parameter or header received an invalid value.\n
            TooManyRequestsError: Raised, if the client is sending too many requests and is getting rate-limited.\n
            SchemaVersionMismatch: Raised, if the request contains a `Collection` in a schema that doesn't match the expected or specified `schema_version`.\n
            ServerError: Raised, if an internal server error occurs.\n
            UnsupportedMediaTypeError: Raised, if the requested endpoint received a body parameter of an unsupported media type.\n
            UnsupportedSchemaError: Raised, if the requested endpoint received a `Collection` of an unknown schema.

        Returns:
            CollectionMetadata: The metadata of the `Collection` created.
        """
        if not isinstance(file_path, (str, Path)):
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
        """Deletes the resource at the specified `path`.

        Args:
            path (str): The path of the endpoint relative to the API server's base URL.
            params (dict[str, Any], optional): A collection of query parameters to be sent with the request. Defaults to `None`.
            headers (dict[str, Any], optional): A collection of headers to be sent with the request. Defaults to `None`.

        Raises:
            CollectionNotDeletedError: Raised, if the requested `Collection` could not be deleted due to an internal server error.\n
            CollectionNotFoundError: Raised, if a `Collection` with the provided `collection_id` was not found.\n
            InvalidCollectionIdError: Raised, if the path parameter `collection_id` received a value that can't be parsed to `int`.\n
            InvalidNumberError: Raised, if a parameter expecting a value of type `int` or `float` received a value that can't be parsed to `int` or `float`. Can also be part of a body parameter.\n
            MethodNotAllowedError: Raised, if the request method is not allowed for the requested endpoint.\n
            MissingAccessError: Raised, if the client is not allowed to access the requested endpoint.\n
            NotAuthenticatedError: Raised, if the requested endpojnt requires authentication, but the client is not authenticated.\n
            NotFoundError: Raised, if a resource was not found.\n
            ParameterValidationError: Raised, if a body, path or query parameter or header received an invalid value.\n
            ParameterFormatError: Raised, if a body, path or query parameter or header received a value in a format that can't be parsed to the expected type.\n
            ParameterValueError: Raised, if a body, path or query parameter or header received an invalid value.\n
            TooManyRequestsError: Raised, if the client is sending too many requests and is getting rate-limited.\n
            ServerError: Raised, if an internal server error occurs.

        Returns:
            httpx.Response: The response from the API.
        """
        request_headers = utils.merge_headers(self.__http_client.headers, headers)
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
        """Deletes the resource at the specified `path` using the specified `api_key`.

        Args:
            path (str): The path of the endpoint relative to the API server's base URL.
            api_key (str, optional): The api key to be sent with the request for authorization. Defaults to `None`.
            params (dict[str, Any], optional): A collection of query parameters to be sent with the request. Defaults to `None`.
            headers (dict[str, Any], optional): A collection of headers to be sent with the request. Defaults to `None`.

        Raises:
            CollectionNotDeletedError: Raised, if the requested `Collection` could not be deleted due to an internal server error.\n
            CollectionNotFoundError: Raised, if a `Collection` with the provided `collection_id` was not found.\n
            InvalidCollectionIdError: Raised, if the path parameter `collection_id` received a value that can't be parsed to `int`.\n
            InvalidNumberError: Raised, if a parameter expecting a value of type `int` or `float` received a value that can't be parsed to `int` or `float`. Can also be part of a body parameter.\n
            MethodNotAllowedError: Raised, if the request method is not allowed for the requested endpoint.\n
            MissingAccessError: Raised, if the client is not allowed to access the requested endpoint.\n
            NotAuthenticatedError: Raised, if the requested endpojnt requires authentication, but the client is not authenticated.\n
            NotFoundError: Raised, if a resource was not found.\n
            ParameterValidationError: Raised, if a body, path or query parameter or header received an invalid value.\n
            ParameterFormatError: Raised, if a body, path or query parameter or header received a value in a format that can't be parsed to the expected type.\n
            ParameterValueError: Raised, if a body, path or query parameter or header received an invalid value.\n
            TooManyRequestsError: Raised, if the client is sending too many requests and is getting rate-limited.\n
            ServerError: Raised, if an internal server error occurs.

        Returns:
            httpx.Response: The response from the API.
        """
        headers = headers or {}
        headers["Authorization"] = api_key or self.__api_key

        response = await self._delete(
            path,
            params=params,
            headers=headers,
        )
        return response

    async def _get(self, path: str, params: Optional[dict[str, Any]] = None, headers: Optional[dict[str, Any]] = None) -> Response:
        """Sends a request to get resources from the API with query parameters.

        Args:
            path (str): The path of the endpoint relative to the API server's base URL.
            params (dict[str, Any], optional): A collection of query parameters to be sent with the request. Defaults to `None`.
            headers (dict[str, Any], optional): A collection of headers to be sent with the request. Defaults to `None`.

        Raises:
            AllianceNotFoundError: Raised, if an `Alliance` with the provided `alliance_id` was not found.\n
            CollectionNotFoundError: Raised, if a `Collection` with the provided `collection_id` was not found.\n
            FromDateAfterToDateError: Raised, if the parameters `fromDate` and `toDate` have been specified and `fromDate` is greater than `toDate`.\n
            FromDateTooEarlyError: Raised, if the parameter `fromDate` is lower than the PSS start date.\n
            InvalidAllianceIdError: Raised, if the path parameter `alliance_id` received a value that can't be parsed to `int`.\n
            InvalidBoolError: Raised, if a parameter expecting a value of type `bool` received a value that can't be parsed to `bool`. Can also be part of a body parameter.\n
            InvalidCollectionIdError: Raised, if the path parameter `collection_id` received a value that can't be parsed to `int`.\n
            InvalidDateTimeError: Raised, if a parameter expecting a value of type `datetime` received a value that can't be parsed to `datetime`. Can also be part of a body parameter.\n
            InvalidDescError: Raised, if the query parameter `desc` received a value that can't be parsed to `bool`.\n
            InvalidFromDateError: Raised, if the query parameter `fromDate` received a value that can't be parsed to `datetime`.\n
            InvalidIntervalError: Raised, if the query parameter `interval` received a value that can't be parsed to `ParameterInterval`.\n
            InvalidNumberError: Raised, if a parameter expecting a value of type `int` or `float` received a value that can't be parsed to `int` or `float`. Can also be part of a body parameter.\n
            InvalidSkipError: Raised, if the query parameter `skip` received a value that can't be parsed to `int`.\n
            InvalidTakeError: Raised, if the query parameter `take` received a value that can't be parsed to `int`.\n
            InvalidToDateError: Raised, if the query parameter `toDate` received a value that can't be parsed to `datetime`.\n
            InvalidUserIdError: Raised, if the path parameter `user_id` received a value that can't be parsed to `int`.\n
            MethodNotAllowedError: Raised, if the request method is not allowed for the requested endpoint.\n
            NotFoundError: Raised, if a resource was not found.\n
            ParameterValidationError: Raised, if a body, path or query parameter or header received an invalid value.\n
            ParameterFormatError: Raised, if a body, path or query parameter or header received a value in a format that can't be parsed to the expected type.\n
            ParameterValueError: Raised, if a body, path or query parameter or header received an invalid value.\n
            ToDateTooEarlyError: Raised, if the parameter `toDate` is lower than the PSS start date.\n
            TooManyRequestsError: Raised, if the client is sending too many requests and is getting rate-limited.\n
            ServerError: Raised, if an internal server error occurs.\n
            UserNotFoundError: Raised, if a `User` with the provided `user_id` was not found.

        Returns:
            httpx.Response: The response from the API.
        """
        request_headers = utils.merge_headers(self.__http_client.headers, headers)
        response = await self.__http_client.get(path, params=params, headers=request_headers)
        _raise_on_error(response)
        return response

    async def _get_with_filter_parameters(
        self,
        path: str,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        interval: Optional[ParameterInterval] = ParameterInterval.MONTHLY,
        desc: Optional[bool] = False,
        skip: Optional[int] = 0,
        take: Optional[int] = 100,
    ) -> Response:
        """Sends a request to get resources from the API with query parameters for filtering the results.

        Args:
            path (str): The path of the endpoint relative to the API server's base URL.
            from_date (datetime, optional): The earliest date for which to return results. Defaults to `None`.
            to_date (datetime, optional): The latest date for which to return results. Defaults to `None`.
            interval (ParameterInterval, optional): The interval of the data to return, either hourly, end of day or end of month. Defaults to `ParameterInterval.MONTHLY`.
            desc (bool, optional): Determines, if the results should be returned in descending order. Defaults to `False`.
            skip (int, optional): The number of results to skip in the response. Defaults to `0`.
            take (int, optional): The number of results to be returned. Defaults to `100`.

        Raises:
            AllianceNotFoundError: Raised, if an `Alliance` with the provided `alliance_id` was not found.\n
            CollectionNotFoundError: Raised, if a `Collection` with the provided `collection_id` was not found.\n
            FromDateAfterToDateError: Raised, if the parameters `fromDate` and `toDate` have been specified and `fromDate` is greater than `toDate`.\n
            FromDateTooEarlyError: Raised, if the parameter `fromDate` is lower than the PSS start date.\n
            InvalidAllianceIdError: Raised, if the path parameter `alliance_id` received a value that can't be parsed to `int`.\n
            InvalidBoolError: Raised, if a parameter expecting a value of type `bool` received a value that can't be parsed to `bool`. Can also be part of a body parameter.\n
            InvalidCollectionIdError: Raised, if the path parameter `collection_id` received a value that can't be parsed to `int`.\n
            InvalidDateTimeError: Raised, if a parameter expecting a value of type `datetime` received a value that can't be parsed to `datetime`. Can also be part of a body parameter.\n
            InvalidDescError: Raised, if the query parameter `desc` received a value that can't be parsed to `bool`.\n
            InvalidFromDateError: Raised, if the query parameter `fromDate` received a value that can't be parsed to `datetime`.\n
            InvalidIntervalError: Raised, if the query parameter `interval` received a value that can't be parsed to `ParameterInterval`.\n
            InvalidNumberError: Raised, if a parameter expecting a value of type `int` or `float` received a value that can't be parsed to `int` or `float`. Can also be part of a body parameter.\n
            InvalidSkipError: Raised, if the query parameter `skip` received a value that can't be parsed to `int`.\n
            InvalidTakeError: Raised, if the query parameter `take` received a value that can't be parsed to `int`.\n
            InvalidToDateError: Raised, if the query parameter `toDate` received a value that can't be parsed to `datetime`.\n
            InvalidUserIdError: Raised, if the path parameter `user_id` received a value that can't be parsed to `int`.\n
            MethodNotAllowedError: Raised, if the request method is not allowed for the requested endpoint.\n
            NotFoundError: Raised, if a resource was not found.\n
            ParameterValidationError: Raised, if a body, path or query parameter or header received an invalid value.\n
            ParameterFormatError: Raised, if a body, path or query parameter or header received a value in a format that can't be parsed to the expected type.\n
            ParameterValueError: Raised, if a body, path or query parameter or header received an invalid value.\n
            ToDateTooEarlyError: Raised, if the parameter `toDate` is lower than the PSS start date.\n
            TooManyRequestsError: Raised, if the client is sending too many requests and is getting rate-limited.\n
            ServerError: Raised, if an internal server error occurs.\n
            UserNotFoundError: Raised, if a `User` with the provided `user_id` was not found.

        Returns:
            httpx.Response: The response from the API.
        """
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
        """Posts an HTTP request to the given API endpoint.

        Args:
            path (str): The path of the endpoint relative to the API server's base URL.
            json (dict[str, Any], optional): A request body to be sent with the request. Defaults to `None`.
            files (dict[str, tuple], optional): A collection of file to be sent with the request. Defaults to `None`.
            params (dict[str, Any], optional): A collection of query parameters to be sent with the request. Defaults to `None`.
            headers (dict[str, Any], optional): A collection of headers to be sent with the request. Defaults to `None`.

        Raises:
            ConflictError: Raised, if a resource could not be created due to conflicting data.\n
            InvalidBoolError: Raised, if a parameter expecting a value of type `bool` received a value that can't be parsed to `bool`. Can also be part of a body parameter.\n
            InvalidDateTimeError: Raised, if a parameter expecting a value of type `datetime` received a value that can't be parsed to `datetime`. Can also be part of a body parameter.\n
            InvalidDescError: Raised, if the query parameter `desc` received a value that can't be parsed to `bool`.\n
            InvalidIntervalError: Raised, if the query parameter `interval` received a value that can't be parsed to `ParameterInterval`.\n
            InvalidJsonUpload: Raised, if the uploaded JSON file is invalid.\n
            InvalidNumberError: Raised, if a parameter expecting a value of type `int` or `float` received a value that can't be parsed to `int` or `float`. Can also be part of a body parameter.\n
            MethodNotAllowedError: Raised, if the request method is not allowed for the requested endpoint.\n
            MissingAccessError: Raised, if the client is not allowed to access the requested endpoint.\n
            NonUniqueCollectionIdError: Raised, if a `Collection` with its `collection_id` already exists in the database.\n
            NonUniqueTimestampError: Raised, if a `Collection` with its `timestamp` already exists in the database.\n
            NotAuthenticatedError: Raised, if the requested endpojnt requires authentication, but the client is not authenticated.\n
            ParameterValidationError: Raised, if a body, path or query parameter or header received an invalid value.\n
            ParameterFormatError: Raised, if a body, path or query parameter or header received a value in a format that can't be parsed to the expected type.\n
            ParameterValueError: Raised, if a body, path or query parameter or header received an invalid value.\n
            TooManyRequestsError: Raised, if the client is sending too many requests and is getting rate-limited.\n
            SchemaVersionMismatch: Raised, if the request contains a `Collection` in a schema that doesn't match the expected or specified `schema_version`.\n
            ServerError: Raised, if an internal server error occurs.\n
            UnsupportedMediaTypeError: Raised, if the requested endpoint received a body parameter of an unsupported media type.\n
            UnsupportedSchemaError: Raised, if the requested endpoint received a `Collection` of an unknown schema.

        Returns:
            httpx.Response: The response from the API.
        """
        request_headers = utils.merge_headers(self.__http_client.headers, headers)

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
        """Posts an HTTP request to the given API endpoint.

        Args:
            path (str): The path of the endpoint relative to the API server's base URL.
            api_key (str, optional): The api key to be sent with the request for authorization. Defaults to `None`.
            json (dict[str, Any], optional): A request body to be sent with the request. Defaults to `None`.
            files (dict[str, tuple], optional): A collection of file to be sent with the request. Defaults to `None`.
            params (dict[str, Any], optional): A collection of query parameters to be sent with the request. Defaults to `None`.
            headers (dict[str, Any], optional): A collection of headers to be sent with the request. Defaults to `None`.

        Raises:
            ConflictError: Raised, if a resource could not be created due to conflicting data.\n
            InvalidBoolError: Raised, if a parameter expecting a value of type `bool` received a value that can't be parsed to `bool`. Can also be part of a body parameter.\n
            InvalidDateTimeError: Raised, if a parameter expecting a value of type `datetime` received a value that can't be parsed to `datetime`. Can also be part of a body parameter.\n
            InvalidDescError: Raised, if the query parameter `desc` received a value that can't be parsed to `bool`.\n
            InvalidIntervalError: Raised, if the query parameter `interval` received a value that can't be parsed to `ParameterInterval`.\n
            InvalidJsonUpload: Raised, if the uploaded JSON file is invalid.\n
            InvalidNumberError: Raised, if a parameter expecting a value of type `int` or `float` received a value that can't be parsed to `int` or `float`. Can also be part of a body parameter.\n
            MethodNotAllowedError: Raised, if the request method is not allowed for the requested endpoint.\n
            MissingAccessError: Raised, if the client is not allowed to access the requested endpoint.\n
            NonUniqueCollectionIdError: Raised, if a `Collection` with its `collection_id` already exists in the database.\n
            NonUniqueTimestampError: Raised, if a `Collection` with its `timestamp` already exists in the database.\n
            NotAuthenticatedError: Raised, if the requested endpojnt requires authentication, but the client is not authenticated.\n
            ParameterValidationError: Raised, if a body, path or query parameter or header received an invalid value.\n
            ParameterFormatError: Raised, if a body, path or query parameter or header received a value in a format that can't be parsed to the expected type.\n
            ParameterValueError: Raised, if a body, path or query parameter or header received an invalid value.\n
            TooManyRequestsError: Raised, if the client is sending too many requests and is getting rate-limited.\n
            SchemaVersionMismatch: Raised, if the request contains a `Collection` in a schema that doesn't match the expected or specified `schema_version`.\n
            ServerError: Raised, if an internal server error occurs.\n
            UnsupportedMediaTypeError: Raised, if the requested endpoint received a body parameter of an unsupported media type.\n
            UnsupportedSchemaError: Raised, if the requested endpoint received a `Collection` of an unknown schema.

        Returns:
            httpx.Response: The response from the API.
        """
        headers = headers or {}
        headers["Authorization"] = api_key or self.__api_key or ""

        response = await self._post(path, json=json, files=files, params=params, headers=headers)
        return response

    async def _put(
        self,
        path: str,
        json: Optional[dict[str, Any]] = None,
        files: Optional[dict[str, tuple]] = None,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, Any]] = None,
    ) -> Response:
        """Puts an HTTP request to the given API endpoint.

        Args:
            path (str): The path of the endpoint relative to the API server's base URL.
            json (dict[str, Any], optional): A request body to be sent with the request. Defaults to `None`.
            files (dict[str, tuple], optional): A collection of file to be sent with the request. Defaults to `None`.
            params (dict[str, Any], optional): A collection of query parameters to be sent with the request. Defaults to `None`.
            headers (dict[str, Any], optional): A collection of headers to be sent with the request. Defaults to `None`.

        Raises:
            ConflictError: Raised, if a resource could not be created due to conflicting data.\n
            InvalidBoolError: Raised, if a parameter expecting a value of type `bool` received a value that can't be parsed to `bool`. Can also be part of a body parameter.\n
            InvalidDateTimeError: Raised, if a parameter expecting a value of type `datetime` received a value that can't be parsed to `datetime`. Can also be part of a body parameter.\n
            InvalidDescError: Raised, if the query parameter `desc` received a value that can't be parsed to `bool`.\n
            InvalidIntervalError: Raised, if the query parameter `interval` received a value that can't be parsed to `ParameterInterval`.\n
            InvalidJsonUpload: Raised, if the uploaded JSON file is invalid.\n
            InvalidNumberError: Raised, if a parameter expecting a value of type `int` or `float` received a value that can't be parsed to `int` or `float`. Can also be part of a body parameter.\n
            MethodNotAllowedError: Raised, if the request method is not allowed for the requested endpoint.\n
            MissingAccessError: Raised, if the client is not allowed to access the requested endpoint.\n
            NonUniqueCollectionIdError: Raised, if a `Collection` with its `collection_id` already exists in the database.\n
            NonUniqueTimestampError: Raised, if a `Collection` with its `timestamp` already exists in the database.\n
            NotAuthenticatedError: Raised, if the requested endpojnt requires authentication, but the client is not authenticated.\n
            ParameterValidationError: Raised, if a body, path or query parameter or header received an invalid value.\n
            ParameterFormatError: Raised, if a body, path or query parameter or header received a value in a format that can't be parsed to the expected type.\n
            ParameterValueError: Raised, if a body, path or query parameter or header received an invalid value.\n
            TooManyRequestsError: Raised, if the client is sending too many requests and is getting rate-limited.\n
            SchemaVersionMismatch: Raised, if the request contains a `Collection` in a schema that doesn't match the expected or specified `schema_version`.\n
            ServerError: Raised, if an internal server error occurs.\n
            UnsupportedMediaTypeError: Raised, if the requested endpoint received a body parameter of an unsupported media type.\n
            UnsupportedSchemaError: Raised, if the requested endpoint received a `Collection` of an unknown schema.

        Returns:
            httpx.Response: The response from the API.
        """
        request_headers = utils.merge_headers(self.__http_client.headers, headers)

        response = await self.__http_client.put(path, json=json, files=files, params=params, headers=request_headers)
        _raise_on_error(response)
        return response

    async def _put_with_api_key(
        self,
        path: str,
        api_key: Optional[str] = None,
        json: Optional[dict[str, Any]] = None,
        files: Optional[dict[str, tuple]] = None,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, Any]] = None,
    ) -> Response:
        """Posts an HTTP request to the given API endpoint.

        Args:
            path (str): The path of the endpoint relative to the API server's base URL.
            api_key (str, optional): The api key to be sent with the request for authorization. Defaults to `None`.
            json (dict[str, Any], optional): A request body to be sent with the request. Defaults to `None`.
            files (dict[str, tuple], optional): A collection of file to be sent with the request. Defaults to `None`.
            params (dict[str, Any], optional): A collection of query parameters to be sent with the request. Defaults to `None`.
            headers (dict[str, Any], optional): A collection of headers to be sent with the request. Defaults to `None`.

        Raises:
            ConflictError: Raised, if a resource could not be created due to conflicting data.\n
            InvalidBoolError: Raised, if a parameter expecting a value of type `bool` received a value that can't be parsed to `bool`. Can also be part of a body parameter.\n
            InvalidDateTimeError: Raised, if a parameter expecting a value of type `datetime` received a value that can't be parsed to `datetime`. Can also be part of a body parameter.\n
            InvalidDescError: Raised, if the query parameter `desc` received a value that can't be parsed to `bool`.\n
            InvalidIntervalError: Raised, if the query parameter `interval` received a value that can't be parsed to `ParameterInterval`.\n
            InvalidJsonUpload: Raised, if the uploaded JSON file is invalid.\n
            InvalidNumberError: Raised, if a parameter expecting a value of type `int` or `float` received a value that can't be parsed to `int` or `float`. Can also be part of a body parameter.\n
            MethodNotAllowedError: Raised, if the request method is not allowed for the requested endpoint.\n
            MissingAccessError: Raised, if the client is not allowed to access the requested endpoint.\n
            NonUniqueCollectionIdError: Raised, if a `Collection` with its `collection_id` already exists in the database.\n
            NonUniqueTimestampError: Raised, if a `Collection` with its `timestamp` already exists in the database.\n
            NotAuthenticatedError: Raised, if the requested endpojnt requires authentication, but the client is not authenticated.\n
            ParameterValidationError: Raised, if a body, path or query parameter or header received an invalid value.\n
            ParameterFormatError: Raised, if a body, path or query parameter or header received a value in a format that can't be parsed to the expected type.\n
            ParameterValueError: Raised, if a body, path or query parameter or header received an invalid value.\n
            TooManyRequestsError: Raised, if the client is sending too many requests and is getting rate-limited.\n
            SchemaVersionMismatch: Raised, if the request contains a `Collection` in a schema that doesn't match the expected or specified `schema_version`.\n
            ServerError: Raised, if an internal server error occurs.\n
            UnsupportedMediaTypeError: Raised, if the requested endpoint received a body parameter of an unsupported media type.\n
            UnsupportedSchemaError: Raised, if the requested endpoint received a `Collection` of an unknown schema.

        Returns:
            httpx.Response: The response from the API.
        """
        headers = headers or {}
        headers["Authorization"] = api_key or self.__api_key or ""

        response = await self._put(path, json=json, files=files, params=params, headers=headers)
        return response


# Helper


def _raise_on_error(response: Response):
    """Raises an `ApiError`, if the API returned an error response. Does nothing, if the returned HTTP status code is not 401, 403, 404, 405, 409, 415, 422, 429 or 500.

    Args:
        response (Response): The response returned by the API.

    Raises:
        AllianceNotFoundError: Raised, if an `Alliance` with the provided `alliance_id` was not found.\n
        CollectionNotDeletedError: Raised, if the requested `Collection` could not be deleted due to an internal server error.\n
        CollectionNotFoundError: Raised, if a `Collection` with the provided `collection_id` was not found.\n
        ConflictError: Raised, if a resource could not be created due to conflicting data.\n
        FromDateAfterToDateError: Raised, if the parameters `fromDate` and `toDate` have been specified and `fromDate` is greater than `toDate`.\n
        FromDateTooEarlyError: Raised, if the parameter `fromDate` is lower than the PSS start date.\n
        InvalidAllianceIdError: Raised, if the path parameter `alliance_id` received a value that can't be parsed to `int`.\n
        InvalidBoolError: Raised, if a parameter expecting a value of type `bool` received a value that can't be parsed to `bool`. Can also be part of a body parameter.\n
        InvalidCollectionIdError: Raised, if the path parameter `collection_id` received a value that can't be parsed to `int`.\n
        InvalidDateTimeError: Raised, if a parameter expecting a value of type `datetime` received a value that can't be parsed to `datetime`. Can also be part of a body parameter.\n
        InvalidDescError: Raised, if the query parameter `desc` received a value that can't be parsed to `bool`.\n
        InvalidFromDateError: Raised, if the query parameter `fromDate` received a value that can't be parsed to `datetime`.\n
        InvalidIntervalError: Raised, if the query parameter `interval` received a value that can't be parsed to `ParameterInterval`.\n
        InvalidJsonUpload: Raised, if the uploaded JSON file is invalid.\n
        InvalidNumberError: Raised, if a parameter expecting a value of type `int` or `float` received a value that can't be parsed to `int` or `float`. Can also be part of a body parameter.\n
        InvalidSkipError: Raised, if the query parameter `skip` received a value that can't be parsed to `int`.\n
        InvalidTakeError: Raised, if the query parameter `take` received a value that can't be parsed to `int`.\n
        InvalidToDateError: Raised, if the query parameter `toDate` received a value that can't be parsed to `datetime`.\n
        InvalidUserIdError: Raised, if the path parameter `user_id` received a value that can't be parsed to `int`.\n
        MethodNotAllowedError: Raised, if the request method is not allowed for the requested endpoint.\n
        MissingAccessError: Raised, if the client is not allowed to access the requested endpoint.\n
        NonUniqueCollectionIdError: Raised, if a `Collection` with its `collection_id` already exists in the database.\n
        NonUniqueTimestampError: Raised, if a `Collection` with its `timestamp` already exists in the database.\n
        NotAuthenticatedError: Raised, if the requested endpojnt requires authentication, but the client is not authenticated.\n
        NotFoundError: Raised, if a resource was not found.\n
        ParameterValidationError: Raised, if a body, path or query parameter or header received an invalid value.\n
        ParameterFormatError: Raised, if a body, path or query parameter or header received a value in a format that can't be parsed to the expected type.\n
        ParameterValueError: Raised, if a body, path or query parameter or header received an invalid value.\n
        ToDateTooEarlyError: Raised, if the parameter `toDate` is lower than the PSS start date.\n
        TooManyRequestsError: Raised, if the client is sending too many requests and is getting rate-limited.\n
        SchemaVersionMismatch: Raised, if the request contains a `Collection` in a schema that doesn't match the expected or specified `schema_version`.\n
        ServerError: Raised, if an internal server error occurs.\n
        UnsupportedMediaTypeError: Raised, if the requested endpoint received a body parameter of an unsupported media type.\n
        UnsupportedSchemaError: Raised, if the requested endpoint received a `Collection` of an unknown schema.\n
        UserNotFoundError: Raised, if a `User` with the provided `user_id` was not found.
    """
    if response.status_code not in (400, 401, 403, 404, 405, 409, 415, 422, 429, 500):
        return

    api_error = ApiErrorResponse(**response.json())
    exception = FromAPI.to_error(api_error)

    raise exception


__all__ = [
    PssFleetDataClient.__name__,
]
