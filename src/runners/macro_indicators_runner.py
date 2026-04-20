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
from services.macro_indicators_services import get_fred_data, FRED_SERIES
from repositories.macro_indicators_repository import insert_macro_indicators

def run() -> None:
    with Database() as db:
        total_inserted = 0
        for name, series_id in FRED_SERIES.items():
            try:
                observations = get_fred_data(series_id)
                insert_macro_indicators(db, observations, name)
                valid_count = len([obs for obs in observations if obs.get('value') != '.'])
                total_inserted += valid_count
                logger.info(f"{name} -> {valid_count} inserted")
            except Exception as e:
                logger.error(f"{name}: {e}")
        logger.info(f"✅ Total data ingested: {total_inserted}")

if __name__ == "__main__":
    run()