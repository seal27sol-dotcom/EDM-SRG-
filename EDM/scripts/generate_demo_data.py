#!/usr/bin/env python3
"""Generate disclosed, deterministic demonstration data for Project Savanna.

These records are synthetic and are not instructor-provided SRG data.
"""

from __future__ import annotations

import csv
import json
import random
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path
from openpyxl import Workbook

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DASHBOARD_DATA = ROOT / "dashboard" / "data"
SEED = 20261004
random.seed(SEED)

STORES = [
    ("ST01", "Kampala Central", "Kampala"), ("ST02", "Ntinda", "Kampala"),
    ("ST03", "Jinja", "Jinja"), ("ST04", "Mbarara", "Mbarara"),
    ("ST05", "Gulu", "Gulu"), ("ST06", "Entebbe", "Kampala"),
    ("ST07", "Mukono", "Mukono"), ("ST08", "Fort Portal", "Fort Portal"),
    ("ST09", "Mbale", "Mbale"), ("ST10", "Arua", "Arua"),
    ("ST11", "Masaka", "Masaka"), ("ST12", "Lira", "Lira"),
    ("ST13", "Hoima", "Hoima"), ("ST14", "Wakiso", "Wakiso"),
    ("ST15", "Kabalagala", "Kampala"), ("ST16", "Nansana", "Wakiso"),
    ("ST17", "Kasese", "Kasese"), ("ST18", "Soroti", "Soroti"),
    ("ST19", "Iganga", "Iganga"), ("ST20", "Kireka", "Wakiso"),
    ("ST21", "Kabale", "Kabale"), ("ST22", "Kitgum", "Kitgum"),
    ("ST23", "Kampala East", "Kampala"),
]
DISTRICTS = ["Kampala", "Wakiso", "Jinja", "Mbarara", "Gulu", "Mukono", "Mbale", "Arua", "Masaka", "Lira", "Hoima", "Kasese"]
FIRST_NAMES = ["Amina", "John", "Grace", "Peter", "Sarah", "David", "Ruth", "Moses", "Esther", "Paul", "Joan", "Isaac", "Mercy", "Brian", "Hellen"]
LAST_NAMES = ["Kato", "Nakamya", "Okello", "Namuli", "Mugisha", "Achieng", "Ssemanda", "Atim", "Nabirye", "Ouma", "Tumusiime", "Nansubuga"]
CATEGORIES = ["Grocery", "Household", "Personal Care", "Beverages", "Electronics", "Fresh Food"]
PRODUCT_NAMES = ["Rice", "Cooking Oil", "Soap", "Tea", "Sugar", "Milk", "Flour", "Water", "Beans", "Phone Charger", "Toothpaste", "Juice"]


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def make_customers() -> list[dict]:
    base = []
    for index in range(1, 3851):
        first, last = random.choice(FIRST_NAMES), random.choice(LAST_NAMES)
        digits = f"7{random.randint(0, 9)}{random.randint(1000000, 9999999)}"
        phone = random.choice([digits, "+256" + digits, "0" + digits, "+256 " + digits[:3] + " " + digits[3:]])
        registered = date(2023, 1, 1) + timedelta(days=random.randint(0, 1000))
        updated = date(2025, 6, 30) - timedelta(days=random.randint(0, 365))
        base.append({
            "CustomerID": f"C{index:05d}", "FullName": f"{first} {last}",
            "Phone": phone, "Email": f"{first.lower()}.{last.lower()}{index}@example.test",
            "Gender": random.choice(["Female", "F", "female", "Male", "M", "male", "Prefer not to say"]),
            "DateOfBirth": (date(1960, 1, 1) + timedelta(days=random.randint(0, 15000))).strftime(random.choice(["%Y-%m-%d", "%d/%m/%Y", "%m-%d-%Y"])),
            "District": random.choice(DISTRICTS + ["Kampalaa", "Wakiso ", "Unknown"]),
            "RegistrationDate": registered.strftime(random.choice(["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"])),
            "LastUpdatedAt": updated.strftime(random.choice(["%Y-%m-%d", "%d/%m/%Y"])),
            "SourceSystem": random.choice(["POS", "CRM", "LOYALTY", "ECOM"]),
            "LoyaltyAccountID": f"L{index:05d}" if random.random() < 0.7 else "",
        })
    rows = list(base)
    # A deliberate 23% row-level repeat rate, with new source IDs and small variations.
    duplicate_count = round(len(base) * 0.23 / 0.77)
    for offset in range(duplicate_count):
        original = dict(base[offset])
        original["CustomerID"] = f"C{len(base) + offset + 1:05d}"
        original["SourceSystem"] = random.choice(["POS", "CRM", "LOYALTY", "ECOM"])
        if offset % 3 == 0:
            original["FullName"] = original["FullName"].replace(" ", "  ", 1)
        if offset % 4 == 0:
            original["Phone"] = original["Phone"].replace("+256", "0")
        rows.append(original)
    for row in rows:
        if random.random() < 0.07:
            row["Email"] = ""
        if random.random() < 0.05:
            row["Phone"] = ""
        if random.random() < 0.035:
            row["FullName"] = ""
    random.shuffle(rows)
    return rows


