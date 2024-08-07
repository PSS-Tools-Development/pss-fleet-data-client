from datetime import datetime

import pytest
from pssapi.enums import AllianceMembership

from pss_fleet_data.utils import encode_alliance_membership


test_cases_invalid = [
    # value, expected_exception
    pytest.param(None, pytest.raises(ValueError), id="none"),
    pytest.param("1234", pytest.raises(ValueError), id="str"),
    pytest.param(True, pytest.raises(TypeError), id="bool"),
    pytest.param(12.34, pytest.raises(TypeError), id="float"),
    pytest.param(1234, pytest.raises(TypeError), id="int"),
    pytest.param(complex("-1.23+4.5j"), pytest.raises(TypeError), id="complex"),
    pytest.param([5020], pytest.raises(TypeError), id="list[int]"),
    pytest.param({"seconds": 5020}, pytest.raises(TypeError), id="dict[str, int]"),
    pytest.param((datetime(2016, 1, 1),), pytest.raises(TypeError), id="tuple[datetime]"),
]


test_cases_valid = [
    # value, expected_result
    pytest.param("None", -1, id="rank_none_as_str"),
    pytest.param("Candidate", 6, id="rank_candidate_as_str"),
    pytest.param("Ensign", 5, id="rank_ensign_as_str"),
    pytest.param("Lieutenant", 4, id="rank_lieutenant_as_str"),
    pytest.param("Major", 3, id="rank_major_as_str"),
    pytest.param("Commander", 2, id="rank_commander_as_str"),
    pytest.param("ViceAdmiral", 1, id="rank_vice_admiral_as_str"),
    pytest.param("FleetAdmiral", 0, id="rank_fleet_admiral_as_str"),
    pytest.param(AllianceMembership.NONE, -1, id="rank_none_as_enum"),
    pytest.param(AllianceMembership.CANDIDATE, 6, id="rank_candidate_as_enum"),
    pytest.param(AllianceMembership.ENSIGN, 5, id="rank_ensign_as_enum"),
    pytest.param(AllianceMembership.LIEUTENANT, 4, id="rank_lieutenant_as_enum"),
    pytest.param(AllianceMembership.MAJOR, 3, id="rank_major_as_enum"),
    pytest.param(AllianceMembership.COMMANDER, 2, id="rank_commander_as_enum"),
    pytest.param(AllianceMembership.VICE_ADMIRAL, 1, id="rank_vice_admiral_as_enum"),
    pytest.param(AllianceMembership.FLEET_ADMIRAL, 0, id="rank_fleet_admiral_as_enum"),
]


@pytest.mark.parametrize(["value", "expected_exception"], test_cases_invalid)
def test_encode_alliance_membership_invalid(value, expected_exception):
    with expected_exception:
        _ = encode_alliance_membership(value)


@pytest.mark.parametrize(["value", "expected_result"], test_cases_valid)
def test_encode_alliance_membership_valid(value, expected_result):
    result = encode_alliance_membership(value)
    assert result == expected_result
