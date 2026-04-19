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
from services.fx_rates_service import get_fx_rates, generate_dates
from repositories.fx_rates_repository import insert_fx_data

def run(start_date: str = "20251017", nb_days: int = 10) -> None:
    with Database() as db:
        dates = generate_dates(start_date, nb_days)
        for date in dates:
            try:
                data = get_fx_rates(date)
                insert_fx_data(db, data)
                logger.info(f"✅ {date} inserted")
            except Exception as e:
                logger.error(f"❌ {date}: {e}")

if __name__ == "__main__":
    run()