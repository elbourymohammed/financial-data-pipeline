WITH raw_macro_indicators AS (
    SELECT * from {{ source('public', 'raw_macro_indicators') }}
),

deduplicates AS (
    SELECT *, ROW_NUMBER() OVER(
        PARTITION BY date, indicator_name, value
    ) as row_num
    FROM raw_macro_indicators
),

macro_indicators_cleaned AS (
    SELECT
        date::TIMESTAMPTZ,
        UPPER(indicator_name) as indicator_name,
        ROUND(value::NUMERIC, 2) as value,
        UPPER(country) as country,
        ingestion_timestamp
    FROM deduplicates
    WHERE row_num = 1 AND date IS NOT NULL AND 
    indicator_name IS NOT NULL AND 
    value is NOT NULL
),

final AS (
    SELECT 
        date,
        REPLACE(REPLACE(indicator_name,'CPI', 'INFLATION'), 'GDP', 'TOTAL PRODUCTION VALUE') AS indicator_name,
        value, country, ingestion_timestamp
    FROM macro_indicators_cleaned
)

select * from final

