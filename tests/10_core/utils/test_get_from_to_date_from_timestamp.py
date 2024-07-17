from datetime import datetime, timezone

import pytest
import utils_test_cases
from dateutil.parser import parse as parse_datetime

from client.core.enums import ParameterInterval
from client.core.utils import get_from_to_date_from_timestamp


@pytest.mark.parametrize(["timestamp", "interval", "expected_from_date", "expected_to_date"], utils_test_cases.from_to_timestamps)
def test_get_from_to_date_from_timestamp(timestamp: datetime, interval: ParameterInterval, expected_from_date: datetime, expected_to_date: datetime):
    from_date, to_date = get_from_to_date_from_timestamp(timestamp, interval)
    assert from_date == expected_from_date
    assert to_date == expected_to_date


@pytest.mark.parametrize(["timestamp", "interval", "expected_exception"], utils_test_cases.from_to_timestamps_invalid)
def test_get_from_to_date_from_timestamp_invalid(timestamp: datetime, interval: ParameterInterval, expected_exception: Exception):
    with pytest.raises(expected_exception):
        _ = get_from_to_date_from_timestamp(timestamp, interval)
