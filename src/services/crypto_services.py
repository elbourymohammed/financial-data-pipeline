from datetime import datetime, timedelta
import logging
import requests

logger = logging.getLogger(__name__)

def get_crypto_usd(date: datetime) -> tuple:
    """Fetch Bitcoin price for given date."""
    formatted_date = date.strftime("%Y-%m-%d")
    
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/history"
    params = {"date": formatted_date, "localization": "false"}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        usd_price = data.get("market_data", {}).get("current_price", {}).get("usd")
        
        if usd_price is None:
            raise ValueError(f"Bitcoin price not found for {formatted_date}")
        
        logger.info(f"Fetched Bitcoin price: {usd_price} USD on {formatted_date}")
        return formatted_date, float(usd_price)
    except (requests.RequestException, ValueError) as e:
        logger.error(f"Error fetching Bitcoin price: {e}")
        raise

def generate_dates(start: str, n: int):
    start_date = datetime.strptime(start, "%Y%m%d")
    dates = []
    current = start_date

    while len(dates) < n:
        if current.weekday() < 5:
            dates.append(current)
        current += timedelta(days=1)

    return dates
