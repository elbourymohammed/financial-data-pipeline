from database.Database import Database

def creation_table_raw_metal_prices(db: Database):
        
    query:str = """
        CREATE TABLE IF NOT EXISTS raw_metal_prices (
        id SERIAL PRIMARY KEY,
        date TIMESTAMPTZ,
        metal VARCHAR(10),          
        exchange VARCHAR(50),       
        currency VARCHAR(10),       

        price NUMERIC,
        prev_close_price NUMERIC,
        change NUMERIC,             
        change_percent NUMERIC,     

        price_gram_24k NUMERIC,
        price_gram_22k NUMERIC,
        price_gram_21k NUMERIC,
        price_gram_20k NUMERIC,
        price_gram_18k NUMERIC,
        price_gram_16k NUMERIC,
        price_gram_14k NUMERIC,
        price_gram_10k NUMERIC,

        timestamp TIMESTAMP
        );
    """
        
    db.execute(query=query)

def create_table_raw_fx_rates(db: Database):
    query: str = """
    CREATE TABLE IF NOT EXISTS raw_fx_rates (
    id SERIAL PRIMARY KEY,
    date DATE,
    base_currency VARCHAR(10),
    target_currency VARCHAR(10),
    rate NUMERIC,
    ingestion_timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP);
    """
    db.execute(query=query)

def create_table_raw_crypto_prices(db: Database):
    query: str = """
    CREATE TABLE IF NOT EXISTS raw_crypto_prices (
    id SERIAL PRIMARY KEY,
    date TIMESTAMPTZ,
    crypto VARCHAR(20),
    currency VARCHAR(10),
    price NUMERIC,
    ingestion_timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP);
    """
    db.execute(query=query)
    
def create_table_raw_macro_indicators(db: Database):
    query: str = """
    CREATE TABLE IF NOT EXISTS raw_macro_indicators (
    id SERIAL PRIMARY KEY,
    date DATE,
    indicator_name VARCHAR(50),
    value NUMERIC,
    country VARCHAR(50),

    ingestion_timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP);
    """
    db.execute(query=query)

def create_table_raw_market_indices(db: Database):
    query: str = """
    CREATE TABLE IF NOT EXISTS raw_market_indices (
    id SERIAL PRIMARY KEY,
    date DATE,
    index_name VARCHAR(50),
    value NUMERIC,

    ingestion_timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP);
    """
    db.execute(query=query)   

def create_indices(db: Database):
    query:str = """
    CREATE INDEX IF NOT EXISTS idx_fx_date ON raw_fx_rates(date);
    CREATE INDEX IF NOT EXISTS idx_crypto_date ON raw_crypto_prices(date);
    """
    db.execute(query=query)

if __name__ == "__main__":
    db: Database = Database()
    db.connect()
    create_table_raw_crypto_prices(db)
    create_table_raw_fx_rates(db)
    create_table_raw_macro_indicators(db)
    creation_table_raw_metal_prices(db)
    create_indices(db)
    db.disconnect()
