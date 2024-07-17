from datetime import datetime, timezone


utc = timezone.utc

import pytest

from client.core.enums import ParameterInterval


from_to_timestamps = [
    # timestamp, interval, expected_from_date, expected_to_date
    pytest.param(datetime(2017, 1, 6), ParameterInterval.HOURLY, datetime(2017, 1, 5, 23, tzinfo=utc), datetime(2017, 1, 6, tzinfo=utc), id="hourly"),
    pytest.param(datetime(2017, 1, 6), ParameterInterval.DAILY, datetime(2017, 1, 5, tzinfo=utc), datetime(2017, 1, 6, tzinfo=utc), id="daily"),
    pytest.param(datetime(2017, 1, 6), ParameterInterval.MONTHLY, datetime(2016, 12, 6, tzinfo=utc), datetime(2017, 1, 6, tzinfo=utc), id="monthly"),
    # first of year
    pytest.param(
        datetime(2017, 1, 1),
        ParameterInterval.HOURLY,
        datetime(2016, 12, 31, 23, tzinfo=utc),
        datetime(2017, 1, 1, tzinfo=utc),
        id="hourly_on_first_of_year",
    ),
    pytest.param(
        datetime(2017, 1, 1),
        ParameterInterval.DAILY,
        datetime(2016, 12, 31, tzinfo=utc),
        datetime(2017, 1, 1, tzinfo=utc),
        id="daily_on_first_of_year",
    ),
    pytest.param(
        datetime(2017, 1, 1),
        ParameterInterval.MONTHLY,
        datetime(2016, 12, 1, tzinfo=utc),
        datetime(2017, 1, 1, tzinfo=utc),
        id="monthly_on_first_of_year",
    ),
    # first of month
    pytest.param(
        datetime(2017, 7, 1),
        ParameterInterval.HOURLY,
        datetime(2017, 6, 30, 23, tzinfo=utc),
        datetime(2017, 7, 1, tzinfo=utc),
        id="hourly_on_first_of_month",
    ),
    pytest.param(
        datetime(2017, 7, 1),
        ParameterInterval.DAILY,
        datetime(2017, 6, 30, tzinfo=utc),
        datetime(2017, 7, 1, tzinfo=utc),
        id="daily_on_first_of_month",
    ),
    pytest.param(
        datetime(2017, 7, 1),
        ParameterInterval.MONTHLY,
        datetime(2017, 6, 1, tzinfo=utc),
        datetime(2017, 7, 1, tzinfo=utc),
        id="monthly_on_first_of_month",
    ),
    # with hours
    pytest.param(
        datetime(2017, 1, 6, 12),
        ParameterInterval.HOURLY,
        datetime(2017, 1, 6, 11, tzinfo=utc),
        datetime(2017, 1, 6, 12, tzinfo=utc),
        id="hourly_with_hours",
    ),
    pytest.param(
        datetime(2017, 1, 6, 12),
        ParameterInterval.DAILY,
        datetime(2017, 1, 5, 12, tzinfo=utc),
        datetime(2017, 1, 6, 12, tzinfo=utc),
        id="daily_with_hours",
    ),
    pytest.param(
        datetime(2017, 1, 6, 12),
        ParameterInterval.MONTHLY,
        datetime(2016, 12, 6, 12, tzinfo=utc),
        datetime(2017, 1, 6, 12, tzinfo=utc),
        id="monthly_with_hours",
    ),
    # with minutes
    pytest.param(
        datetime(2017, 1, 6),
        ParameterInterval.HOURLY,
        datetime(2017, 1, 5, 23, tzinfo=utc),
        datetime(2017, 1, 6, tzinfo=utc),
        id="hourly_with_minutes",
    ),
    pytest.param(
        datetime(2017, 1, 6), ParameterInterval.DAILY, datetime(2017, 1, 5, tzinfo=utc), datetime(2017, 1, 6, tzinfo=utc), id="daily_with_minutes"
    ),
    pytest.param(
        datetime(2017, 1, 6),
        ParameterInterval.MONTHLY,
        datetime(2016, 12, 6, tzinfo=utc),
        datetime(2017, 1, 6, tzinfo=utc),
        id="monthly_with_minutes",
    ),
    # with seconds
    pytest.param(
        datetime(2017, 1, 6),
        ParameterInterval.HOURLY,
        datetime(2017, 1, 5, 23, tzinfo=utc),
        datetime(2017, 1, 6, tzinfo=utc),
        id="hourly_with_seconds",
    ),
    pytest.param(
        datetime(2017, 1, 6), ParameterInterval.DAILY, datetime(2017, 1, 5, tzinfo=utc), datetime(2017, 1, 6, tzinfo=utc), id="daily_with_seconds"
    ),
    pytest.param(
        datetime(2017, 1, 6),
        ParameterInterval.MONTHLY,
        datetime(2016, 12, 6, tzinfo=utc),
        datetime(2017, 1, 6, tzinfo=utc),
        id="monthly_with_seconds",
    ),
    # with tzinfo
    pytest.param(
        datetime(2017, 1, 6, tzinfo=utc),
        ParameterInterval.HOURLY,
        datetime(2017, 1, 5, 23, tzinfo=utc),
        datetime(2017, 1, 6, tzinfo=utc),
        id="hourly_with_tzinfo",
    ),
    pytest.param(
        datetime(2017, 1, 6, tzinfo=utc),
        ParameterInterval.DAILY,
        datetime(2017, 1, 5, tzinfo=utc),
        datetime(2017, 1, 6, tzinfo=utc),
        id="daily_with_tzinfo",
    ),
    pytest.param(
        datetime(2017, 1, 6, tzinfo=utc),
        ParameterInterval.MONTHLY,
        datetime(2016, 12, 6, tzinfo=utc),
        datetime(2017, 1, 6, tzinfo=utc),
        id="monthly_with_tzinfo",
    ),
    # mixed with hours, minutes, seconds
    pytest.param(
        datetime(2017, 1, 6, 3, 12, 56),
        ParameterInterval.HOURLY,
        datetime(2017, 1, 6, 2, 12, 56, tzinfo=utc),
        datetime(2017, 1, 6, 3, 12, 56, tzinfo=utc),
        id="hourly_mixed",
    ),
    pytest.param(
        datetime(2017, 1, 6, 8, 0, 12),
        ParameterInterval.DAILY,
        datetime(2017, 1, 5, 8, 0, 12, tzinfo=utc),
        datetime(2017, 1, 6, 8, 0, 12, tzinfo=utc),
        id="daily_mixed",
    ),
    pytest.param(
        datetime(2017, 1, 6, 0, 0, 59),
        ParameterInterval.MONTHLY,
        datetime(2016, 12, 6, 0, 0, 59, tzinfo=utc),
        datetime(2017, 1, 6, 0, 0, 59, tzinfo=utc),
        id="monthly_mixed",
    ),
    # result from_date before PSS start date
    pytest.param(
        datetime(2016, 1, 6),
        ParameterInterval.HOURLY,
        datetime(2016, 1, 6, tzinfo=utc),
        datetime(2016, 1, 6, tzinfo=utc),
        id="hourly_from_date_before_pss_start_date_1",
    ),
    pytest.param(
        datetime(2016, 1, 6, 0, 23),
        ParameterInterval.HOURLY,
        datetime(2016, 1, 6, tzinfo=utc),
        datetime(2016, 1, 6, 0, 23, tzinfo=utc),
        id="hourly_from_date_before_pss_start_date_2",
    ),
    pytest.param(
        datetime(2016, 1, 6),
        ParameterInterval.DAILY,
        datetime(2016, 1, 6, tzinfo=utc),
        datetime(2016, 1, 6, tzinfo=utc),
        id="daily_from_date_before_pss_start_date_1",
    ),
    pytest.param(
        datetime(2016, 1, 6, 0, 23),
        ParameterInterval.DAILY,
        datetime(2016, 1, 6, tzinfo=utc),
        datetime(2016, 1, 6, 0, 23, tzinfo=utc),
        id="daily_from_date_before_pss_start_date_2",
    ),
    pytest.param(
        datetime(2016, 1, 6, 23, 0),
        ParameterInterval.DAILY,
        datetime(2016, 1, 6, tzinfo=utc),
        datetime(2016, 1, 6, 23, 0, tzinfo=utc),
        id="daily_from_date_before_pss_start_date_3",
    ),
    pytest.param(
        datetime(2016, 1, 6),
        ParameterInterval.MONTHLY,
        datetime(2016, 1, 6, tzinfo=utc),
        datetime(2016, 1, 6, tzinfo=utc),
        id="monthly_from_date_before_pss_start_date_1",
    ),
    pytest.param(
        datetime(2016, 1, 6, 0, 23),
        ParameterInterval.MONTHLY,
        datetime(2016, 1, 6, tzinfo=utc),
        datetime(2016, 1, 6, 0, 23, tzinfo=utc),
        id="monthly_from_date_before_pss_start_date_2",
    ),
    pytest.param(
        datetime(2016, 1, 6, 23, 0),
        ParameterInterval.MONTHLY,
        datetime(2016, 1, 6, tzinfo=utc),
        datetime(2016, 1, 6, 23, 0, tzinfo=utc),
        id="monthly_from_date_before_pss_start_date_3",
    ),
    pytest.param(
        datetime(2016, 2, 5),
        ParameterInterval.MONTHLY,
        datetime(2016, 1, 6, tzinfo=utc),
        datetime(2016, 2, 5, tzinfo=utc),
        id="monthly_from_date_before_pss_start_date_4",
    ),
    # parameter timestamp before PSS start date
    pytest.param(
        datetime(2016, 1, 1),
        ParameterInterval.HOURLY,
        datetime(2016, 1, 6, tzinfo=utc),
        datetime(2016, 1, 6, tzinfo=utc),
        id="hourly_timestamp_before_pss_start_date",
    ),
    pytest.param(
        datetime(2016, 1, 1),
        ParameterInterval.DAILY,
        datetime(2016, 1, 6, tzinfo=utc),
        datetime(2016, 1, 6, tzinfo=utc),
        id="daily_timestamp_before_pss_start_date",
    ),
    pytest.param(
        datetime(2016, 1, 1),
        ParameterInterval.MONTHLY,
        datetime(2016, 1, 6, tzinfo=utc),
        datetime(2016, 1, 6, tzinfo=utc),
        id="monthly_timestamp_before_pss_start_date",
    ),
]
"""timestamp, interval, expected_from_date, expected_to_date"""


