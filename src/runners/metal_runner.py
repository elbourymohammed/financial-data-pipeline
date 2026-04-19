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
from services.metal_services import fetch_metal_price, generate_dates
from repositories.metal_repository import insert_metal

def run(start_date: str = "20251017", nb_days: int = 10) -> None:
    with Database() as db:
        dates = generate_dates(start_date, nb_days)
        metals = ['XAU', 'XAG', 'XPT', 'XPD']
        for date in dates:
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