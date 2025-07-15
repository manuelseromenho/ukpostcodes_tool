from ukpostcodes_tool.constants import (
    CENTRAL_LONDON_DISTRICTS_REQUIRING_SUBDIVISION,
    DOUBLE_DIGIT_DISTRICTS,
    NON_GEOGRAPHIC_DISTRICTS,
    SINGLE_DIGIT_DISTRICTS,
    UK_POSTCODE_REGEX,
    ZERO_ONLY_ALLOWED_DISTRICTS,
)
from ukpostcodes_tool.logging_setup import setup_logger


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
        get_normalized (str): The postcode formatted with uppercase letters and a single space before the last three characters.
        is_valid (bool): True if the postcode passes both regex and additional district-specific validations; False otherwise.
    """

    def __init__(self, raw_postcode: str):
        self._raw_postcode = raw_postcode
        self._normalized = self.normalize(raw_postcode)
        self._outward, self._inward = self._normalized.split()
        self._area = "".join([c for c in self._outward if c.isalpha()])
        self._digits = "".join([c for c in self._outward if c.isdigit()])

    def is_valid(self):
        return self.validate(self._raw_postcode)

    def get_normalized(self):
        return self._normalized

    def _is_valid_central_london_subdistrict(self) -> bool:
        for prefix in CENTRAL_LONDON_DISTRICTS_REQUIRING_SUBDIVISION:
            if self._outward.startswith(prefix) and len(self._outward) >= len(prefix):
                return True

        return any(
            self._outward.startswith(prefix) and len(self._outward) >= len(prefix)
            for prefix in CENTRAL_LONDON_DISTRICTS_REQUIRING_SUBDIVISION
        )

    def _is_non_geographic_and_valid(self):
        if self._area == "BF":
            return True
        if self._area == "BX":
            # Must be in the format BXd, where d is 1-9
            return (
                len(self._digits) == 1
                and self._digits.isdigit()
                and self._digits != "0"
            )
        if self._area == "XX":
            # Must be in the format XXd or XXdd
            return (
                self._digits.isdigit()
                and 1 <= len(self._digits) <= 2
                and self._digits != "0"
            )

        return self._outward in NON_GEOGRAPHIC_DISTRICTS

    def _is_valid_single_digit_district(self) -> bool:
        return len(self._digits) == 1

    def _is_valid_double_digit_district(self) -> bool:
        return len(self._digits) == 2

    def _is_valid_zero_rule(self) -> bool:
        return self._area in ZERO_ONLY_ALLOWED_DISTRICTS

    def _does_it_pass_additional_rules(self) -> bool:
        if self._digits == "0" and not self._is_valid_zero_rule():
            return False

        if self._is_valid_central_london_subdistrict():
            return True

        if self._outward in NON_GEOGRAPHIC_DISTRICTS or self._area in {
            "BF",
            "BX",
            "XX",
        }:
            return self._is_non_geographic_and_valid()

        if (
            self._area in SINGLE_DIGIT_DISTRICTS
            and not self._is_valid_single_digit_district()
        ):
            return False

        if (
            self._area in DOUBLE_DIGIT_DISTRICTS
            and not self._is_valid_double_digit_district()
        ):
            return False

        return True

    @classmethod
    def validate(cls, raw_postcode: str) -> bool:
        """
        Validate the postcode format against the UK postcode rules.
        """
        try:
            instance = cls(raw_postcode)
        except ValueError:
            logger = setup_logger()
            logger.error("Invalid Postcode, needs at least 4 chars")
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
