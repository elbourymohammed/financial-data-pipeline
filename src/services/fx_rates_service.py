import os
import requests
from datetime import datetime, timedelta
from typing import Optional
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

FX_API_TOKEN = os.getenv("FX_API_TOKEN")
BASE_URL = "https://api.fxratesapi.com"


def get_yesterday_date() -> str:
    """Get yesterday's date in YYYY-MM-DD format."""
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime("%Y-%m-%d")


def get_fx_rates(date: Optional[str] = None):
    """Fetch FX rates for given date (defaults to yesterday)."""
    if date is None:
        date = get_yesterday_date()
    
    url = f"{BASE_URL}/historical"

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