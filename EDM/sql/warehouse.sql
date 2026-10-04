-- PostgreSQL star schema; fact grain: one source transaction line.
CREATE SCHEMA IF NOT EXISTS analytics;

CREATE TABLE IF NOT EXISTS analytics.dim_date (
    date_key INTEGER PRIMARY KEY,
    calendar_date DATE NOT NULL UNIQUE,
    month_key INTEGER NOT NULL,
    month_label TEXT NOT NULL,
    calendar_year SMALLINT NOT NULL,
    calendar_month SMALLINT NOT NULL
);

CREATE TABLE IF NOT EXISTS analytics.dim_customer (
    customer_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id TEXT NOT NULL,
    full_name TEXT,
    district TEXT,
    segment TEXT,
    email TEXT,
    phone TEXT,
    valid_from TIMESTAMPTZ NOT NULL DEFAULT now(),
    valid_to TIMESTAMPTZ,
    is_current BOOLEAN NOT NULL DEFAULT TRUE,
    UNIQUE (customer_id, valid_from),
    CHECK (valid_to IS NULL OR valid_to > valid_from)
);

CREATE TABLE IF NOT EXISTS analytics.customer_crosswalk (
    source_system TEXT NOT NULL,
    source_customer_id TEXT NOT NULL,
    enterprise_customer_id TEXT NOT NULL,
    match_rule TEXT NOT NULL,
    match_status TEXT NOT NULL,
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (source_system, source_customer_id)
);

CREATE TABLE IF NOT EXISTS analytics.dim_product (
    product_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id TEXT NOT NULL,
    sku TEXT NOT NULL,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    unit TEXT NOT NULL,
    supplier_id TEXT,
    valid_from TIMESTAMPTZ NOT NULL DEFAULT now(),
    valid_to TIMESTAMPTZ,
    is_current BOOLEAN NOT NULL DEFAULT TRUE,
    UNIQUE (product_id, valid_from),
    CHECK (valid_to IS NULL OR valid_to > valid_from)
);

CREATE TABLE IF NOT EXISTS analytics.product_crosswalk (
    source_system TEXT NOT NULL,
    source_product_id TEXT NOT NULL,
    enterprise_product_id TEXT NOT NULL,
    source_sku TEXT NOT NULL,
    sku_status TEXT NOT NULL,
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (source_system, source_product_id)
);

CREATE TABLE IF NOT EXISTS analytics.dim_store (
    store_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    store_id TEXT NOT NULL,
    store_name TEXT NOT NULL,
    district TEXT NOT NULL,
    valid_from TIMESTAMPTZ NOT NULL DEFAULT now(),
    valid_to TIMESTAMPTZ,
    is_current BOOLEAN NOT NULL DEFAULT TRUE,
    UNIQUE (store_id, valid_from),
    CHECK (valid_to IS NULL OR valid_to > valid_from)
);

CREATE TABLE IF NOT EXISTS analytics.dim_payment (
    payment_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    payment_method TEXT NOT NULL,
    provider TEXT,
    currency_code CHAR(3) NOT NULL
);

CREATE TABLE IF NOT EXISTS analytics.fact_sales (
    sales_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source_transaction_id TEXT NOT NULL,
    date_key INTEGER NOT NULL REFERENCES analytics.dim_date(date_key),
    customer_key BIGINT REFERENCES analytics.dim_customer(customer_key),
    product_key BIGINT NOT NULL REFERENCES analytics.dim_product(product_key),
    store_key BIGINT REFERENCES analytics.dim_store(store_key),
    payment_key BIGINT REFERENCES analytics.dim_payment(payment_key),
    channel TEXT NOT NULL,
    quantity NUMERIC(12, 3) NOT NULL,
    unit_price NUMERIC(14, 2) NOT NULL,
    source_currency CHAR(3) NOT NULL,
    amount_ugx NUMERIC(16, 2) NOT NULL,
    payment_reference TEXT,
    source_system TEXT NOT NULL,
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (source_system, source_transaction_id)
);

CREATE INDEX IF NOT EXISTS ix_fact_sales_date ON analytics.fact_sales(date_key);
CREATE INDEX IF NOT EXISTS ix_fact_sales_customer ON analytics.fact_sales(customer_key);
CREATE INDEX IF NOT EXISTS ix_fact_sales_product ON analytics.fact_sales(product_key);
CREATE INDEX IF NOT EXISTS ix_fact_sales_store ON analytics.fact_sales(store_key);
CREATE UNIQUE INDEX IF NOT EXISTS ux_dim_customer_current_id
    ON analytics.dim_customer(customer_id) WHERE is_current;
CREATE UNIQUE INDEX IF NOT EXISTS ux_dim_store_current_id
    ON analytics.dim_store(store_id) WHERE is_current;
CREATE UNIQUE INDEX IF NOT EXISTS ux_dim_product_current_sku
    ON analytics.dim_product(sku) WHERE is_current;
CREATE UNIQUE INDEX IF NOT EXISTS ux_dim_payment_method_currency
    ON analytics.dim_payment(payment_method, currency_code);

CREATE OR REPLACE VIEW analytics.v_fact_sales_analyst AS
SELECT sales_key, date_key, customer_key, product_key, store_key, payment_key,
       channel, quantity, unit_price, source_currency, amount_ugx, source_system, loaded_at
FROM analytics.fact_sales;
