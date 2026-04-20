from datetime import datetime, timedelta
from typing import Optional
import logging
import requests

logger = logging.getLogger(__name__)

def get_yesterday_date() -> str:
    """Get yesterday's date in YYYY-MM-DD format."""
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime("%Y-%m-%d")

def get_crypto_usd(date: Optional[str] = None) -> tuple:
    """Fetch Bitcoin price for given date (defaults to yesterday)."""
    if date is None:
        formatted_date = get_yesterday_date()
    else:
        formatted_date = date
    
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
