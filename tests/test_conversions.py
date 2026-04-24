from datetime import date, time

from utils.conversions import safe_date_str, safe_int, safe_time_str, to_time


def test_safe_int_handles_invalid_values():
    assert safe_int("12") == 12
    assert safe_int(None, default=5) == 5
    assert safe_int("invalid", default=0) == 0


def test_date_and_time_formatters():
    assert safe_date_str(date(2026, 4, 24)) == "2026-04-24"
    assert safe_time_str(time(7, 5, 0)) == "07:05:00"
    assert safe_time_str("7:5:0") == "07:05:00"


def test_to_time_accepts_common_formats():
    assert to_time("07:30").strftime("%H:%M:%S") == "07:30:00"
    assert to_time("7:0:0").strftime("%H:%M:%S") == "07:00:00"
    assert to_time(None) is None
