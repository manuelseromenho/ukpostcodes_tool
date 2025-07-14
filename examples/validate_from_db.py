import sqlite3

from src.ukpostcodes_tool.core import Postcode

DB_PATH = "postcodes_convert.sqlite"


def validate_postcodes_from_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("select postcode from postcodes")
    rows = cursor.fetchall()

    valid_count = 0
    invalid_count = 0

    for i, (raw_postcode,) in enumerate(rows, 1):
        if raw_postcode is None:
            continue

        normalized = Postcode.normalize(raw_postcode)

        if Postcode.validate(raw_postcode):
            valid_count += 1
        else:
            invalid_count += 1
            print(f"❌ Invalid postcode on row {i}: '{raw_postcode}' → '{normalized}'")

    print(f"\nSummary: ✅ Valid: {valid_count} | ❌ Invalid: {invalid_count}")

    conn.close()


if __name__ == "__main__":
    validate_postcodes_from_db()
