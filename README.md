# UK Postcodes Tool

A lightweight Python library to validate and normalize **UK postcodes**, following official UK postcode formatting rules and additional regional constraints.

## Features

- Validates postcode structure using regular expressions
- Applies extra validation rules based on postcode area
- Handles special and non-geographic postcodes
- Normalizes postcodes to uppercase with a single space before the inward code

## Installation

Clone the repo and install with:

```bash
pip install .
```

## Usage

```python
from ukpostcodes_tool.core import Postcode

postcode = Postcode("EC1A1BB")
print(postcode.get_normalized())  # 'EC1A 1BB'
print(postcode.is_valid())        # True or False

# or it's possible to access directly

print(Postcode.normalize("EC1A1BB"))    # 'EC1A 1BB'
print(Postcode.validate("EC1A 1BB"))    # True
print(Postcode.validate("INVALID"))     # False
```

## Validation Logic

The validation occurs in two main steps:

### 1. Regex Validation

Checks the postcode against a regex pattern that covers:
- Standard postcode formats (e.g., A9 9AA, A9A 9AA, AA9 9AA, AA9A 9AA).
- Special cases like 'GIR 0AA', 'XM4 5HQ', and 'SAN TA1'.
- Enforces exactly one space separating outward and inward codes.
- Validates the inward code format (one digit followed by two letters, excluding C, I, K, M, O, V).


### 2. Additional Rules

Applies postcode district-specific rules not enforceable by regex:
- Areas with non-geographic postcodes.
- Areas with only single-digit districts must have exactly one digit in the outward code.
- Areas with only double-digit districts must have exactly two digits in the outward code.
- The digit '0' in the district part is only allowed for certain postcode areas.
- Central London single-digit districts that require an additional letter subdivision
  (e.g., EC1–EC4, SW1, W1, WC1, WC2, E1W, N1C, N1P, NW1W, SE1P) must include this subdivision letter.


## License

MIT © Manuel Seromenho
