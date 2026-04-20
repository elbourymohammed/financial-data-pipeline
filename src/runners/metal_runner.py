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
from services.metal_services import fetch_metal_price, get_yesterday_date
from repositories.metal_repository import insert_metal

def run() -> None:
    """Ingest metal prices for yesterday."""
    with Database() as db:
        date = get_yesterday_date()
        metals = ['XAU', 'XAG', 'XPT', 'XPD']
        for metal in metals:
            try:
                data = fetch_metal_price(metal, 'USD', date)
                if data:
                    insert_metal(db, data)
                    logger.info(f"✅ {date} {metal} -> inserted")
                else:
                    logger.warning(f"{date} {metal}: No data returned")
            except Exception as e:
                logger.error(f"❌ {date} {metal}: {e}")

if __name__ == "__main__":
    run()