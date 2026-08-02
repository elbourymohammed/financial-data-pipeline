-- Initialize database for Data Project
-- This script runs when PostgreSQL container starts

-- Create extensions if they don't exist
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create schemas
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS marts;

-- Create raw ingestion tables
CREATE TABLE IF NOT EXISTS public.raw_crypto_prices (
    date date,
    crypto text,
    currency text,
    price numeric,
    ingestion_timestamp timestamp with time zone
);

CREATE TABLE IF NOT EXISTS public.raw_fx_rates (
    date date,
    base_currency text,
    target_currency text,
    rate numeric,
    ingestion_timestamp timestamp with time zone
);

CREATE TABLE IF NOT EXISTS public.raw_macro_indicators (
    date date,
    indicator_name text,
    value numeric,
    country text,
    ingestion_timestamp timestamp with time zone
);

CREATE TABLE IF NOT EXISTS public.raw_metal_prices (
    date date,
    metal text,
    exchange text,
    currency text,
    price numeric,
    prev_close_price numeric,
    change numeric,
    change_percent numeric,
    price_gram_24k numeric,
    price_gram_22k numeric,
    price_gram_21k numeric,
    price_gram_20k numeric,
    price_gram_18k numeric,
    price_gram_16k numeric,
    price_gram_14k numeric,
    price_gram_10k numeric
);
