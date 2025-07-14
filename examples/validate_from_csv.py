import csv
from pathlib import Path

from src.ukpostcodes_tool.core import Postcode

CURRENT_DIR = Path(__file__).parent.resolve()
CSV_FILE_PATH = CURRENT_DIR / "sampled_postcodes.csv"


def validate_postcodes_in_csv():
    print(f"\n📄 Processing file: {CSV_FILE_PATH.name}")
    valid, invalid = 0, 0

    with CSV_FILE_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if not row:
                continue

            raw_postcode = row[0].strip()
            if Postcode.validate(raw_postcode):
                valid += 1
            else:
                normalized = Postcode.normalize(raw_postcode)
                invalid += 1
                print(f"  ❌ Line {i+1}: '{raw_postcode}' → '{normalized}'")

    print(f"✅ Valid: {valid} | ❌ Invalid: {invalid}")


if __name__ == "__main__":
    validate_postcodes_in_csv()
