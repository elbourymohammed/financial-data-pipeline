WITH raw_metal_prices AS (
    SELECT * FROM {{ source('public', 'raw_metal_prices') }}
),

metal_prices AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY date, metal, currency
            ORDER BY id
        ) AS row_num
    FROM raw_metal_prices
),

final_without_replacement_metals_name AS (
    SELECT
        date::TIMESTAMPTZ                   AS date,
        UPPER(metal)                        AS metal,
        UPPER(exchange)                     AS exchange,
        UPPER(currency)                     AS currency,
        ROUND(price::NUMERIC, 2)            AS price,
        ROUND(prev_close_price::NUMERIC, 2) AS prev_close_price,
        ROUND(price_gram_24k::NUMERIC, 2)   AS price_gram_24k,
        ROUND(price_gram_22k::NUMERIC, 2)   AS price_gram_22k,
        ROUND(price_gram_21k::NUMERIC, 2)   AS price_gram_21k,
        ROUND(price_gram_20k::NUMERIC, 2)   AS price_gram_20k,
        ROUND(price_gram_18k::NUMERIC, 2)   AS price_gram_18k,
        ROUND(price_gram_16k::NUMERIC, 2)   AS price_gram_16k,
        ROUND(price_gram_14k::NUMERIC, 2)   AS price_gram_14k,
        ROUND(price_gram_10k::NUMERIC, 2)   AS price_gram_10k,
        ROUND((price - LAG(price::NUMERIC) OVER (
            PARTITION BY metal ORDER BY date
        ))::NUMERIC, 4)                     AS change,
        ROUND(((price - LAG(price::NUMERIC) OVER (
            PARTITION BY metal ORDER BY date
        )) / LAG(price::NUMERIC) OVER (
            PARTITION BY metal ORDER BY date
        ) * 100)::NUMERIC, 4)              AS change_percent
    FROM metal_prices
    WHERE row_num = 1 AND price IS NOT NULL AND prev_close_price IS NOT NULL
),

final AS (
    SELECT
        date,
        REPLACE(REPLACE(REPLACE(metal,'XAU', 'GOLD'),'XAG', 'SILVER'), 'XPT', 'PLATINIUM') as metal,
        exchange,
        currency,
        price,
        prev_close_price,
        change,
        change_percent,
        price_gram_24k,
        price_gram_22k,
        price_gram_21k,
        price_gram_20k,
        price_gram_18k,
        price_gram_16k,
        price_gram_14k,
        price_gram_10k
    FROM final_without_replacement_metals_name

)

SELECT * FROM final