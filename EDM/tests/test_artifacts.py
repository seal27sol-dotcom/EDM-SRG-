import csv
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


class DemoArtifactTests(unittest.TestCase):
    def test_source_and_cleaned_record_volumes(self):
        for name, expected in (
            ("SRG_Customers_demo.csv", 5000),
            ("SRG_Products_demo.csv", 1200),
            ("SRG_Sales_demo.csv", 60000),
            ("SRG_Stores_demo.csv", 23),
        ):
            with (DATA / name).open(encoding="utf-8", newline="") as source:
                self.assertEqual(sum(1 for _ in csv.DictReader(source)), expected, name)
        with (DATA / "cleaned" / "sales.csv").open(encoding="utf-8", newline="") as source:
            self.assertEqual(sum(1 for _ in csv.DictReader(source)), 60000)

    def test_quality_metrics_and_dashboard_use_generated_rows(self):
        metrics = {}
        with (DATA / "quality_before_after.csv").open(encoding="utf-8", newline="") as source:
            for row in csv.DictReader(source):
                metrics[(row["domain"], row["metric"])] = row["after"]
        self.assertEqual(metrics[("customers", "duplicate_rows_pct")], "0.0")
        self.assertEqual(metrics[("products", "duplicate_skus_pct")], "0.0")
        with (DATA / "cleaned" / "customer_crosswalk.csv").open(encoding="utf-8", newline="") as source:
            crosswalk = list(csv.DictReader(source))
        self.assertEqual(len(crosswalk), 5000)
        with (DATA / "cleaned" / "products.csv").open(encoding="utf-8", newline="") as source:
            products = list(csv.DictReader(source))
        self.assertEqual(len(products), 1200)
        self.assertEqual(len({row["SKU"] for row in products}), 1200)
        with (ROOT / "dashboard" / "data" / "srg-demo.json").open(encoding="utf-8") as source:
            dashboard = json.load(source)
        self.assertEqual(dashboard["summary"]["transactions"], 60000)
        self.assertEqual(dashboard["summary"]["customers"], 3869)
        self.assertEqual(len(dashboard["transactions"]), 60000)
        self.assertTrue(all(row[9] in {"Grocery", "Household", "Personal Care", "Beverages", "Electronics", "Fresh Food"} for row in dashboard["transactions"]))
        self.assertIn("Synthetic", dashboard["provenance"])

    def test_sales_customer_ids_resolve_through_mastered_crosswalk(self):
        with (DATA / "cleaned" / "customers.csv").open(encoding="utf-8", newline="") as source:
            mastered = {row["CustomerID"] for row in csv.DictReader(source)}
        with (DATA / "cleaned" / "sales.csv").open(encoding="utf-8", newline="") as source:
            sales = csv.DictReader(source)
            self.assertTrue(all(row["CustomerID"] in mastered for row in sales))

    def test_catalog_csv_rows_have_consistent_columns(self):
        for path, expected_columns in (
            (ROOT / "docs" / "data_dictionary.csv", 8),
            (ROOT / "docs" / "validation_rules.csv", 6),
        ):
            with path.open(encoding="utf-8", newline="") as source:
                rows = list(csv.reader(source))
            self.assertGreaterEqual(len(rows), 13)
            self.assertTrue(all(len(row) == expected_columns for row in rows), path.name)

    def test_hr_analytics_copy_is_masked(self):
        path = DATA / "cleaned" / "SRG_HR_analytics_masked.csv"
        with path.open(encoding="utf-8", newline="") as source:
            rows = list(csv.DictReader(source))
        self.assertEqual(len(rows), 80)
        self.assertNotIn("NationalID", rows[0])
        self.assertNotIn("SalaryUGX", rows[0])
        self.assertTrue(rows[0]["NationalIDMasked"].startswith("*"))


if __name__ == "__main__":
    unittest.main()
