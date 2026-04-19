WITH metals AS (
    SELECT
        date,
        metal,
        price as metal_price,
        change as metal_change,
        change_percent as metal_change_pct,
        price_gram_24k,
        price_gram_18k,
        price_gram_14k
    FROM {{ ref('stg_metal_prices') }}
),

crypto AS (
    SELECT
        date,
        crypto_name,
        price as crypto_price
    FROM {{ ref('stg_crypto_prices') }}
),

fx AS (
    SELECT
        date,
        target_currency,
        rate AS fx_rate
    FROM {{ ref('stg_fx_rates') }}
),

macro AS (
    SELECT
        date,
        indicator_name,
        value as macro_value
    FROM {{ ref('stg_macro_indicators') }}
),

crypto_pivot AS (
    SELECT
        date,
        MAX(CASE WHEN crypto_name = 'BITCOIN' THEN crypto_price END) AS btc_price
    FROM crypto
    GROUP BY date
),

fx_pivot AS (
    SELECT
        date,
        MAX(CASE WHEN target_currency = 'EUR' THEN fx_rate END) AS usd_eur,
        MAX(CASE WHEN target_currency = 'GBP' THEN fx_rate END) AS usd_gbp,
        MAX(CASE WHEN target_currency = 'JPY' THEN fx_rate END) AS usd_jpy,
        MAX(CASE WHEN target_currency = 'CHF' THEN fx_rate END) AS usd_chf
    FROM fx
    GROUP BY date
),

macro_pivot AS (
    SELECT
        m_dates.date,
        MAX(CASE WHEN indicator_name = 'UNEMPLOYMENT'
            THEN macro_value END)              AS unemployment,
        MAX(CASE WHEN indicator_name = 'INFLATION'
            THEN macro_value END)              AS inflation,
        MAX(CASE WHEN indicator_name = 'TOTAL PRODUCTION VALUE'
            THEN macro_value END)              AS total_production_value
    FROM (
        SELECT DISTINCT date::DATE AS date FROM metals
    ) m_dates
    LEFT JOIN macro m
        ON m.date::DATE = (
            SELECT MAX(date::DATE)
            FROM macro m2
            WHERE m2.indicator_name = m.indicator_name
            AND m2.date::DATE <= m_dates.date
        )
    GROUP BY m_dates.date
),
final AS (
    SELECT
        m.date,
        m.metal,

        -- métaux
        m.metal_price,
        m.metal_change,
        m.metal_change_pct,
        m.price_gram_24k,
        m.price_gram_18k,
        m.price_gram_14k,

        -- crypto
        c.btc_price,

        -- taux de change
        f.usd_eur,
        f.usd_gbp,
        f.usd_jpy,
        f.usd_chf,

        -- macro
        mp.unemployment,
        mp.inflation,
        mp.total_production_value

    FROM metals m
    LEFT JOIN crypto_pivot  c   ON m.date::DATE  = c.date::DATE
    LEFT JOIN fx_pivot       f  ON m.date::DATE = f.date::DATE
    LEFT JOIN macro_pivot    mp ON m.date::DATE = mp.date::DATE
)

SELECT * FROM final
ORDER BY metal, date