def make_products() -> list[dict]:
    rows = []
    for index in range(1, 1201):
        category = random.choice(CATEGORIES)
        if index % 37 == 0:
            category = category + "s"
        unit = random.choice(["kg", "KGS", "Kilograms", "each", "pcs", "litre"])
        updated = date(2025, 6, 30) - timedelta(days=random.randint(0, 540))
        rows.append({
            "ProductID": f"P{index:05d}",
            "SKU": f"SKU-{index - 24:05d}" if index % 20 == 0 else f"SKU-{index:05d}",
            "ProductName": f"{random.choice(PRODUCT_NAMES)} {random.choice(["500g", "1kg", "2L", "Pack", ""])}".strip(),
            "Category": category, "Unit": unit,
            "UnitPrice": round(random.uniform(1500, 85000), 2),
            "SupplierID": f"SUP{random.randint(1, 14):02d}",
            "LastUpdatedAt": updated.strftime(random.choice(["%Y-%m-%d", "%d/%m/%Y"])),
            "SourceSystem": random.choice(["POS", "ECOM", "SUPPLIER"]),
        })
    return rows


def make_sales(customers: list[dict], products: list[dict]) -> list[dict]:
    customer_ids = [row["CustomerID"] for row in customers if row["FullName"]]
    product_ids = [row["ProductID"] for row in products]
    rows = []
    start = date(2025, 1, 1)
    for index in range(1, 60001):
        store_id, store_name, _district = random.choice(STORES)
        sold_on = start + timedelta(days=random.randrange(181))
        channel = random.choices(["POS", "ECOM", "APP"], weights=[0.72, 0.18, 0.10])[0]
        currency = random.choices(["UGX", "UGX ", "UGX.", "KES", "RWF"], weights=[0.84, 0.07, 0.04, 0.03, 0.02])[0]
        quantity = random.randint(1, 6) * (-1 if random.random() < 0.025 else 1)
        unit_price = round(random.uniform(1500, 85000), 2)
        rows.append({
            "TransactionID": f"T{index:07d}",
            "TransactionDate": sold_on.strftime(random.choice(["%Y-%m-%d", "%d/%m/%Y"])),
            "CustomerID": random.choice(customer_ids), "ProductID": random.choice(product_ids),
            "StoreID": store_id if channel == "POS" else ("ONLINE" if channel == "ECOM" else "APP"),
            "StoreName": store_name if channel == "POS" else channel.title(),
            "Channel": channel, "Quantity": quantity,
            "UnitPrice": unit_price, "Currency": currency,
            "PaymentMethod": random.choice(["Cash", "MTN MoMo", "Airtel Money", "Card"]),
            "PaymentReference": "" if random.random() < 0.06 else f"PAY{random.randint(10000000, 99999999)}",
        })
    return rows


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    customers = make_customers()
    products = make_products()
    sales = make_sales(customers, products)
    customer_ids = [row["CustomerID"] for row in customers]
    write_csv(DATA / "SRG_Customers_demo.csv", customers)
    write_csv(DATA / "SRG_Products_demo.csv", products)
    write_csv(DATA / "SRG_Sales_demo.csv", sales)
    write_csv(DATA / "SRG_Suppliers_demo.csv", [
        {"SupplierID": f"SUP{i:02d}", "SupplierName": f"Supplier {i:02d}", "Country": random.choice(["Uganda", "Kenya", "Rwanda"]), "Currency": random.choice(["UGX", "KES", "USD"])}
        for i in range(1, 15)
    ])
    write_csv(DATA / "SRG_Stores_demo.csv", [
        {"StoreID": store_id, "StoreName": store_name, "District": district}
        for store_id, store_name, district in STORES
    ])
    write_csv(DATA / "SRG_Loyalty_demo.csv", [
        {"LoyaltyAccountID": f"L{i:05d}", "CustomerID": random.choice(customer_ids), "PointsBalance": random.randint(0, 25000), "Status": random.choice(["Active", "Inactive"])}
        for i in range(1, 3501)
    ])
    hr_rows = [
        {"EmployeeID": f"E{i:04d}", "FullName": f"Employee {i:03d}", "JobTitle": random.choice(["Store Manager", "Cashier", "IT Analyst", "HR Officer"]), "NationalID": f"CM{i:08d}", "SalaryUGX": random.randint(500000, 8000000), "Phone": f"+2567{random.randint(10000000, 99999999)}"}
        for i in range(1, 81)
    ]
    write_csv(DATA / "SRG_HR_demo.csv", hr_rows)
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Employee Data"
    worksheet.append(list(hr_rows[0]))
    for employee in hr_rows:
        worksheet.append(list(employee.values()))
    workbook.save(DATA / "SRG_HR_demo.xlsx")

    # A deliberately small synthetic error log for diagnosis practice, not the missing instructor log.
    (DATA / "etl_error_log_demo.txt").write_text(
        "2025-06-30 01:02:11 ERROR extract POS_ST03: connection timeout after 30s\n"
        "2025-06-30 01:02:42 WARN extract POS_ST03: retry 1/1 skipped\n"
        "2025-06-30 01:03:01 INFO load fact_sales: 59812 rows committed\n"
        "2025-06-30 01:03:04 ERROR dimension_product: duplicate key SKU-00142\n"
        "2025-06-30 01:03:07 ERROR job status: SUCCESS (partial load)\n",
        encoding="utf-8",
    )
    events = [
        {"event_id": f"F{i:04d}", "store_id": random.choice(STORES)[0], "event_time": f"2025-06-30T{random.randint(8, 20):02d}:{random.randint(0, 59):02d}:00Z", "event_type": random.choice(["entry", "exit"]), "count": 1}
        for i in range(1, 301)
    ]
    (DATA / "footfall_stream_sample_demo.json").write_text(json.dumps(events, indent=2), encoding="utf-8")

    # Dashboard data are aggregated directly from the generated transactions.
    month_sales = defaultdict(float)
    store_sales = defaultdict(float)
    channel_sales = Counter()
    category_sales = defaultdict(float)
    product_by_id = {row["ProductID"]: row for row in products}
    store_district = {row[0]: row[2] for row in STORES}
    transactions = []
    net_sales = 0.0
    for row in sales:
        amount = row["Quantity"] * row["UnitPrice"]
        month = row["TransactionDate"][-7:] if "/" not in row["TransactionDate"] else row["TransactionDate"][3:10]
        if "/" in row["TransactionDate"]:
            day, month_number, year = row["TransactionDate"].split("/")
            month = f"{year}-{month_number}"
        month_sales[month] += amount
        store_sales[row["StoreID"]] += amount
        channel_sales[row["Channel"]] += amount
        category_sales[product_by_id[row["ProductID"]]["Category"]] += amount
        net_sales += amount
        if len(transactions) < 1500:
            transactions.append({
                "date": row["TransactionDate"], "customer": row["CustomerID"], "product": row["ProductID"],
                "store": row["StoreID"], "storeName": row["StoreName"], "channel": row["Channel"],
                "quantity": row["Quantity"], "amount": round(amount, 2),
                "district": store_district.get(row["StoreID"], "Digital"),
                "category": product_by_id[row["ProductID"]]["Category"],
            })
    dashboard = {
        "provenance": "Synthetic demonstration data; not instructor-provided SRG records.",
        "period": "2025-01 to 2025-06", "seed": SEED,
        "summary": {"transactions": len(sales), "customers": len(customers), "products": len(products), "netSales": round(net_sales, 2), "returnRows": sum(1 for row in sales if row["Quantity"] < 0)},
        "monthly": [{"month": key, "sales": round(value, 2)} for key, value in sorted(month_sales.items())],
        "stores": [{"store": key, "sales": round(value, 2)} for key, value in sorted(store_sales.items(), key=lambda item: item[1], reverse=True)],
        "channels": [{"channel": key, "sales": round(value, 2)} for key, value in sorted(channel_sales.items())],
        "categories": [{"category": key, "sales": round(value, 2)} for key, value in sorted(category_sales.items(), key=lambda item: item[1], reverse=True)],
        "transactions": transactions,
        "quality": {"customerRows": len(customers), "customerRowsWithBlankPhone": sum(not row["Phone"] for row in customers), "customerRowsWithBlankEmail": sum(not row["Email"] for row in customers), "productRows": len(products), "negativeQuantityRows": sum(row["Quantity"] < 0 for row in sales), "missingPaymentRefs": sum(not row["PaymentReference"] for row in sales)},
    }
    DASHBOARD_DATA.mkdir(parents=True, exist_ok=True)
    (DASHBOARD_DATA / "srg-demo.json").write_text(json.dumps(dashboard, separators=(",", ":")), encoding="utf-8")
    print(f"Generated {len(customers):,} customers, {len(products):,} products, {len(sales):,} sales; seed={SEED}")


if __name__ == "__main__":
    main()
