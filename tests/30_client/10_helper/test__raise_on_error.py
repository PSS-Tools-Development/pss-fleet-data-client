import pytest
from httpx import Response

from pss_fleet_data import ApiError, ErrorCode
from pss_fleet_data.client import _raise_on_error
from pss_fleet_data.core.exceptions import *


RESPONSE_CONTENT_BASE = {
    "message": "message",
    "details": "details",
    "timestamp": "2024-04-15T00:59:00Z",
    "url": "https://example.com",
    "suggestion": "",
    "links": [],
}


test_cases_does_not_raise = [
    # status_code
    pytest.param(200, id="200"),
    pytest.param(201, id="201"),
    pytest.param(204, id="204"),
]
"""status_code"""


test_cases_raises = [
    # status_code, error_code, expected_exception
    pytest.param(404, ErrorCode.ALLIANCE_NOT_FOUND, AllianceNotFoundError, id="alliance_not_found"),
    pytest.param(500, ErrorCode.COLLECTION_NOT_DELETED, CollectionNotDeletedError, id="collection_not_deleted"),
    pytest.param(404, ErrorCode.COLLECTION_NOT_FOUND, CollectionNotFoundError, id="collection_not_found"),
    pytest.param(409, ErrorCode.CONFLICT, ConflictError, id="conflict"),
    pytest.param(403, ErrorCode.FORBIDDEN, MissingAccessError, id="forbidden"),
    pytest.param(422, ErrorCode.FROM_DATE_AFTER_TO_DATE, FromDateAfterToDateError, id="from_date_after_to_date"),
    pytest.param(422, ErrorCode.INVALID_BOOL, InvalidBoolError, id="invalid_bool"),
    pytest.param(422, ErrorCode.INVALID_DATETIME, InvalidDateTimeError, id="invalid_datetime"),
    pytest.param(422, ErrorCode.INVALID_JSON_FORMAT, InvalidJsonUpload, id="invalid_json_format"),
    pytest.param(422, ErrorCode.INVALID_NUMBER, InvalidNumberError, id="invalid_number"),
    pytest.param(422, ErrorCode.INVALID_PARAMETER, ParameterValidationError, id="invalid_parameter"),
    pytest.param(422, ErrorCode.INVALID_PARAMETER_FORMAT, ParameterFormatError, id="invalid_parameter_format"),
    pytest.param(422, ErrorCode.INVALID_PARAMETER_VALUE, ParameterValueError, id="invalid_parameter_value"),
    pytest.param(405, ErrorCode.METHOD_NOT_ALLOWED, MethodNotAllowedError, id="method_not_allowed"),
    pytest.param(409, ErrorCode.NON_UNIQUE_COLLECTION_ID, NonUniqueCollectionIdError, id="non_unique_collection_id"),
    pytest.param(409, ErrorCode.NON_UNIQUE_TIMESTAMP, NonUniqueTimestampError, id="non_unique_timestamp"),
    pytest.param(401, ErrorCode.NOT_AUTHENTICATED, NotAuthenticatedError, id="not_authenticated"),
    pytest.param(404, ErrorCode.NOT_FOUND, NotFoundError, id="not_found"),
    pytest.param(422, ErrorCode.PARAMETER_ALLIANCE_ID_INVALID, InvalidAllianceIdError, id="parameter_alliance_id_invalid"),
    pytest.param(422, ErrorCode.PARAMETER_COLLECTION_ID_INVALID, InvalidCollectionIdError, id="parameter_collection_id_invalid"),
    pytest.param(422, ErrorCode.PARAMETER_DESC_INVALID, InvalidDescError, id="parameter_desc_invalid"),
    pytest.param(422, ErrorCode.PARAMETER_FROM_DATE_INVALID, InvalidFromDateError, id="parameter_from_date_invalid"),
    pytest.param(422, ErrorCode.PARAMETER_FROM_DATE_TOO_EARLY, FromDateTooEarlyError, id="parameter_from_date_too_early"),
    pytest.param(422, ErrorCode.PARAMETER_INTERVAL_INVALID, InvalidIntervalError, id="parameter_interval_invalid"),
    pytest.param(422, ErrorCode.PARAMETER_SKIP_INVALID, InvalidSkipError, id="parameter_skip_invalid"),
    pytest.param(422, ErrorCode.PARAMETER_TAKE_INVALID, InvalidTakeError, id="parameter_take_invalid"),
    pytest.param(422, ErrorCode.PARAMETER_TO_DATE_INVALID, InvalidToDateError, id="parameter_to_date_invalid"),
    pytest.param(422, ErrorCode.PARAMETER_TO_DATE_TOO_EARLY, ToDateTooEarlyError, id="parameter_to_date_too_early"),
    pytest.param(422, ErrorCode.PARAMETER_USER_ID_INVALID, InvalidUserIdError, id="parameter_user_id_invalid"),
    pytest.param(429, ErrorCode.RATE_LIMITED, TooManyRequestsError, id="rate_limited"),
    pytest.param(422, ErrorCode.SCHEMA_VERSION_MISMATCH, SchemaVersionMismatch, id="schema_version_mismatch"),
    pytest.param(500, ErrorCode.SERVER_ERROR, ServerError, id="server_error"),
    pytest.param(415, ErrorCode.UNSUPPORTED_MEDIA_TYPE, UnsupportedMediaTypeError, id="unsupported_media_type"),
    pytest.param(422, ErrorCode.UNSUPPORTED_SCHEMA, UnsupportedSchemaError, id="unsupported_schema"),
    pytest.param(404, ErrorCode.USER_NOT_FOUND, UserNotFoundError, id="user_not_found"),
]
"""status_code, error_code, expected_exception"""


@pytest.mark.parametrize(["status_code"], test_cases_does_not_raise)
def test__raise_on_error_does_not_raise(status_code: int):
    response = Response(status_code)

    _raise_on_error(response)


@pytest.mark.parametrize(["status_code", "error_code", "expected_exception"], test_cases_raises)
def test__raise_on_error_raises(status_code: int, error_code: ErrorCode, expected_exception: ApiError):
    content = dict(RESPONSE_CONTENT_BASE)
    content["code"] = error_code
    response = Response(status_code, json=content)

    with pytest.raises(expected_exception):
        _raise_on_error(response)
