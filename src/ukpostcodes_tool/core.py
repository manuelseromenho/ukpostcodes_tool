import re

# abcdefghijklmnopqrstuvwxyz

UK_POSTCODE_REGEX = re.compile(
    r"""
    ^(
        (GIR\s0AA)|XM4\s5HQ|SAN\sTA1|                           # Special cases
        (
            (
                ([A-PR-UWYZ][0-9][0-9]?) |                      # A9 or A99
                ([A-PR-UWYZ][A-HK-Y][0-9][0-9]?) |              # AA9 or AA99
                ([A-PR-UWYZ][0-9][A-HJKPSTUW]) |                # A9A
                ([A-PR-UWYZ][A-HK-Y][0-9][ABEHMNPRVWXY])        # AA9A
            )
            \s                                                  # one and only one space
            [0-9][ABD-HJLNP-UW-Z]{2}                            # Inward code
        )
    )$
    """,
    re.VERBOSE | re.IGNORECASE,
)

SINGLE_DIGIT_DISTRICTS = {
    "BL",
    "BR",
    "FY",
    "HA",
    "HD",
    "HG",
    "HR",
    "HS",
    "HX",
    "JE",
    "LD",
    "SM",
    "SR",
    "WC",
    "WN",
    "ZE",
}

DOUBLE_DIGIT_DISTRICTS = {"AB", "LL", "SO"}

ZERO_ONLY_ALLOWED_DISTRICTS = {"BL", "BS", "CM", "CR", "FY", "HA", "PR", "SL", "SS"}

CENTRAL_LONDON_DISTRICTS_REQUIRING_SUBDIVISION = {
    "EC1",
    "EC2",
    "EC3",
    "EC4",
    "SW1",
    "W1",
    "WC1",
    "WC2",
    "E1W",
    "N1C",
    "N1P",
    "NW1W",
    "SE1P",
}

NON_GEOGRAPHIC_DISTRICTS = {
    "AB": {"99"},
    "B": {"99"},
    "BA": {"9"},
    "BB": {"0", "94"},
    "BL": ["11", "78"],
    "BD": {"97", "98", "99"},
    "BN": {"50", "51", "52", "88", "91", "95", "99"},
    "BS": {"0", "98", "99"},
    "BT": {"58"},
    "CA": {"95", "99"},
    "CF": {"30", "91", "95", "99"},
    "CH": {str(i) for i in range(25, 35)}.union({"88", "99"}),
    "CM": {"92", "98", "99"},
    "CR": {"9", "44", "90"},
    "CT": {"50"},
    "CW": {"98"},
    "DE": {"1", "45"},
    "DH": {"97", "98", "99"},
    "DL": {"98"},
    "DN": {"55"},
    "E": {"77", "98"},
    "EC": {"1P", "2P", "3P", "4P", "50"},
    "EH": {"77", "91", "95", "99"},
    "G": {"9", "58", "70", "79", "90"},
    "GL": {"11"},
    "GU": {"95"},
    "HP": {"22"},
    "IP": {"98"},
    "IV": {"99"},
    "KY": {"99"},
    "L": {"67", "69", "70", "71", "72", "73", "74", "75", "80"},
    "LE": {"21", "41", "55", "87", "94", "95"},
    "LS": {"88", "98", "99"},
    "M": {"60", "61", "99"},
    "ME": {"99"},
    "MK": {"77"},
    "N": {"1P", "81"},
    "NE": {"82", "83", "85", "88", "92", "98", "99"},
    "NG": {"70", "80", "90"},
    "NN": {"99"},
    "NR": {"18", "19", "26", "99"},
    "NW": {"1W", "26"},
    "OL": {"16", "95"},
    "PE": {"99"},
    "PL": {"95"},
    "PO": {"24"},
    "PR": {"0", "11"},
    "RH": {"77"},
    "S": {"49", "94", "95", "96", "97", "98", "99"},
    "SA": {"48", "72", "80", "99"},
    "SE": {"1P"},
    "SR": {"9", "43"},
    "SS": {"1"},
    "SY": {"99"},
    "TN": {"2"},
    "TQ": {"9"},
    "UB": {"3", "5", "8", "18"},
    "W": {"1A"},
    "WA": {"55", "88"},
    "WD": {"99"},
    "WF": {"90"},
    "WR": {"11", "78", "99"},
    "WV": {"1", "98", "99"},
    "YO": {"90"},
    "JE": {"1", "4", "5"},
    "IM": {"86", "87", "99"},
}


