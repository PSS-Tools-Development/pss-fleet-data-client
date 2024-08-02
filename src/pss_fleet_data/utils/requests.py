from datetime import datetime
from typing import Any, MutableMapping, Optional

from ..models.enums import ParameterInterval


def create_parameter_dict(
    *,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    interval: Optional[ParameterInterval] = None,
    desc: Optional[bool] = None,
    skip: Optional[int] = None,
    take: Optional[int] = None,
) -> dict[str, Any]:
    """Creates a dictionary of query parameters.

    Args:
        from_date (datetime, optional): The earliest date for which to return results. Defaults to None.
        to_date (datetime, optional): The latest date for which to return results. Defaults to None.
        interval (ParameterInterval, optional): The interval of the data to return, either hourly, end of day or end of month. Defaults to None.
        desc (bool, optional): Determines, if the results should be returned in descending order. Defaults to None.
        skip (int, optional): The number of results to skip in the response. Defaults to None.
        take (int, optional): The number of results to be returned. Defaults to None.

    Returns:
        dict[str, Any]: A dictionary of query parameters. Only includes the specified parameters.
    """
    parameters = {}
    if from_date:
        parameters["fromDate"] = from_date
    if to_date:
        parameters["toDate"] = to_date
    if interval:
        parameters["interval"] = interval
    if desc is not None:
        parameters["desc"] = desc
    if skip is not None:
        parameters["skip"] = skip
    if take is not None:
        parameters["take"] = take
    return parameters


def merge_headers(client_headers: MutableMapping[str, str], headers: MutableMapping[str, str]) -> dict[str, str]:
    """Merges header dicts, overwriting keys existing in the `client_headers`, if those are also defined in `headers`.

    Args:
        client_headers (MutableMapping[str, str]): The default headers of an `AsyncClient`.
        headers (MutableMapping[str, str]): The additional headers to add or to overwrite default headers with.

    Returns:
        dict[str, str]: A new dictionary representing the headers to be sent with a `Request`.
    """
    request_headers = dict(client_headers or {})
    request_headers.update(headers or {})

    return request_headers
