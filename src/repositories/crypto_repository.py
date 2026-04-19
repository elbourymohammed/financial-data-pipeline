from datetime import datetime

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