class Postcode:
    """
    Normalize and Validate a UK postcode.

    This class validates UK postcodes in two steps:

    1. Regex Validation:
       - Checks the postcode against a regex pattern that covers:
         - Standard postcode formats (e.g., A9 9AA, A9A 9AA, AA9 9AA, AA9A 9AA).
         - Special cases like 'GIR 0AA', 'XM4 5HQ', and 'SAN TA1'.
         - Enforces exactly one space separating outward and inward codes.
         - Validates the inward code format (one digit followed by two letters, excluding C, I, K, M, O, V).

    2. Additional Rule Validation (_does_it_pass_additional_rules):
       - Applies postcode district-specific rules not enforceable by regex:
         - Areas with non-geographic postcodes.
         - Areas with only single-digit districts must have exactly one digit in the outward code.
         - Areas with only double-digit districts must have exactly two digits in the outward code.
         - The digit '0' in the district part is only allowed for certain postcode areas.
         - Central London single-digit districts that require an additional letter subdivision
           (e.g., EC1–EC4, SW1, W1, WC1, WC2, E1W, N1C, N1P, NW1W, SE1P) must include this subdivision letter.

    Usage:
        postcode = Postcode("EC1A1BB")
        print(postcode.get_normalized())  # 'EC1A 1BB'
        print(postcode.is_valid())    # True or False

        or it's possible to access directly

        print(Postcode.normalize("EC1A1BB") # 'EC1A 1BB'
        print(Postcode.validate("EC1A 1BB") # True or False



    Args:
        raw_postcode (str): The postcode string to validate (may be unformatted).

    Attributes:
        _normalized (str): The postcode formatted with uppercase letters and a single space before the last three characters.
        is_valid (bool): True if the postcode passes both regex and additional district-specific validations; False otherwise.
    """

    def __init__(self, raw_postcode: str):
        self._raw_postcode = raw_postcode
        self._normalized = self.normalize(raw_postcode)
        self._outward, self._inward = self._normalized.split()
        self._area = None
        self._digits = None

    def is_valid(self):
        return self.validate(self._raw_postcode)

    def get_normalized(self):
        return self._normalized

    def _is_valid_central_london_specific_rules(self) -> bool:
        return any(
            self._outward.startswith(prefix) and len(self._outward) >= len(prefix)
            for prefix in CENTRAL_LONDON_DISTRICTS_REQUIRING_SUBDIVISION
        )

    def _is_valid_non_geographic_rules(self):
        if self._area == "BX":
            # Must be in the format BXd, where d is 1-9
            return (
                len(self._digits) == 1
                and self._digits.isdigit()
                and self._digits != "0"
            )
        if self._area == "XX":
            # Must be in the format XXd or XXdd
            return self._digits.isdigit() and 1 <= len(self._digits) <= 2
        if (
            self._area in NON_GEOGRAPHIC_DISTRICTS
            and self._digits in NON_GEOGRAPHIC_DISTRICTS[self._area]
        ):
            return True

    def _is_valid_single_digit_district(self) -> bool:
        if self._area in SINGLE_DIGIT_DISTRICTS:
            return len(self._digits) == 1

    def _is_valid_double_digit_district(self) -> bool:
        if self._area in DOUBLE_DIGIT_DISTRICTS:
            return len(self._digits) == 2

    def _is_valid_zero_rule(self) -> bool:
        if self._area in ZERO_ONLY_ALLOWED_DISTRICTS:
            if self._digits == 0:
                return True

    def _does_it_pass_additional_rules(self) -> bool:
        if self._is_valid_central_london_specific_rules():
            return True

        self._area = "".join([c for c in self._outward if c.isalpha()])
        self._digits = "".join([c for c in self._outward if c.isdigit()])

        rules = [
            self._is_valid_non_geographic_rules(),
            self._is_valid_single_digit_district(),
            self._is_valid_double_digit_district(),
            self._is_valid_zero_rule(),
        ]

        if any(rule is True for rule in rules) or all(rule is None for rule in rules):
            return True

        return False

    @classmethod
    def validate(cls, raw_postcode: str) -> bool:
        """
        Validate the postcode format against the UK postcode rules.
        """
        try:
            instance = cls(raw_postcode)
        except ValueError:
            return False
        if not bool(UK_POSTCODE_REGEX.match(instance._normalized)):
            return False
        return instance._does_it_pass_additional_rules()

    @classmethod
    def normalize(cls, raw_postcode: str) -> str:
        """
        Normalize the postcode: Ensure it's uppercase, no spaces, ensure one space before last 3 chars.
        """

        normalized_postcode = raw_postcode.strip().replace(" ", "").upper()
        return normalized_postcode[:-3] + " " + normalized_postcode[-3:]
