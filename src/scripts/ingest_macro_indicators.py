import os
import requests
from datetime import datetime
from database.Database import Database

FRED_API_KEY = os.getenv("FRED_API_KEY")

FRED_SERIES = {
    "CPI": "CPIAUCSL",        # Inflation
    "UNEMPLOYMENT": "UNRATE", # Chômage
    "GDP": "GDP"              # PIB
}

def get_fred_data(series_id: str):
    url = "https://api.stlouisfed.org/fred/series/observations"

    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception(f"API error: {response.status_code} - {response.text}")

    return response.json().get("observations", [])

def insert_macro(db, observations, indicator_name):
    query = """
        INSERT INTO raw_macro_indicators (
            date, indicator_name, value, country, ingestion_timestamp
        )
        VALUES (%s, %s, %s, %s, %s)
    """

    for obs in observations:
        date_str = obs.get("date")
        value_str = obs.get("value")

        # skip missing values
        if value_str == ".":
            continue

        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        value = float(value_str)

        db.execute(query, (
            date,
            indicator_name,
            value,
            "USA",
            datetime.utcnow()
        ))


def main():
    db: Database = Database()
    db.connect()

    total_inserted = 0

    for name, series_id in FRED_SERIES.items():
        print(f"🔄 Fetching {name}...")

        observations = get_fred_data(series_id)
        print(observations)
        insert_macro(db, observations, name)

        total_inserted += len(observations)

    db.disconnect()
    print(f"✅ Total data ingested: {total_inserted}")


if __name__ == "__main__":
    main()