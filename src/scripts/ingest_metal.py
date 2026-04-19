import os
import requests
from datetime import datetime, timedelta

from typing import Dict, Any
from dotenv import load_dotenv, find_dotenv

from database.Database import Database

load_dotenv(find_dotenv())

API_KEY = os.getenv("METAL_API_KEY")
BASE_URL = f"https://www.goldapi.io/api/"

def fetch_gold_price(metal_symbol, currency_code, date: str):
    headers = {
        "x-access-token": API_KEY,
        "Content-Type": "application/json"
    }

    try:
        URL = f"{BASE_URL}/{metal_symbol}/{currency_code}/{date}"

        response = requests.get(URL, headers=headers, timeout=10)
        response.raise_for_status()  # gère les erreurs HTTP

        raw : Dict[str, Any]= response.json()

        return {
            "date":             raw.get("date"),
            "metal":            raw.get("metal"),
            "exchange":         raw.get("exchange"),
            "currency":         raw.get("currency"),
            "price":            raw.get("price"),
            "prev_close_price": raw.get("prev_close_price"),
            "change":           raw.get("ch"),
            "change_percent":   raw.get("chp"),
            "price_gram_24k":   raw.get("price_gram_24k"),
            "price_gram_22k":   raw.get("price_gram_22k"),
            "price_gram_21k":   raw.get("price_gram_21k"),
            "price_gram_20k":   raw.get("price_gram_20k"),
            "price_gram_18k":   raw.get("price_gram_18k"),
            "price_gram_16k":   raw.get("price_gram_16k"),
            "price_gram_14k":   raw.get("price_gram_14k"),
            "price_gram_10k":   raw.get("price_gram_10k"),
        }

    except requests.exceptions.RequestException as e:
        print(f"API error: {e}")
        return None

def load_data(db: Database, data: dict) -> None:
    
    query = """
        INSERT INTO raw_metal_prices (
            date, metal, exchange, currency, price,
            prev_close_price, change, change_percent,
            price_gram_24k, price_gram_22k, price_gram_21k, price_gram_20k,
            price_gram_18k, price_gram_16k, price_gram_14k, price_gram_10k
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s
        )
    """
    
    db.execute(query, tuple(data.values()))
    
def generate_dates(start: str, n: int) -> list:
    start_date = datetime.strptime(start, "%Y%m%d")
    dates = []
    current = start_date
    while len(dates) < n:
        if current.weekday() < 5:
            dates.append(current.strftime("%Y%m%d"))
        current += timedelta(days=1)
    return dates
    
if __name__ == "__main__":
    # Connexion Bdd 
    db: Database = Database()
    db.connect()
    
    # Récupération des données depuis l'api
    dates = generate_dates("20251017", 10)

    for date in dates:
        for metal in ['XAU', 'XAG', 'XPT', 'XPD']:
            data = fetch_gold_price(metal, 'USD', date) 
            if data is None:
                print(f"Limite de requête atteinte de l'api")
            else:
                # alimentation de la bdd
                load_data(db, data=data)
