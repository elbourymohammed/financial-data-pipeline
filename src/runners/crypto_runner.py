import sys
from pathlib import Path
import logging
import os
from dotenv import load_dotenv

load_dotenv()
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, LOG_LEVEL), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

sys.path.insert(0, str(Path(__file__).parent.parent))

from database.Database import Database
from services.crypto_services import get_crypto_usd
from repositories.crypto_repository import insert_crypto

def run() -> None:
    """Ingest Bitcoin price for yesterday."""
    with Database() as db:
        try:
            date_str, price = get_crypto_usd()
            insert_crypto(db, date_str, "bitcoin", price)
            logger.info(f"Inserted crypto: {date_str} -> {price}")
        except Exception as e:
            logger.error(f"Error occurred: {e}")

if __name__ == "__main__":
    run()