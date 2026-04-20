import sys
from pathlib import Path
import logging
import os
from dotenv import load_dotenv

load_dotenv()
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, LOG_LEVEL), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from database.Database import Database
from services.fx_rates_service import get_fx_rates
from repositories.fx_rates_repository import insert_fx_data

def run() -> None:
    """Ingest FX rates for yesterday."""
    with Database() as db:
        try:
            data = get_fx_rates()
            insert_fx_data(db, data)
            logger.info(f"✅ FX rates for yesterday inserted")
        except Exception as e:
            logger.error(f"❌ Error inserting FX rates: {e}")

if __name__ == "__main__":
    run()