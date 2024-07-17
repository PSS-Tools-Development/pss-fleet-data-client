from typing import Any, Optional

import pytest
import utils_test_cases

from client.core import utils


@pytest.mark.parametrize(["input", "expected_output"], utils_test_cases.parameter_dicts)
def test_create_parameter_dict(input: Optional[dict[str, Any]], expected_output: dict[str, Any]):
    if input is None:
        output = utils.create_parameter_dict()
    else:
        output = utils.create_parameter_dict(**input)
    assert expected_output == output


@pytest.mark.parametrize(["input", "expected_error"], utils_test_cases.parameter_dicts_invalid)
def test_create_parameter_dict_invalid(input: Optional[dict[str, Any]], expected_error: Exception):
    with pytest.raises(expected_error):
        _ = utils.create_parameter_dict(**input)