from_to_timestamps_invalid = [
    # timestamp, interval, expected_error
    pytest.param(None, ParameterInterval.HOURLY, TypeError, id="timestamp_none_interval_hourly"),
    pytest.param(None, ParameterInterval.DAILY, TypeError, id="timestamp_none_interval_daily"),
    pytest.param(None, ParameterInterval.MONTHLY, TypeError, id="timestamp_none_interval_monthly"),
    pytest.param(datetime(2016, 1, 6), None, ValueError, id="timestamp_valid_interval_none"),
    pytest.param(datetime(2016, 1, 6), "invalid", ValueError, id="timestamp_valid_interval_is_str"),
    pytest.param(datetime(2016, 1, 6), "", ValueError, id="timestamp_valid_interval_empty_str"),
    pytest.param(datetime(2016, 1, 6), 1, ValueError, id="timestamp_valid_interval_is_int"),
    pytest.param("blah", ParameterInterval.HOURLY, TypeError, id="timestamp_is_str_interval_hourly"),
    pytest.param("blah", ParameterInterval.DAILY, TypeError, id="timestamp_is_str_interval_daily"),
    pytest.param("blah", ParameterInterval.MONTHLY, TypeError, id="timestamp_is_str_interval_monthly"),
    pytest.param("", ParameterInterval.HOURLY, TypeError, id="timestamp_empty_str_interval_hourly"),
    pytest.param("", ParameterInterval.DAILY, TypeError, id="timestamp_empty_str_interval_daily"),
    pytest.param("", ParameterInterval.MONTHLY, TypeError, id="timestamp_empty_str_interval_monthly"),
    pytest.param(1, ParameterInterval.HOURLY, TypeError, id="timestamp_is_int_interval_hourly"),
    pytest.param(1, ParameterInterval.DAILY, TypeError, id="timestamp_is_int_interval_daily"),
    pytest.param(1, ParameterInterval.MONTHLY, TypeError, id="timestamp_is_int_interval_monthly"),
]


