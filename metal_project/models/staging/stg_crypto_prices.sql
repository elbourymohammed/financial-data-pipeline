WITH raw_crypto_prices AS (
    SELECT * from {{ source('public', 'raw_crypto_prices') }}
rypto_prices
),

deduplicates AS(
    SELECT *, ROW_NUMBER() OVER(
        PARTITION BY crypto, date, currency
    ) as row_num
    FROM raw_crypto_prices
),

final AS (
    SELECT
        date::TIMESTAMPTZ,
        UPPER(crypto) as crypto_name,
        UPPER(currency) as currency,
        ROUND(price::NUMERIC, 2) as price,
        ingestion_timestamp
    FROM deduplicates
    WHERE row_num = 1
)

select * from final