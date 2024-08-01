from datetime import datetime, timezone

import pytest

from pss_fleet_data.models.enums import ParameterInterval
from pss_fleet_data.utils import get_most_recent_timestamp


test_cases_invalid = [
    # timestamp, interval, expected_exception
    pytest.param(datetime(2024, 4, 15), None, ValueError, id="interval_none"),
    pytest.param(datetime(2024, 4, 15), "monthly", ValueError, id="interval_invalid"),
]
"""timestamp, interval, expected_exception"""


test_cases_valid = [
    # timestamp, interval, expected_result
    # MONTHLY
    pytest.param(datetime(2024, 4, 15), ParameterInterval.MONTHLY, datetime(2024, 4, 1, tzinfo=timezone.utc), id="monthly"),
    pytest.param(datetime(2024, 4, 15), "month", datetime(2024, 4, 1, tzinfo=timezone.utc), id="monthly_interval_as_str"),
    pytest.param(datetime(2024, 4, 1), ParameterInterval.MONTHLY, datetime(2024, 4, 1, tzinfo=timezone.utc), id="monthly_no_change"),
    pytest.param(datetime(2024, 4, 15, tzinfo=timezone.utc), ParameterInterval.MONTHLY, datetime(2024, 4, 1, tzinfo=timezone.utc), id="monthly_utc"),
    pytest.param(
        datetime(2024, 4, 1, tzinfo=timezone.utc), ParameterInterval.MONTHLY, datetime(2024, 4, 1, tzinfo=timezone.utc), id="monthly_utc_no_change"
    ),
    pytest.param(datetime(2024, 4, 15, 18, 3, 42, 333), ParameterInterval.MONTHLY, datetime(2024, 4, 1, tzinfo=timezone.utc), id="monthly_detailed"),
    # DAILY
    pytest.param(datetime(2024, 4, 15, 18), ParameterInterval.DAILY, datetime(2024, 4, 15, tzinfo=timezone.utc), id="daily"),
    pytest.param(datetime(2024, 4, 15, 18), "day", datetime(2024, 4, 15, tzinfo=timezone.utc), id="daily_interval_as_str"),
    pytest.param(datetime(2024, 4, 15), ParameterInterval.DAILY, datetime(2024, 4, 15, tzinfo=timezone.utc), id="daily_no_change"),
    pytest.param(datetime(2024, 4, 15, 18, tzinfo=timezone.utc), ParameterInterval.DAILY, datetime(2024, 4, 15, tzinfo=timezone.utc), id="daily_utc"),
    pytest.param(
        datetime(2024, 4, 15, tzinfo=timezone.utc), ParameterInterval.DAILY, datetime(2024, 4, 15, tzinfo=timezone.utc), id="daily_utc_no_change"
    ),
    pytest.param(datetime(2024, 4, 15, 18, 3, 42, 333), ParameterInterval.DAILY, datetime(2024, 4, 15, tzinfo=timezone.utc), id="daily_detailed"),
    # HOURLY
    pytest.param(datetime(2024, 4, 15, 18, 5), ParameterInterval.HOURLY, datetime(2024, 4, 15, 18, tzinfo=timezone.utc), id="hourly"),
    pytest.param(datetime(2024, 4, 15, 18, 5), "hour", datetime(2024, 4, 15, 18, tzinfo=timezone.utc), id="hourly_interval_as_str"),
    pytest.param(datetime(2024, 4, 15, 18), ParameterInterval.HOURLY, datetime(2024, 4, 15, 18, tzinfo=timezone.utc), id="hourly_no_change"),
    pytest.param(
        datetime(2024, 4, 15, 18, 5, tzinfo=timezone.utc), ParameterInterval.HOURLY, datetime(2024, 4, 15, 18, tzinfo=timezone.utc), id="hourly_utc"
    ),
    pytest.param(
        datetime(2024, 4, 15, 18, tzinfo=timezone.utc),
        ParameterInterval.HOURLY,
        datetime(2024, 4, 15, 18, tzinfo=timezone.utc),
        id="hourly_utc_no_change",
    ),
    pytest.param(
        datetime(2024, 4, 15, 18, 3, 42, 333), ParameterInterval.HOURLY, datetime(2024, 4, 15, 18, tzinfo=timezone.utc), id="hourly_detailed"
    ),
]
"""timestamp, interval, expected_result"""


@pytest.mark.parametrize(["timestamp", "interval", "expected_exception"], test_cases_invalid)
def test_get_most_recent_timestamp_invalid(timestamp: datetime, interval: ParameterInterval, expected_exception: Exception):
    with pytest.raises(expected_exception):
        _ = get_most_recent_timestamp(timestamp, interval)


@pytest.mark.parametrize(["timestamp", "interval", "expected_result"], test_cases_valid)
def test_get_most_recent_timestamp_valid(timestamp: datetime, interval: ParameterInterval, expected_result: datetime):
    result = get_most_recent_timestamp(timestamp, interval)
    assert result == expected_result
