-- PostgreSQL core load. Python standardization runs before this warehouse load.
-- Source contract: data/cleaned/sales.csv is canonicalized by scripts/profile_clean.py.
-- Grain: one input transaction line. Unknown currencies are quarantined by the Python job.
-- Run with psql from the repository root. The whole load is atomic.
\set ON_ERROR_STOP on
BEGIN;

CREATE TEMP TABLE stg_customer (
    customerid TEXT, fullname TEXT, phone TEXT, email TEXT, gender TEXT,
    dateofbirth DATE, district TEXT, registrationdate DATE, lastupdatedat DATE,
    sourcesystem TEXT, loyaltyaccountid TEXT
);
CREATE TEMP TABLE stg_customer_crosswalk (
    sourcesystem TEXT, sourcecustomerid TEXT, enterprisecustomerid TEXT,
    matchrule TEXT, matchstatus TEXT
);
CREATE TEMP TABLE stg_product (
    productid TEXT, sku TEXT, productname TEXT, category TEXT, unit TEXT,
    unitprice NUMERIC(14,2), supplierid TEXT, lastupdatedat DATE,
    sourcesystem TEXT, sourcesku TEXT, skustatus TEXT
);
CREATE TEMP TABLE stg_store (storeid TEXT, storename TEXT, district TEXT);

CREATE TEMP TABLE stg_sales_normalized (
    transactionid TEXT, transactiondate DATE, customerid TEXT, productid TEXT,
    storeid TEXT, channel TEXT, quantity NUMERIC(12,3), unitprice NUMERIC(14,2),
    currency CHAR(3), amountugx NUMERIC(16,2), paymentmethod TEXT,
        paymentreference TEXT, paymentreferencemissing BOOLEAN
);

\copy stg_customer FROM 'data/cleaned/customers.csv' WITH (FORMAT csv, HEADER true)
\copy stg_customer_crosswalk FROM 'data/cleaned/customer_crosswalk.csv' WITH (FORMAT csv, HEADER true)
\copy stg_product FROM 'data/cleaned/products.csv' WITH (FORMAT csv, HEADER true)
\copy stg_store FROM 'data/cleaned/stores.csv' WITH (FORMAT csv, HEADER true)
\copy stg_sales_normalized FROM 'data/cleaned/sales.csv' WITH (FORMAT csv, HEADER true)

-- Customer identity is loaded as the current MDM key; source aliases remain in the crosswalk outside this fact model.
INSERT INTO analytics.dim_customer (customer_id, full_name, district, email, phone)
SELECT DISTINCT ON (customerid) customerid, NULLIF(fullname, ''), district,
             NULLIF(email, ''), NULLIF(phone, '')
FROM stg_customer s
WHERE customerid <> ''
    AND NOT EXISTS (SELECT 1 FROM analytics.dim_customer d WHERE d.customer_id = s.customerid AND d.is_current)
ORDER BY customerid, lastupdatedat DESC NULLS LAST;

INSERT INTO analytics.customer_crosswalk
    (source_system, source_customer_id, enterprise_customer_id, match_rule, match_status)
SELECT sourcesystem, sourcecustomerid, enterprisecustomerid, matchrule, matchstatus
FROM stg_customer_crosswalk
ON CONFLICT (source_system, source_customer_id) DO UPDATE
SET enterprise_customer_id = EXCLUDED.enterprise_customer_id,
    match_rule = EXCLUDED.match_rule,
    match_status = EXCLUDED.match_status,
    recorded_at = now();

-- Product SCD Type 2: expire changed versions, then add their new current versions.
UPDATE analytics.dim_product d
SET valid_to = clock_timestamp(), is_current = FALSE
FROM stg_product s
WHERE d.product_id = s.productid AND d.is_current
    AND (d.sku, d.product_name, d.category, d.unit, d.supplier_id)
            IS DISTINCT FROM (s.sku, s.productname, s.category, s.unit, s.supplierid);
INSERT INTO analytics.dim_product (product_id, sku, product_name, category, unit, supplier_id, valid_from)
SELECT DISTINCT ON (s.productid) s.productid, s.sku, s.productname, s.category, s.unit, s.supplierid, clock_timestamp()
FROM stg_product s
WHERE NOT EXISTS (SELECT 1 FROM analytics.dim_product d WHERE d.product_id = s.productid AND d.is_current)
ORDER BY s.productid, s.lastupdatedat DESC NULLS LAST;

