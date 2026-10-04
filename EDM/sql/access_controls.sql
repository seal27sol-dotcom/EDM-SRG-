-- Apply as a PostgreSQL administrator after warehouse.sql.
DO $$ BEGIN
    CREATE ROLE edm_steward NOLOGIN;
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;
DO $$ BEGIN
    CREATE ROLE edm_analyst NOLOGIN;
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

REVOKE ALL ON SCHEMA analytics FROM PUBLIC;
GRANT USAGE ON SCHEMA analytics TO edm_steward, edm_analyst;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA analytics TO edm_steward;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA analytics TO edm_steward;

REVOKE ALL ON analytics.dim_customer FROM PUBLIC, edm_analyst;
REVOKE ALL ON analytics.fact_sales FROM PUBLIC, edm_analyst;
GRANT SELECT (customer_key, customer_id, district, segment, valid_from, valid_to, is_current)
    ON analytics.dim_customer TO edm_analyst;
GRANT SELECT (product_key, product_id, sku, product_name, category, unit,
              valid_from, valid_to, is_current)
    ON analytics.dim_product TO edm_analyst;
GRANT SELECT ON analytics.dim_date, analytics.dim_store, analytics.dim_payment,
    analytics.v_fact_sales_analyst TO edm_analyst;

ALTER DEFAULT PRIVILEGES IN SCHEMA analytics
    REVOKE ALL ON TABLES FROM PUBLIC;
