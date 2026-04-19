import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv, find_dotenv

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


def generate_dates(start: str, n: int):
    start_date = datetime.strptime(start, "%Y%m%d")
    dates = []
    current = start_date

    while len(dates) < n:
        if current.weekday() < 5:  # skip weekend
            dates.append(current.strftime("%Y-%m-%d"))
        current += timedelta(days=1)

    return dates