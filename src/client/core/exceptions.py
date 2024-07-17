from dataclasses import dataclass


# Base Exception


@dataclass()
class ApiError(Exception):
    """
    The base exception to be thrown, when an error is returned by the API.
    """

    code: str
    message: str
    details: str
    timestamp: str
    suggestion: str
    links: dict[str, str]  # Url: description

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        message = f"The API raised {self.code} at {self.timestamp}: {self.message}\n\t{self.details}\n\tSuggestion: {self.suggestion}"
        if self.links:
            message += "\n\tSee also:\n\t- " + "\n\t- ".join(f"{description}: {url}" for url, description in self.links.items())
        return message


# HTTP 401


class NotAuthenticatedError(ApiError):
    pass


# HTTP 403


class MissingAccessError(ApiError):
    pass


# HTTP 404


class NotFoundError(ApiError):
    pass


class AllianceNotFoundError(NotFoundError):
    pass


class CollectionNotFoundError(NotFoundError):
    pass


class UserNotFoundError(NotFoundError):
    pass


# HTTP 405


class MethodNotAllowedError(ApiError):
    pass


# HTTP 409


class ConflictError(ApiError):
    pass


class NonUniqueTimestampError(ConflictError):
    pass


class NonUniqueCollectionIdError(ConflictError):
    pass


# HTTP 415


class UnsupportedMediaTypeError(ApiError):
    pass


# HTTP 422


class ParameterValidationError(ApiError):
    pass


# Parameter Format


class ParameterFormatError(ParameterValidationError):
    pass


class InvalidBoolError(ParameterFormatError):
    pass


class InvalidDateTimeError(ParameterFormatError):
    pass


class InvalidJsonUpload(ParameterFormatError):
    pass


class InvalidNumberError(ParameterFormatError):
    pass


class UnsupportedSchemaError(ParameterFormatError):
    pass


class SchemaVersionMismatch(UnsupportedSchemaError):
    pass


# Parameter Value


class ParameterValueError(ParameterValidationError):
    pass


class FromDateAfterToDateError(ParameterValueError):
    pass


class InvalidAllianceIdError(ParameterValueError):
    pass


class InvalidCollectionIdError(ParameterValueError):
    pass


class InvalidDescError(ParameterValueError):
    pass


class InvalidFromDateError(ParameterValueError):
    pass


class FromDateTooEarlyError(InvalidFromDateError):
    pass


class InvalidToDateError(ParameterValueError):
    pass


class ToDateTooEarlyError(InvalidToDateError):
    pass


class InvalidIntervalError(ParameterValueError):
    pass


class InvalidSkipError(ParameterValueError):
    pass


class InvalidTakeError(ParameterValueError):
    pass


class InvalidUserIdError(ParameterValueError):
    pass


# HTTP 429


class TooManyRequestsError(ApiError):  # 429
    pass


# HTTP 500


class ServerError(ApiError):  # 500
    pass


class CollectionNotDeletedError(ServerError):
    pass


__all__ = [
    AllianceNotFoundError.__name__,
    ApiError.__name__,
    CollectionNotDeletedError.__name__,
    CollectionNotFoundError.__name__,
    ConflictError.__name__,
    FromDateAfterToDateError.__name__,
    FromDateTooEarlyError.__name__,
    InvalidAllianceIdError.__name__,
    InvalidBoolError.__name__,
    InvalidCollectionIdError.__name__,
    InvalidDateTimeError.__name__,
    InvalidDescError.__name__,
    InvalidFromDateError.__name__,
    InvalidIntervalError.__name__,
    InvalidJsonUpload.__name__,
    InvalidNumberError.__name__,
    InvalidSkipError.__name__,
    InvalidTakeError.__name__,
    InvalidToDateError.__name__,
    InvalidUserIdError.__name__,
    MethodNotAllowedError.__name__,
    MissingAccessError.__name__,
    NonUniqueCollectionIdError.__name__,
    NonUniqueTimestampError.__name__,
    NotAuthenticatedError.__name__,
    NotFoundError.__name__,
    ParameterFormatError.__name__,
    ParameterValidationError.__name__,
    ParameterValueError.__name__,
    SchemaVersionMismatch.__name__,
    ServerError.__name__,
    ToDateTooEarlyError.__name__,
    TooManyRequestsError.__name__,
    UnsupportedMediaTypeError.__name__,
    UnsupportedSchemaError.__name__,
    UserNotFoundError.__name__,
]
