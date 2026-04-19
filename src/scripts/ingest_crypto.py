import requests
from datetime import datetime, timedelta
from database.Database import Database


def get_crypto_usd(date: datetime):
    formatted_date = date.strftime("%d-%m-%Y")

    url = "https://api.coingecko.com/api/v3/coins/bitcoin/history"

    params = {
        "date": formatted_date,
        "localization": "false"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception(f"API error: {response.status_code} - {response.text}")

    data = response.json()

    usd_price = data["market_data"]["current_price"]["usd"]

    return formatted_date, usd_price


def insert_crypto(db, date, crypto, price):
    ingestion_time = datetime.utcnow()

    query = """
        INSERT INTO raw_crypto_prices (
            date,
            crypto,
            currency,
            price,
            ingestion_timestamp
        )
        VALUES (%s, %s, %s, %s, %s)
    """

    db.execute(query, (
        str(date),
        crypto,
        "USD",
        price,
        ingestion_time
    ))


def generate_dates(start: str, n: int):
    start_date = datetime.strptime(start, "%Y%m%d")
    dates = []
    current = start_date

    while len(dates) < n:
        if current.weekday() < 5:
            dates.append(current)
        current += timedelta(days=1)

    return dates


if __name__ == "__main__":

    db: Database = Database()
    db.connect()

    dates = generate_dates("20251031", 5)

    for date in dates:
        try:
            formatted_date, price = get_crypto_usd(date)
            
            insert_crypto(db, date, "bitcoin", price)

            print(f"✅ Inserted: {formatted_date} -> {price}")

        except Exception as e:
            db.disconnect()
            print(f"❌ Error for {date}: {e}")
        
    db.disconnect()
