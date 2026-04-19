from datetime import datetime

def insert_macro_indicators(db, observations, indicator_name):
    query = """
        INSERT INTO raw_macro_indicators (
            date, indicator_name, value, country, ingestion_timestamp
        )
        VALUES (%s, %s, %s, %s, %s)
    """

    for obs in observations:
        date_str = obs.get("date")
        value_str = obs.get("value")

        # skip missing values
        if value_str == ".":
            continue

        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        value = float(value_str)

        db.execute(query, (
            date,
            indicator_name,
            value,
            "USA",
            datetime.utcnow()
        ))