INSERT INTO analytics.product_crosswalk
    (source_system, source_product_id, enterprise_product_id, source_sku, sku_status)
SELECT sourcesystem, productid, productid, sourcesku, skustatus
FROM stg_product
ON CONFLICT (source_system, source_product_id) DO UPDATE
SET source_sku = EXCLUDED.source_sku,
    sku_status = EXCLUDED.sku_status,
    recorded_at = now();

-- Store SCD Type 2: preserve location history when the store reference changes.
UPDATE analytics.dim_store d
SET valid_to = clock_timestamp(), is_current = FALSE
FROM stg_store s
WHERE d.store_id = s.storeid AND d.is_current
    AND (d.store_name, d.district) IS DISTINCT FROM (s.storename, s.district);
INSERT INTO analytics.dim_store (store_id, store_name, district, valid_from)
SELECT DISTINCT ON (s.storeid) s.storeid, s.storename, s.district, clock_timestamp()
FROM stg_store s
WHERE NOT EXISTS (SELECT 1 FROM analytics.dim_store d WHERE d.store_id = s.storeid AND d.is_current)
ORDER BY s.storeid;

INSERT INTO analytics.dim_payment (payment_method, provider, currency_code)
SELECT DISTINCT s.paymentmethod,
             CASE WHEN s.paymentmethod ILIKE '%MTN%' THEN 'MTN'
                        WHEN s.paymentmethod ILIKE '%Airtel%' THEN 'Airtel'
                        ELSE s.paymentmethod END,
             s.currency
FROM stg_sales_normalized s
WHERE NOT EXISTS (SELECT 1 FROM analytics.dim_payment d
                                    WHERE d.payment_method = s.paymentmethod AND d.currency_code = s.currency);

INSERT INTO analytics.dim_date (date_key, calendar_date, month_key, month_label, calendar_year, calendar_month)
SELECT DISTINCT to_char(transactiondate, 'YYYYMMDD')::INTEGER,
       transactiondate,
       to_char(transactiondate, 'YYYYMM')::INTEGER,
       to_char(transactiondate, 'Mon YYYY'),
       EXTRACT(YEAR FROM transactiondate)::SMALLINT,
       EXTRACT(MONTH FROM transactiondate)::SMALLINT
FROM stg_sales_normalized
ON CONFLICT (calendar_date) DO NOTHING;

-- Resolve source identifiers to current mastered and slowly-changing dimension rows.
INSERT INTO analytics.fact_sales (
    source_transaction_id, date_key, customer_key, product_key, store_key,
    payment_key, channel, quantity, unit_price, source_currency, amount_ugx,
    payment_reference, source_system
)
SELECT s.transactionid,
       d.date_key,
       c.customer_key,
       p.product_key,
       st.store_key,
       pay.payment_key,
       s.channel,
       s.quantity,
       s.unitprice,
       s.currency,
       s.amountugx,
       NULLIF(s.paymentreference, ''),
    CASE s.channel WHEN 'POS' THEN 'POS' WHEN 'ECOM' THEN 'ECOMMERCE' ELSE 'APP' END
FROM stg_sales_normalized s
JOIN analytics.dim_date d ON d.calendar_date = s.transactiondate
LEFT JOIN analytics.dim_customer c ON c.customer_id = s.customerid AND c.is_current
JOIN analytics.dim_product p ON p.product_id = s.productid AND p.is_current
LEFT JOIN analytics.dim_store st ON st.store_id = s.storeid AND st.is_current
LEFT JOIN analytics.dim_payment pay ON pay.payment_method = s.paymentmethod AND pay.currency_code = s.currency
ON CONFLICT (source_system, source_transaction_id) DO NOTHING;

-- Gate the batch: do not publish if expected rows are absent or lookup failures exceed threshold.
DO $$
DECLARE
    staged_count BIGINT;
    loaded_count BIGINT;
BEGIN
    SELECT COUNT(*) INTO staged_count FROM stg_sales_normalized;
    SELECT COUNT(*) INTO loaded_count
    FROM analytics.fact_sales f
    JOIN stg_sales_normalized s ON s.transactionid = f.source_transaction_id
    WHERE f.source_system = CASE s.channel WHEN 'POS' THEN 'POS' WHEN 'ECOM' THEN 'ECOMMERCE' ELSE 'APP' END;
    IF staged_count = 0 OR loaded_count < staged_count * 0.995 THEN
        RAISE EXCEPTION 'Load quality gate failed: staged %, matched %', staged_count, loaded_count;
    END IF;
END $$;
COMMIT;
