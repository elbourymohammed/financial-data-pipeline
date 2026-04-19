WITH raw_fx_rates AS (
    SELECT * from {{ source('public', 'raw_fx_rates') }}
),

deduplicates AS (
    SELECT *, ROW_NUMBER() OVER(
        PARTITION BY date, base_currency, target_currency
    ) as row_num
    FROM raw_fx_rates
),


final AS (
    SELECT
        date::TIMESTAMPTZ,
        UPPER(base_currency)   as base_currency,
        UPPER(target_currency) as target_currency,
        ROUND(rate::NUMERIC,2) as rate,
        ingestion_timestamp
    FROM deduplicates
    WHERE row_num = 1 AND rate IS NOT NULL
)

SELECT * FROM final