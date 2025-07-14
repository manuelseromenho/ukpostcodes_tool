import pytest
from src.ukpostcodes_tool.core import Postcode


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("w1a0ax", "W1A 0AX"),
        ("EC1A1BB", "EC1A 1BB"),
        ("dn551pt", "DN55 1PT"),
        ("GIR0AA", "GIR 0AA"),
    ],
)
def test_normalize_postcode(raw, expected):
    assert Postcode.normalize(raw) == expected


@pytest.mark.parametrize(
    "valid_code",
    [
        "W1A 0AX",
        "EC1A 1BB",
        "M1 1AE",
        "B33 8TH",
        "CR2 6XH",
        "DN55 1PT",
        "GIR 0AA",
    ],
)
def test_valid_postcodes(valid_code):
    assert Postcode.validate(valid_code)


@pytest.mark.parametrize(
    "invalid_code",
    ["ZZ1 1ZZ", "W1A0A", "123 456", "EC1!", "AA@ 9AA", "ABCDE", "", "M1 1AE1"],
)
def test_invalid_postcodes(invalid_code):
    assert not Postcode.validate(invalid_code)
