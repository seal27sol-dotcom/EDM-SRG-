-- Run with psql as a database administrator after access_controls.sql.
\set ON_ERROR_STOP on

SET ROLE edm_analyst;
SELECT customer_id, district FROM analytics.dim_customer LIMIT 1;
SELECT sales_key, amount_ugx FROM analytics.v_fact_sales_analyst LIMIT 1;

DO $$ BEGIN
    PERFORM email FROM analytics.dim_customer LIMIT 1;
    RAISE EXCEPTION 'FAIL: analyst unexpectedly read customer email';
EXCEPTION WHEN insufficient_privilege THEN
    RAISE NOTICE 'PASS: analyst cannot read customer email';
END $$;

DO $$ BEGIN
    PERFORM payment_reference FROM analytics.fact_sales LIMIT 1;
    RAISE EXCEPTION 'FAIL: analyst unexpectedly read payment reference';
EXCEPTION WHEN insufficient_privilege THEN
    RAISE NOTICE 'PASS: analyst cannot read payment reference';
END $$;
RESET ROLE;
