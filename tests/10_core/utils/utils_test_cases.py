from datetime import datetime, timezone

import pytest

from client.core.enums import ParameterInterval


from_to_timestamps = [
    # timestamp, interval, expected_from_date, expected_to_date
    pytest.param(datetime(2017, 1, 6), ParameterInterval.HOURLY, datetime(2017, 1, 5, 23), datetime(2017, 1, 6), id="hourly"),
    pytest.param(datetime(2017, 1, 6), ParameterInterval.DAILY, datetime(2017, 1, 5), datetime(2017, 1, 6), id="daily"),
    pytest.param(datetime(2017, 1, 6), ParameterInterval.MONTHLY, datetime(2016, 12, 6), datetime(2017, 1, 6), id="monthly"),
    #
    pytest.param(datetime(2017, 1, 1), ParameterInterval.HOURLY, datetime(2016, 12, 31, 23), datetime(2017, 1, 1), id="hourly_on_first_of_year"),
    pytest.param(datetime(2017, 1, 1), ParameterInterval.DAILY, datetime(2016, 12, 31), datetime(2017, 1, 1), id="daily_on_first_of_year"),
    pytest.param(datetime(2017, 1, 1), ParameterInterval.MONTHLY, datetime(2016, 12, 1), datetime(2017, 1, 1), id="monthly_on_first_of_year"),
    #
    pytest.param(datetime(2017, 7, 1), ParameterInterval.HOURLY, datetime(2017, 6, 30, 23), datetime(2017, 7, 1), id="hourly_on_first_of_month"),
    pytest.param(datetime(2017, 7, 1), ParameterInterval.DAILY, datetime(2017, 6, 30), datetime(2017, 7, 1), id="daily_on_first_of_month"),
    pytest.param(datetime(2017, 7, 1), ParameterInterval.MONTHLY, datetime(2017, 6, 1), datetime(2017, 7, 1), id="monthly_on_first_of_month"),
    #
    pytest.param(datetime(2017, 1, 6, 12), ParameterInterval.HOURLY, datetime(2017, 1, 6, 11), datetime(2017, 1, 6, 12), id="hourly_with_hours"),
    pytest.param(datetime(2017, 1, 6, 12), ParameterInterval.DAILY, datetime(2017, 1, 5, 12), datetime(2017, 1, 6, 12), id="daily_with_hours"),
    pytest.param(datetime(2017, 1, 6, 12), ParameterInterval.MONTHLY, datetime(2016, 12, 6, 12), datetime(2017, 1, 6, 12), id="monthly_with_hours"),
    #
    pytest.param(datetime(2017, 1, 6), ParameterInterval.HOURLY, datetime(2017, 1, 5, 23), datetime(2017, 1, 6), id="hourly_with_minutes"),
    pytest.param(datetime(2017, 1, 6), ParameterInterval.DAILY, datetime(2017, 1, 5), datetime(2017, 1, 6), id="daily_with_minutes"),
    pytest.param(datetime(2017, 1, 6), ParameterInterval.MONTHLY, datetime(2016, 12, 6), datetime(2017, 1, 6), id="monthly_with_minutes"),
    #
    pytest.param(datetime(2017, 1, 6), ParameterInterval.HOURLY, datetime(2017, 1, 5, 23), datetime(2017, 1, 6), id="hourly_with_seconds"),
    pytest.param(datetime(2017, 1, 6), ParameterInterval.DAILY, datetime(2017, 1, 5), datetime(2017, 1, 6), id="daily_with_seconds"),
    pytest.param(datetime(2017, 1, 6), ParameterInterval.MONTHLY, datetime(2016, 12, 6), datetime(2017, 1, 6), id="monthly_with_seconds"),
    #
    pytest.param(
        datetime(2017, 1, 6, tzinfo=timezone.utc),
        ParameterInterval.HOURLY,
        datetime(2017, 1, 5, 23, tzinfo=timezone.utc),
        datetime(2017, 1, 6, tzinfo=timezone.utc),
        id="hourly_with_tzinfo",
    ),
    pytest.param(
        datetime(2017, 1, 6, tzinfo=timezone.utc),
        ParameterInterval.DAILY,
        datetime(2017, 1, 5, tzinfo=timezone.utc),
        datetime(2017, 1, 6, tzinfo=timezone.utc),
        id="daily_with_tzinfo",
    ),
    pytest.param(
        datetime(2017, 1, 6, tzinfo=timezone.utc),
        ParameterInterval.MONTHLY,
        datetime(2016, 12, 6, tzinfo=timezone.utc),
        datetime(2017, 1, 6, tzinfo=timezone.utc),
        id="monthly_with_tzinfo",
    ),
    #
    pytest.param(
        datetime(2017, 1, 6, 3, 12, 56),
        ParameterInterval.HOURLY,
        datetime(2017, 1, 6, 2, 12, 56),
        datetime(2017, 1, 6, 3, 12, 56),
        id="hourly_mixed",
    ),
    pytest.param(
        datetime(2017, 1, 6, 8, 0, 12),
        ParameterInterval.DAILY,
        datetime(2017, 1, 5, 8, 0, 12),
        datetime(2017, 1, 6, 8, 0, 12),
        id="daily_mixed",
    ),
    pytest.param(
        datetime(2017, 1, 6, 0, 0, 59),
        ParameterInterval.MONTHLY,
        datetime(2016, 12, 6, 0, 0, 59),
        datetime(2017, 1, 6, 0, 0, 59),
        id="monthly_mixed",
    ),
]
"""timestamp, interval, expected_from_date, expected_to_date"""


parameter_dicts = [
    # input, expected_output
    pytest.param(None, {}, id="none"),
    pytest.param({}, {}, id="empty"),
    pytest.param({"from_date": None}, {}, id="fromDate_none"),
    pytest.param({"from_date": "blah"}, {"fromDate": "blah"}, id="fromDate_is_str"),
    pytest.param({"from_date": ""}, {}, id="fromDate_empty_str"),
    pytest.param({"from_date": datetime(2016, 1, 6)}, {"fromDate": datetime(2016, 1, 6)}, id="fromDate_without_tzinfo"),
    pytest.param(
        {"from_date": datetime(2016, 1, 6, tzinfo=timezone.utc)},
        {"fromDate": datetime(2016, 1, 6, tzinfo=timezone.utc)},
        id="fromDate_with_tzinfo",
    ),
    pytest.param({"to_date": None}, {}, id="toDate_none"),
    pytest.param({"to_date": "blah"}, {"toDate": "blah"}, id="toDate_is_str"),
    pytest.param({"to_date": ""}, {}, id="toDate_empty_str"),
    pytest.param({"to_date": datetime(2016, 12, 31)}, {"toDate": datetime(2016, 12, 31)}, id="toDate_without_tzinfo"),
    pytest.param(
        {"to_date": datetime(2016, 1, 6, tzinfo=timezone.utc)},
        {"toDate": datetime(2016, 1, 6, tzinfo=timezone.utc)},
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
