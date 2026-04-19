from datetime import datetime


def insert_fx_data(db, data):
    base = data.get("base")
    rates = data.get("rates", {})
    timestamp = data.get("date")

    ingestion_time = datetime.utcnow()

    query = """
        INSERT INTO raw_fx_rates (
            date,
            base_currency,
            target_currency,
            rate,
            ingestion_timestamp
        )
        VALUES (%s, %s, %s, %s, %s)
    """

    for currency, rate in rates.items():
        db.execute(query, (
            timestamp,
            base,
            currency,
            rate,
            ingestion_time
        ))
