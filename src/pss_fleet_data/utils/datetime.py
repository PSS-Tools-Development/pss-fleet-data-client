from datetime import datetime, timedelta, timezone
from typing import Optional, Union

import dateutil

from ..core.config import get_config
from ..models.enums import ParameterInterval


def add_timezone_utc(dt: Optional[datetime]) -> datetime:
    """Takes a `datetime` and makes it a timezone-aware `datetime` with timezone UTC, if it's not timezone-aware, yet.

    Args:
        dt (datetime): The `datetime` to be localized to the UTC timezone.

    Raises:
        ValueError: Raised, if parameter `dt` is not of type `datetime`.

    Returns:
        datetime: The timezone-aware `datetime` with the UTC timezone, if the provided `datetime` is not timezone-aware. The provided timezone-aware `datetime`, if it's not `None`. `None`, else.
    """
    if dt is None:
        return None

    if not isinstance(dt, datetime):
        raise TypeError("The parameter `dt` must be of type `datetime`!")

    if not dt.tzinfo:
        return dt.replace(tzinfo=timezone.utc)
    else:
        return dt


def convert_datetime_to_seconds(dt: Optional[datetime]) -> int:
    """Takes a `datetime` and converts it to seconds since the PSS start date.

    Args:
        dt (datetime): The `datetime` to be localized to the UTC timezone.

    Raises:
        TypeError: Raised, if parameter `dt` is not of type `datetime`.

    Returns:
        datetime: The seconds since the PSS start date. 0, if the provided `datetime` is before the PSS start date. `None`, else.
    """
    if dt is None:
        return None

    if not isinstance(dt, datetime):
        raise TypeError("The parameter `dt` must be of type `datetime`!")

    dt = localize_to_utc(dt)
    if dt < get_config().pss_start_date:
        return 0

    return int((dt - get_config().pss_start_date).total_seconds())


def format_datetime(dt: Optional[datetime], remove_tzinfo: bool = False) -> str:
    """Removes microseconds from a given `datetime` and returns an iso-formatted string of it.

    Args:
        dt (datetime, optional): The `datetime to be formatted. May be `None`.
        remove_tzinfo (bool, optional): Determines, whether to remove the timezone information from the given `datetime`. Defaults to False.

    Returns:
        str: The formatted datetime, including or excluding timezone information, if the provided `datetime` is not `None`. Else, `None`.
    """
    if not dt:
        return None

    if remove_tzinfo:
        dt = remove_timezone(dt)
    return dt.replace(microsecond=0).isoformat()


def get_most_recent_from_to_date_from_timestamp(timestamp: datetime, interval: ParameterInterval) -> tuple[datetime, datetime]:
    """Calculates most recent `datetime`s to be used as `fromDate` and `toDate` parameters given the specified `interval`.

    Args:
        timestamp (datetime): The timestamp to base the calculations on.
        interval (ParameterInterval): The interval to base the calculations on.

    Raises:
        ValueError: The parameter `interval` received an invalid value.

    Returns:
        tuple[datetime, datetime]: Two `datetime`s to be used as `fromDate` and `toDate` parameters. Localized to UTC timezone.
        The 1st `datetime` (for the `fromDate` parameter) depends on the provided `interval`:
        `HOURLY` will subtract 1 hour, `DAILY` will subtract 1 day and `MONTHLY` will subtract 1 month.
        The 2nd `datetime` (for the `toDate` parameter) is equal to the provided `timestamp`.
    """
    match interval:
        case ParameterInterval.HOURLY:
            from_date = timestamp - timedelta(hours=1)
        case ParameterInterval.DAILY:
            from_date = timestamp - timedelta(days=1)
        case ParameterInterval.MONTHLY:
            from_date = timestamp - dateutil.relativedelta.relativedelta(months=1)
        case _:
            raise ValueError(f"Parameter `interval` received in invalid value: {interval}")

    from_date = localize_to_utc(from_date)
    to_date = localize_to_utc(timestamp)

    return max(from_date, get_config().pss_start_date), max(to_date, get_config().pss_start_date)


def get_most_recent_timestamp(timestamp: datetime, interval: ParameterInterval) -> datetime:
    """Calculates the most recent timestamp matching the interval.

    Args:
        timestamp (datetime): The point in time for which to calculate the most recent timestamp.
        interval (ParameterInterval): The interval to base the calculations on.

    Raises:
        ValueError: The parameter `interval` received an invalid value or `None`.

    Returns:
        datetime: A timestamp localized to UTC. Depending on the `interval`:
        `MONTHLY` returns the most recent first of month.
        `DAILY` returns the most recent midnight.
        `HOURLY` returns the most recent hour.
    """
    result = localize_to_utc(timestamp).replace(minute=0, second=0, microsecond=0)

    match interval:
        case ParameterInterval.HOURLY:
            pass
        case ParameterInterval.DAILY:
            result = result.replace(hour=0)
        case ParameterInterval.MONTHLY:
            result = result.replace(hour=0, day=1)
        case _:
            raise ValueError(f"Parameter `interval` received in invalid value: {interval}")

    return result


def localize_to_utc(dt: Optional[datetime]) -> datetime:
    """Takes a `datetime` and converts it to a timezone-aware UTC `datetime`.

    Args:
        dt (datetime): The `datetime` to be localized to the UTC timezone.

    Raises:
        ValueError: Raised, if parameter `dt` is not of type `datetime`.

    Returns:
        datetime: The localized `datetime`, if `dt` is not `None`. `None`, else.
    """
    if dt is None:
        return None

    if not isinstance(dt, datetime):
        raise TypeError("The parameter `dt` must be of type `datetime`!")

    if not dt.tzinfo:
        return add_timezone_utc(dt)
    elif dt.tzinfo != timezone.utc:
        return dt.astimezone(timezone.utc)
    else:
        return dt


def parse_datetime(dt: Optional[Union[datetime, int, str]]) -> datetime:
    """Parses a `str` or `int` to `datetime` or returns the passed datetime.

    Args:
        dt (Union[datetime, int, str]): The `str` or `int` to be parsed. If it's an `int`, it represents the seconds since Jan 6th, 2016 12 am.

    Raises:
        ValueError: Raised, if parameter `dt` is not of type `datetime`, `int` or `str`.

    Returns:
        datetime: The parsed `datetime`, if `dt` is not `None`. `None`, else.
    """
    if dt is None:
        return None

    if not isinstance(dt, (datetime, int, str)) or isinstance(dt, bool):
        raise TypeError("The parameter `dt` must be of type `datetime`, `int` or `str`!")

    if isinstance(dt, int):
        # If it's an integer value, then it's likely encoded as seconds from Jan 6th, 2016 00:00 UTC
        return get_config().pss_start_date + timedelta(seconds=dt)
    elif isinstance(dt, str):
        return dateutil.parser.parse(dt)
    return dt


def remove_timezone(dt: Optional[datetime]) -> datetime:
    """Removes timezone information from a timezone-aware `datetime` object.

    Args:
        dt (datetime): The `datetime` to remove the timezone information from.

    Raises:
        TypeError: Raised, if parameter `dt` is not of type `datetime`.

    Returns:
        datetime: A timezone-naive `datetime` object.
    """
    if dt is None:
        return None

    if not isinstance(dt, datetime):
        raise TypeError("The parameter `dt` must be of type `datetime`!")

    return dt.replace(tzinfo=None)
