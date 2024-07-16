import pytest

from client.core.exceptions import *


invalid_filter_parameters = [
    # parameters, expected_exception
    pytest.param({"from_date": "abc"}, InvalidFromDateError, id="from_date_random_string"),
    pytest.param({"from_date": "2016-13-01T00:00:00"}, InvalidFromDateError, id="from_date_not_a_valid_date"),
    pytest.param({"from_date": "2016-01-01T00:00:00"}, FromDateTooEarlyError, id="from_date_too_early"),
    pytest.param({"to_date": "abc"}, InvalidToDateError, id="to_date_random_string"),
    pytest.param({"to_date": "2016-13-01T00:00:00"}, InvalidToDateError, id="to_date_not_a_valid_date"),
    pytest.param({"to_date": "2016-01-01T00:00:00"}, ToDateTooEarlyError, id="to_date_too_early"),
    pytest.param(
        {
            "from_date": "2020-02-01T00:00:00Z",
            "to_date": "2020-01-01T00:00:00Z",
        },
        FromDateAfterToDateError,
        id="from_date_after_to_date",
    ),
    pytest.param({"interval": "invalid"}, InvalidIntervalError, id="interval_invalid"),
    pytest.param({"skip": -1}, InvalidSkipError, id="skip_negative"),
    pytest.param({"take": -1}, InvalidTakeError, id="take_negative"),
    pytest.param({"take": 101}, InvalidTakeError, id="take_too_big"),
]
"""parameters, expected_exception"""


def invalid_parameter_types(expected_type: str) -> list[pytest.param]:
    invalid_parameters: dict[str, list[pytest.param]] = {
        "bool": [
            pytest.param(True, id="type_bool_True"),
            pytest.param(False, id="type_bool_False"),
        ],
        "float": [
            pytest.param(0.1, id="type_float_0.1"),
            pytest.param(1.1, id="type_float_1.1"),
        ],
        "int": [
            pytest.param(0, id="type_int_0"),
            pytest.param(1, id="type_int_1"),
        ],
        "str": [
            pytest.param("", id="type_str_empty"),
            pytest.param("abc", id="type_str_random"),
        ],
    }

    result = []
    for key, value in invalid_parameters.items():
        if key != expected_type:
            result.extend(value)

    return result
