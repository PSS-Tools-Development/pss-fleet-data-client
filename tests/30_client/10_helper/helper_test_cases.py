import os
from datetime import datetime, timezone

import pytest

from pss_fleet_data.core.enums import ParameterInterval


_DEFAULT_API_KEY = os.getenv("TEST_DEFAULT_API_KEY")


api_keys = [
    # api_key_sent, api_key_expected
    pytest.param(None, _DEFAULT_API_KEY, id="none"),
    pytest.param("", _DEFAULT_API_KEY, id="empty"),
    pytest.param(_DEFAULT_API_KEY, _DEFAULT_API_KEY, id="default"),
    pytest.param("abcdef", "abcdef", id="abcdef"),
]
"""api_key_sent, api_key_expected"""


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
