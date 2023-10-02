import calendar as _calendar
import datetime as _datetime
from typing import Dict as _Dict


# ---------- Constants ----------
API_DATETIME_FORMAT_ISO: str = '%Y-%m-%dT%H:%M:%S'

MONTH_NAME_TO_NUMBER: _Dict[str, int] = {v.lower(): k for k, v in enumerate(_calendar.month_name) if k > 0}
MONTH_SHORT_NAME_TO_NUMBER: _Dict[str, int] = {v.lower(): k for k, v in enumerate(_calendar.month_abbr) if k > 0}

ONE_DAY: _datetime.timedelta = _datetime.timedelta(days=1)

PSS_START_DATETIME: _datetime.datetime = _datetime.datetime(year=2016, month=1, day=6)


# ---------- Functions ----------

def get_utc_now() -> _datetime.datetime:
    return _datetime.datetime.now(_datetime.timezone.utc)


def format_pss_datetime(dt: _datetime.datetime) -> str:
    result = dt.strftime(API_DATETIME_FORMAT_ISO)
    return result


def parse_formatted_datetime(date_time: str, include_time: bool = True, include_tz: bool = True, include_tz_brackets: bool = True) -> _datetime.datetime:
    format_string = '%Y-%m-%d'
    if include_time:
        format_string += ' %H:%M:%S'
    if include_tz:
        if include_tz_brackets:
            format_string += ' (%Z)'
        else:
            format_string += ' %Z'
    result = _datetime.datetime.strptime(date_time, format_string)
    if result.tzinfo is None:
        result = result.replace(tzinfo=_datetime.timezone.utc)
    return result