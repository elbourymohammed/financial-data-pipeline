import os
import requests
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

FRED_API_KEY = os.getenv("FRED_API_KEY")

FRED_SERIES = {
    "CPI":          "CPIAUCSL",
    "UNEMPLOYMENT": "UNRATE",
    "GDP":          "GDP"
}

def get_fred_data(series_id: str) -> list:
    response = requests.get(
        "https://api.stlouisfed.org/fred/series/observations",
        params={
            "series_id": series_id,
            "api_key":   FRED_API_KEY,
            "file_type": "json"
        },
        timeout=10
    )
    if response.status_code != 200:
        raise Exception(f"API error: {response.status_code} - {response.text}")
    return response.json().get("observations", [])