from typing import Any, Optional

import helper_test_cases
import pytest

from client.core import utils


@pytest.mark.parametrize(["input", "expected_output"], helper_test_cases.parameter_dicts)
def test__create_parameter_dict(input: Optional[dict[str, Any]], expected_output: dict[str, Any]):
    if input is None:
        output = utils.create_parameter_dict()
    else:
        output = utils.create_parameter_dict(**input)
    assert expected_output == output
