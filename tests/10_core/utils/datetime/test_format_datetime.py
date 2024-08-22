from src.pss_fleet_data.utils.datetime import format_datetime


def test_returns_none_if_passed_none():
    result = format_datetime(None)
    assert result is None