parameter_dicts = [
    # input, expected_output
    pytest.param(None, {}, id="none"),
    pytest.param({}, {}, id="empty"),
    pytest.param({"from_date": None}, {}, id="fromDate_none"),
    pytest.param({"from_date": "blah"}, {"fromDate": "blah"}, id="fromDate_is_str"),
    pytest.param({"from_date": ""}, {}, id="fromDate_empty_str"),
    pytest.param({"from_date": datetime(2016, 1, 6)}, {"fromDate": datetime(2016, 1, 6)}, id="fromDate_without_tzinfo"),
    pytest.param(
        {"from_date": datetime(2016, 1, 6, tzinfo=utc)},
        {"fromDate": datetime(2016, 1, 6, tzinfo=utc)},
        id="fromDate_with_tzinfo",
    ),
    pytest.param({"to_date": None}, {}, id="toDate_none"),
    pytest.param({"to_date": "blah"}, {"toDate": "blah"}, id="toDate_is_str"),
    pytest.param({"to_date": ""}, {}, id="toDate_empty_str"),
    pytest.param({"to_date": datetime(2016, 12, 31)}, {"toDate": datetime(2016, 12, 31)}, id="toDate_without_tzinfo"),
    pytest.param(
        {"to_date": datetime(2016, 1, 6, tzinfo=utc)},
        {"toDate": datetime(2016, 1, 6, tzinfo=utc)},
        id="toDate_with_tzinfo",
    ),
    pytest.param(
        {"from_date": datetime(2016, 1, 6), "to_date": datetime(2016, 12, 31)},
        {"fromDate": datetime(2016, 1, 6), "toDate": datetime(2016, 12, 31)},
        id="fromDate_toDate",
    ),
    pytest.param({"interval": None}, {}, id="interval_none"),
    pytest.param({"interval": ParameterInterval.MONTHLY}, {"interval": ParameterInterval.MONTHLY}, id="interval_month"),
    pytest.param({"interval": "month"}, {"interval": "month"}, id="interval_is_str"),
    pytest.param({"interval": ""}, {}, id="interval_empty_str"),
    pytest.param({"desc": None}, {}, id="desc_none"),
    pytest.param({"desc": True}, {"desc": True}, id="desc_true"),
    pytest.param({"desc": False}, {"desc": False}, id="desc_false"),
    pytest.param({"desc": "True"}, {"desc": "True"}, id="desc_is_str"),
    pytest.param({"desc": ""}, {"desc": ""}, id="desc_empty_str"),
    pytest.param({"skip": None}, {}, id="skip_none"),
    pytest.param({"skip": -1}, {"skip": -1}, id="skip_negative"),
    pytest.param({"skip": 0}, {"skip": 0}, id="skip_0"),
    pytest.param({"skip": 100}, {"skip": 100}, id="skip_100"),
    pytest.param({"skip": "1"}, {"skip": "1"}, id="skip_is_str"),
    pytest.param({"skip": ""}, {"skip": ""}, id="skip_empty_str"),
    pytest.param({"take": None}, {}, id="take_none"),
    pytest.param({"take": -1}, {"take": -1}, id="take_negative"),
    pytest.param({"take": 0}, {"take": 0}, id="take_0"),
    pytest.param({"take": 100}, {"take": 100}, id="take_100"),
    pytest.param({"take": "1"}, {"take": "1"}, id="take_is_str"),
    pytest.param({"take": ""}, {"take": ""}, id="take_empty_str"),
]
"""input, expected_output"""


parameter_dicts_invalid = [
    # input, expected_output
    pytest.param({"wtf": None}, TypeError, id="unrecognized_param_none"),
    pytest.param({"wtf": "blah"}, TypeError, id="unrecognized_param_is_str"),
    pytest.param({"wtf": ""}, TypeError, id="unrecognized_param_empty_str"),
]
"""input, expected_output"""
