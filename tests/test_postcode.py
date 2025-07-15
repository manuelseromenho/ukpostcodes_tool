import pytest
from ukpostcodes_tool.core import Postcode


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("ec1a1bb", "EC1A 1BB"),
        (" W1A0AX ", "W1A 0AX"),
        ("   m11ae", "M1 1AE"),
    ],
)
def test_normalize(raw, expected):
    assert Postcode.normalize(raw) == expected


@pytest.mark.parametrize(
    "postcode",
    [
        "EC1A 1BB",  # Valid central London
        "W1A 0AX",  # Valid central London
        "M1 1AE",  # Valid A9 9AA
        "B33 8TH",  # Valid A99 9AA
        "DN55 1PT",  # Valid AA99 9AA
        "GIR 0AA",  # Special case
        "XM4 5HQ",  # Special case
        "SAN TA1",  # Special case
        "W7 2JY",
    ],
)
def test_valid_postcodes(postcode):
    assert Postcode.validate(postcode)


@pytest.mark.parametrize(
    "postcode",
    [
        "EC1",  # too short
        "W1A AX",  # missing digit
        "ZZ99 9ZZ",  # invalid area
        "EC1Z 1BB",  # disallowed 3rd letter
        "ER0 1AA",  # area with 0 that isn't in ZERO_ONLY_ALLOWED_DISTRICTS
        "",  # too short
    ],
)
def test_invalid_postcodes(postcode):
    assert not Postcode.validate(postcode)


@pytest.mark.parametrize(
    "postcode",
    [
        "AB99 9ZZ",  # non-geographic
        "CH30 1AB",  # non-geographic range
        "SR43 4AE",  # known valid
        "EC1P 1ZZ",  # non-geographic letter suffix
    ],
)
def test_non_geographic_districts(postcode):
    assert Postcode.validate(postcode)


@pytest.mark.parametrize(
    "postcode",
    [
        "WC1A 1AB",  # central London valid subdivision
        "SW1A 2AA",
        "NW1W 1BB",
    ],
)
def test_central_london_subdivisions(postcode):
    assert Postcode.validate(postcode)


@pytest.mark.parametrize(
    "postcode",
    [
        "AB10 1AA",  # double-digit district
        "LL11 2BB",
        "SO97 4AA",
        "SO15 2GB",
    ],
)
def test_double_digit_only_areas(postcode):
    assert Postcode.validate(postcode)


@pytest.mark.parametrize(
    "postcode",
    [
        "BR9 9AA",  # single-digit district
        "FY1 8QQ",
    ],
)
def test_single_digit_only_areas(postcode):
    assert Postcode.validate(postcode)


@pytest.mark.parametrize(
    "postcode",
    [
        "BS0 1AA",  # district zero allowed
        "CR0 2YZ",
    ],
)
def test_zero_only_areas(postcode):
    assert Postcode.validate(postcode)


def test_instance_interface():
    p = Postcode("ec1a1bb")
    assert p.get_normalized() == "EC1A 1BB"
    assert p.is_valid() is True
