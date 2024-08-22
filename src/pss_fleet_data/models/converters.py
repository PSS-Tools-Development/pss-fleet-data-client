from typing import Optional

from httpx import Response
from pssapi.entities import Alliance as PssAlliance
from pssapi.entities import User as PssUser

from .. import utils
from ..core.exceptions import (
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
from .api_models import ApiAlliance, ApiAllianceHistory, ApiCollection, ApiCollectionMetadata, ApiErrorResponse, ApiUser, ApiUserHistory
from .client_models import AllianceHistory, Collection, CollectionMetadata, UserHistory
from .enums import ErrorCode


class FromAPI:
    """
    Offers functions to convert objects returned by the API to client objects or errors.
    """

    @staticmethod
    def to_pss_alliance(source: ApiAlliance) -> PssAlliance:
        """Converts an `Alliance` returned by the API to a `pssapi.entities.Alliance`.

        Args:
            source (ApiAlliance): An `Alliance` returned by the API.

        Returns:
            pss.entities.Alliance: The converted `Alliance`.
        """
        if source is None:
            return None

        return PssAlliance(
            {
                "AllianceId": source[0],
                "AllianceName": source[1],
                "Score": source[2],
                "DivisionDesignId": source[3],
                "Trophy": source[4],
                "ChampionshipScore": source[5],
                "NumberOfMembers": source[6],
                "NumberOfApprovedMembers": source[7],
            }
        )

    @staticmethod
    def to_alliance_history(source: ApiAllianceHistory) -> AllianceHistory:
        """Converts an `AllianceHistory` returned by the API to an `AllianceHistory`.

        Args:
            source (ApiAllianceHistory): An `AllianceHistory` returned by the API.

        Returns:
            AllianceHistory: The converted `AllianceHistory`.
        """
        return AllianceHistory(
            collection=FromAPI.to_collection_metadata(source.collection),
            alliance=FromAPI.to_pss_alliance(source.fleet),
            users=[FromAPI.to_pss_user(api_user) for api_user in source.users] if source.users else list(),
        )

    @staticmethod
    def to_collection(source: ApiCollection) -> Collection:
        """Converts a `Collection` returned by the API to a `Collection`.

        Args:
            source (ApiCollection): A `Collection` returned by the API.

        Returns:
            Collection: The converted `Collection`.
        """
        return Collection(
            metadata=FromAPI.to_collection_metadata(source.meta),
            alliances=[FromAPI.to_pss_alliance(api_alliance) for api_alliance in source.fleets] if source.fleets else list(),
            users=[FromAPI.to_pss_user(api_user) for api_user in source.users] if source.users else list(),
        )

    @staticmethod
    def to_collection_metadata(source: ApiCollectionMetadata) -> CollectionMetadata:
        """Converts a `CollectionMetadata` returned by the API to a `CollectionMetadata`.

        Args:
            source (ApiCollectionMetadata): A `CollectionMetadata` returned by the API.

        Returns:
            CollectionMetadata: The converted `CollectionMetadata`.
        """
        return CollectionMetadata(
            timestamp=source.timestamp,
            duration=source.duration,
            fleet_count=source.fleet_count,
            user_count=source.user_count,
            tournament_running=source.tourney_running,
            collection_id=source.collection_id,
            schema_version=source.schema_version,
            max_tournament_battle_attempts=source.max_tournament_battle_attempts,
            data_version=source.data_version,
        )

    @staticmethod
    def to_error(source: ApiErrorResponse) -> ApiError:
        """Converts an error response returned by the API to an `ApiError` to be raised.

        Args:
            source (ApiErrorResponse): An error response returned by the API.

        Returns:
            ApiError: The converted `ApiError`.
        """
        exception_class = _error_code_lookup.get(source.code, ApiError)
        result = exception_class(
            source.code,
            source.message,
            source.details,
            source.timestamp,
            source.suggestion,
            {link.path: link.description for link in source.links},
        )
        return result

    @staticmethod
    def to_pss_user(source: Optional[ApiUser]) -> PssUser:
        """Converts a `User` returned by the API to a `pssapi.entities.User`.

        Args:
            source (ApiUser, optional): A `User` returned by the API.

        Returns:
            pss.entities.User: The converted `User`.
        """
        if source is None:
            return None

        return PssUser(
            {
                "Id": source[0],
                "Name": source[1],
                "AllianceId": source[2],
                "Trophy": source[3],
                "AllianceScore": source[4],
                "AllianceMembership": utils.decode_alliance_membership(source[5]),
                "AllianceJoinDate": utils.format_datetime(utils.parse_datetime(source[6]), remove_tzinfo=True),
                "LastLoginDate": utils.format_datetime(utils.parse_datetime(source[7]), remove_tzinfo=True),
                "LastHeartBeatDate": utils.format_datetime(utils.parse_datetime(source[8]), remove_tzinfo=True),
                "CrewDonated": source[9],
                "CrewReceived": source[10],
                "PVPAttackWins": source[11],
                "PVPAttackLosses": source[12],
                "PVPAttackDraws": source[13],
                "PVPDefenceWins": source[14],
                "PVPDefenceLosses": source[15],
                "PVPDefenceDraws": source[16],
                "ChampionshipScore": source[17],
                "HighestTrophy": source[18],
                "TournamentBonusScore": source[19],
            }
        )

    @staticmethod
    def to_user_history(source: ApiUserHistory) -> UserHistory:
        """Converts a `UserHistory` returned by the API to a `UserHistory`.

        Args:
            source (ApiUserHistory): A `UserHistory` returned by the API.

        Returns:
            UserHistory: The converted `UserHistory`.
        """
        return UserHistory(
            collection=FromAPI.to_collection_metadata(source.collection),
            user=FromAPI.to_pss_user(source.user),
            alliance=FromAPI.to_pss_alliance(source.fleet) if source.fleet else None,
        )


class FromResponse:
    """
    Offers functions to convert httpx responses to client objects.
    """

    @staticmethod
    def to_alliance_history(source: Response) -> Optional[AllianceHistory]:
        """Converts a `httpx.Response` returned by the API to an `AllianceHistory`.

        Args:
            source (httpx.Response): The response returned by the API.

        Returns:
            Optional[AllianceHistory]: The converted `AllianceHistory` if the response has content, else `None`.
        """
        if not source.text:
            return None

        response_json = source.json()
        if not response_json:
            return None

        api_alliance_history = ApiAllianceHistory(**response_json)
        alliance_history = FromAPI.to_alliance_history(api_alliance_history)
        return alliance_history

    @staticmethod
    def to_alliance_history_list(source: Response) -> list[AllianceHistory]:
        """Converts a `httpx.Response` returned by the API to a list of `AllianceHistory` objects.

        Args:
            source (httpx.Response): The response returned by the API.

        Returns:
            list[AllianceHistory]: The converted list of `AllianceHistory` objects. The list may be empty.
        """
        if not source.text:
            return []

        response_json = source.json()
        if not response_json:
            return []

        alliance_history_list = [FromAPI.to_alliance_history(ApiAllianceHistory(**item)) for item in response_json]
        return alliance_history_list

    @staticmethod
    def to_collection(source: Response) -> Optional[Collection]:
        """Converts a `httpx.Response` returned by the API to a `Collection`.

        Args:
            source (httpx.Response): The response returned by the API.

        Returns:
            Optional[Collection]: The converted `Collection` if the response has content, else `None`.
        """
        if not source.text:
            return None

        response_json = source.json()
        if not response_json:
            return None

        api_collection = ApiCollection(**response_json)
        collection = FromAPI.to_collection(api_collection)
        return collection

    @staticmethod
    def to_collection_metadata(source: Response) -> Optional[CollectionMetadata]:
        """Converts a `httpx.Response` returned by the API to a `CollectionMetadata`.

        Args:
            source (httpx.Response): The response returned by the API.

        Returns:
            Optional[CollectionMetadata]: The converted `CollectionMetadata` if the response has content, else `None`.
        """
        if not source.text:
            return None

        response_json = source.json()
        if not response_json:
            return None

        api_collection_metadata = ApiCollectionMetadata(**response_json)
        collection_metadata = FromAPI.to_collection_metadata(api_collection_metadata)
        return collection_metadata

    @staticmethod
    def to_collection_metadata_list(source: Response) -> list[CollectionMetadata]:
        """Converts a `httpx.Response` returned by the API to a list of `CollectionMetadata` objects.

        Args:
            source (httpx.Response): The response returned by the API.

        Returns:
            list[CollectionMetadata]: The converted list of `CollectionMetadata` objects. The list may be empty.
        """
        if not source.text:
            return []

        response_json = source.json()
        if not response_json:
            return []

        collection_metadata_list = [FromAPI.to_collection_metadata(ApiCollectionMetadata(**item)) for item in response_json]
        return collection_metadata_list

    @staticmethod
    def to_user_history(source: Response) -> Optional[UserHistory]:
        """Converts a `httpx.Response` returned by the API to a `UserHistory`.

        Args:
            source (httpx.Response): The response returned by the API.

        Returns:
            Optional[UserHistory]: The converted `UserHistory` if the response has content, else `None`.
        """
        if not source.text:
            return None

        response_json = source.json()
        if not response_json:
            return None

        api_user_history = ApiUserHistory(**response_json)
        user_history = FromAPI.to_user_history(api_user_history)
        return user_history

    @staticmethod
    def to_user_history_list(source: Response) -> list[UserHistory]:
        """Converts a `httpx.Response` returned by the API to a list of `UserHistory` objects.

        Args:
            source (httpx.Response): The response returned by the API.

        Returns:
            list[UserHistory]: The converted list of `UserHistory` objects. The list may be empty.
        """
        if not source.text:
            return []

        response_json = source.json()
        if not response_json:
            return []

        user_history_list = [FromAPI.to_user_history(ApiUserHistory(**item)) for item in response_json]
        return user_history_list


class ToAPI:
    """
    Offers functions to convert client objects to objects consumed by the API.
    """

    @staticmethod
    def from_collection(source: Collection) -> ApiCollection:
        """Converts a `Collection` to a `Collection` to be sent to the API.

        Args:
            source (Collection): The `Collection` to be converted.

        Returns:
            ApiCollection: The converted `Collection`.
        """
        return ApiCollection(
            meta=ToAPI.from_collection_metadata(source.metadata),
            fleets=[ToAPI.from_pss_alliance(alliance) for alliance in source.alliances] if source.alliances else list(),
            users=[ToAPI.from_pss_user(users) for users in source.users] if source.users else list(),
        )

    @staticmethod
    def from_collection_metadata(source: CollectionMetadata) -> ApiCollectionMetadata:
        """Converts a `CollectionMetadata` to a `CollectionMetadata` to be sent to the API.

        Args:
            source (Collection): The `CollectionMetadata` to be converted.

        Returns:
            ApiCollectionMetadata: The converted `CollectionMetadata`.
        """
        return ApiCollectionMetadata(
            timestamp=source.timestamp,
            duration=source.duration,
            fleet_count=source.fleet_count,
            user_count=source.user_count,
            tourney_running=source.tournament_running,
            collection_id=None,
            schema_version=source.schema_version,
            max_tournament_battle_attempts=source.max_tournament_battle_attempts,
            data_version=source.data_version,
        )

    @staticmethod
    def from_pss_alliance(source: PssAlliance) -> ApiAlliance:
        """Converts an `Alliance` from the PSS API to an `Alliance` to be sent to the API.

        Args:
            source (pssapi.entities.Alliance): The `Alliance` to be converted.

        Returns:
            ApiAlliance: The converted `Alliance`.
        """
        return (
            source.alliance_id,
            source.alliance_name,
            source.score,
            source.division_design_id,
            source.trophy,
            source.championship_score,
            source.number_of_members,
            source.number_of_approved_members,
        )

    @staticmethod
    def from_pss_user(source: PssUser) -> ApiUser:
        """Converts a `User` from the PSS API to an `User` to be sent to the API.

        Args:
            source (pssapi.entities.User): The `User` to be converted.

        Returns:
            ApiUser: The converted `User`.
        """
        return (
            source.id,
            source.name,
            source.alliance_id,
            source.trophy,
            source.alliance_score,
            utils.encode_alliance_membership(source.alliance_membership),
            utils.convert_datetime_to_seconds(source.alliance_join_date),
            utils.convert_datetime_to_seconds(source.last_login_date),
            utils.convert_datetime_to_seconds(source.last_heart_beat_date),
            source.crew_donated,
            source.crew_received,
            source.pvp_attack_wins,
            source.pvp_attack_losses,
            source.pvp_attack_draws,
            source.pvp_defence_wins,
            source.pvp_defence_losses,
            source.pvp_defence_draws,
            source.championship_score,
            source.highest_trophy,
            source.tournament_bonus_score,
        )


_error_code_lookup = {
    ErrorCode.ALLIANCE_NOT_FOUND: AllianceNotFoundError,
    ErrorCode.COLLECTION_NOT_DELETED: CollectionNotDeletedError,
    ErrorCode.COLLECTION_NOT_FOUND: CollectionNotFoundError,
    ErrorCode.CONFLICT: ConflictError,
    ErrorCode.FORBIDDEN: MissingAccessError,
    ErrorCode.FROM_DATE_AFTER_TO_DATE: FromDateAfterToDateError,
    ErrorCode.INVALID_BOOL: InvalidBoolError,
    ErrorCode.INVALID_DATETIME: InvalidDateTimeError,
    ErrorCode.INVALID_JSON_FORMAT: InvalidJsonUpload,
    ErrorCode.INVALID_NUMBER: InvalidNumberError,
    ErrorCode.INVALID_PARAMETER: ParameterValidationError,
    ErrorCode.INVALID_PARAMETER_FORMAT: ParameterFormatError,
    ErrorCode.INVALID_PARAMETER_VALUE: ParameterValueError,
    ErrorCode.METHOD_NOT_ALLOWED: MethodNotAllowedError,
    ErrorCode.NON_UNIQUE_COLLECTION_ID: NonUniqueCollectionIdError,
    ErrorCode.NON_UNIQUE_TIMESTAMP: NonUniqueTimestampError,
    ErrorCode.NOT_AUTHENTICATED: NotAuthenticatedError,
    ErrorCode.NOT_FOUND: NotFoundError,
    ErrorCode.PARAMETER_ALLIANCE_ID_INVALID: InvalidAllianceIdError,
    ErrorCode.PARAMETER_COLLECTION_ID_INVALID: InvalidCollectionIdError,
    ErrorCode.PARAMETER_DESC_INVALID: InvalidDescError,
    ErrorCode.PARAMETER_FROM_DATE_INVALID: InvalidFromDateError,
    ErrorCode.PARAMETER_FROM_DATE_TOO_EARLY: FromDateTooEarlyError,
    ErrorCode.PARAMETER_INTERVAL_INVALID: InvalidIntervalError,
    ErrorCode.PARAMETER_SKIP_INVALID: InvalidSkipError,
    ErrorCode.PARAMETER_TAKE_INVALID: InvalidTakeError,
    ErrorCode.PARAMETER_TO_DATE_INVALID: InvalidToDateError,
    ErrorCode.PARAMETER_TO_DATE_TOO_EARLY: ToDateTooEarlyError,
    ErrorCode.PARAMETER_USER_ID_INVALID: InvalidUserIdError,
    ErrorCode.RATE_LIMITED: TooManyRequestsError,
    ErrorCode.SCHEMA_VERSION_MISMATCH: SchemaVersionMismatch,
    ErrorCode.SERVER_ERROR: ServerError,
    ErrorCode.UNSUPPORTED_MEDIA_TYPE: UnsupportedMediaTypeError,
    ErrorCode.UNSUPPORTED_SCHEMA: UnsupportedSchemaError,
    ErrorCode.USER_NOT_FOUND: UserNotFoundError,
}
"""A lookup from an API `ErrorCode` to a specific `Exception` type."""
