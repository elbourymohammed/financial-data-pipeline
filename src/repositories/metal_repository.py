def insert_metal(db, data: dict) -> None:
    query = """
        INSERT INTO raw_metal_prices (
            date, metal, exchange, currency, price,
            prev_close_price, change, change_percent,
            price_gram_24k, price_gram_22k, price_gram_21k, price_gram_20k,
            price_gram_18k, price_gram_16k, price_gram_14k, price_gram_10k
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s
        )
    """
    
    db.execute(query, tuple(data.values()))