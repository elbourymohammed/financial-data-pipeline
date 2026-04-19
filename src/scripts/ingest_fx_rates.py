import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv, find_dotenv

from database.Database import Database

load_dotenv(find_dotenv())

FX_API_TOKEN = os.getenv("FX_API_TOKEN")
BASE_URL = "https://api.fxratesapi.com"


def get_fx_rates(date: str):
    url = f"{BASE_URL}/historical"  # YYYY-MM-DD

    headers = {
        "Authorization": f"Bearer {FX_API_TOKEN}"
    }

    params = {
        "base": "USD",
        "date": date
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        raise Exception(f"API error: {response.status_code} - {response.text}")

    return response.json()


def insert_fx_data(db, data):
    base = data.get("base")
    rates = data.get("rates", {})
    timestamp = data.get("date")

    ingestion_time = datetime.utcnow()

    query = """
        INSERT INTO raw_fx_rates (
            date,
            base_currency,
            target_currency,
            rate,
            ingestion_timestamp
        )
        VALUES (%s, %s, %s, %s, %s)
    """

    for currency, rate in rates.items():
        db.execute(query, (
            timestamp,
            base,
            currency,
            rate,
            ingestion_time
        ))


def generate_dates(start: str, n: int):
    start_date = datetime.strptime(start, "%Y%m%d")
    dates = []
    current = start_date

    while len(dates) < n:
        if current.weekday() < 5:  # skip weekend
            dates.append(current.strftime("%Y-%m-%d"))
        current += timedelta(days=1)

    return dates


def main():
    try:
        db: Database = Database()
        db.connect()
        
        dates = generate_dates("20251017", 10)

        for date in dates:
            print(f"Fetching {date}")
            data = get_fx_rates(date)
            insert_fx_data(db, data)

        print("✅ FX data ingested successfully")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()