#!/usr/bin/env python3
"""Profile and standardize the disclosed Project Savanna demo data."""

from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CLEAN = DATA / "cleaned"
DASHBOARD_JSON = ROOT / "dashboard" / "data" / "srg-demo.json"
AS_OF = date(2025, 6, 30)
DISTRICT_MAP = {"kampalaa": "Kampala", "kampala": "Kampala", "wakiso": "Wakiso"}
GENDER_MAP = {"f": "Female", "female": "Female", "m": "Male", "male": "Male", "prefer not to say": "Prefer not to say"}
FX_TO_UGX = {"UGX": 1.0, "KES": 28.5, "RWF": 2.85}
SOURCE_PRIORITY = {"LOYALTY": 0, "CRM": 1, "ECOM": 2, "POS": 3}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if rows:
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)


def normalized_phone(value: str) -> str:
    digits = re.sub(r"\D", "", value or "")
    if digits.startswith("256"):
        digits = digits[3:]
    elif digits.startswith("0"):
        digits = digits[1:]
    return "+256" + digits if len(digits) == 9 else ""


def parse_date(value: str) -> str:
    for pattern in ("%Y-%m-%d", "%d/%m/%Y", "%m-%d-%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(value, pattern).date().isoformat()
        except ValueError:
            pass
    return ""


def person_key(row: dict[str, str]) -> tuple[str, str]:
    email = (row.get("Email") or "").strip().lower()
    phone = normalized_phone(row.get("Phone", ""))
    name = re.sub(r"\s+", " ", (row.get("FullName") or "").strip().lower())
    return ("email", email) if email else (("name_phone", f"{name}|{phone}") if name and phone else ("id", row["CustomerID"]))


def person_keys(row: dict[str, str]) -> list[tuple[str, str]]:
    email = (row.get("Email") or "").strip().lower()
    phone = normalized_phone(row.get("Phone", ""))
    name = re.sub(r"\s+", " ", (row.get("FullName") or "").strip().lower())
    keys = []
    if email:
        keys.append(("email", email))
    if name and phone:
        keys.append(("name_phone", f"{name}|{phone}"))
    return keys or [("id", row["CustomerID"])]


def customer_metrics(rows: list[dict[str, str]]) -> dict[str, float]:
    seen = set()
    duplicates = 0
    valid_districts = {"Kampala", "Wakiso", "Jinja", "Mbarara", "Gulu", "Mukono", "Mbale", "Arua", "Masaka", "Lira", "Hoima", "Kasese"}
    valid_rows = 0
    canonical_rows = 0
    complete_rows = 0
    timely_rows = 0
    for row in rows:
        keys = person_keys(row)
        if any(key in seen for key in keys):
            duplicates += 1
        seen.update(keys)
        raw_phone = row.get("Phone", "").strip()
        phone_ok = not raw_phone or bool(re.fullmatch(r"\+256\d{9}", raw_phone))
        date_value = parse_date(row.get("RegistrationDate", ""))
        updated = parse_date(row.get("LastUpdatedAt", ""))
        raw_district = row.get("District", "")
        district = DISTRICT_MAP.get(raw_district.strip().lower(), raw_district.strip())
        gender_ok = not row.get("Gender") or row["Gender"] in {"Female", "Male", "Prefer not to say"}
        valid = phone_ok and raw_district == district and district in valid_districts and gender_ok and bool(date_value)
        valid_rows += valid
        canonical_rows += bool((not row.get("Phone") or row["Phone"] == normalized_phone(row["Phone"])) and row.get("Gender") in {"Female", "Male", "Prefer not to say"} and row.get("District") == district and row.get("RegistrationDate") == date_value and row.get("LastUpdatedAt") == updated)
        complete_rows += bool(row.get("FullName", "").strip() and (row.get("Phone", "").strip() or row.get("Email", "").strip()) and date_value)
        timely_rows += bool(updated and (AS_OF - date.fromisoformat(updated)).days <= 90)
    count = max(1, len(rows))
    return {
        "rows": len(rows), "duplicate_rows_pct": round(duplicates / count * 100, 2),
        "completeness_pct": round(complete_rows / count * 100, 2),
        "consistency_pct": round(canonical_rows / count * 100, 2),
        "timeliness_pct": round(timely_rows / count * 100, 2),
        "validity_pct": round(valid_rows / count * 100, 2),
        "uniqueness_pct": round((count - duplicates) / count * 100, 2),
        "accuracy_proxy_pct": round(valid_rows / count * 100, 2),
        "missing_phone_pct": round(sum(not r.get("Phone", "").strip() for r in rows) / count * 100, 2),
        "missing_email_pct": round(sum(not r.get("Email", "").strip() for r in rows) / count * 100, 2),
        "invalid_district_rows": sum(r.get("District", "").strip() not in valid_districts for r in rows),
        "phone_plus256_rows": sum(r.get("Phone", "").strip().startswith("+256") for r in rows),
        "phone_local_zero_rows": sum(r.get("Phone", "").strip().startswith("0") for r in rows),
        "phone_unprefixed_rows": sum(bool(r.get("Phone", "").strip()) and not r["Phone"].strip().startswith(("+256", "0")) for r in rows),
        "registration_date_iso_rows": sum(bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", r.get("RegistrationDate", ""))) for r in rows),
        "registration_date_slash_rows": sum("/" in r.get("RegistrationDate", "") for r in rows),
        "registration_date_dash_non_iso_rows": sum("-" in r.get("RegistrationDate", "") and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", r.get("RegistrationDate", "")) for r in rows),
    }


def clean_customers(rows: list[dict[str, str]]) -> tuple[list[dict], list[dict]]:
    best_by_person = {}
    alias_to_group = {}
    source_to_group = {}
    for row in rows:
        keys = person_keys(row)
        key = next((alias_to_group[item] for item in keys if item in alias_to_group), keys[0])
        for item in keys:
            alias_to_group[item] = key
        source_to_group[row["CustomerID"]] = key
        cleaned = {
            **row,
            "FullName": re.sub(r"\s+", " ", (row.get("FullName") or "").strip()),
            "Phone": normalized_phone(row.get("Phone", "")),
            "Email": (row.get("Email") or "").strip().lower(),
            "Gender": GENDER_MAP.get((row.get("Gender") or "").strip().lower(), "Unknown"),
            "DateOfBirth": parse_date(row.get("DateOfBirth", "")),
            "RegistrationDate": parse_date(row.get("RegistrationDate", "")),
            "LastUpdatedAt": parse_date(row.get("LastUpdatedAt", "")),
            "District": DISTRICT_MAP.get((row.get("District") or "").strip().lower(), (row.get("District") or "").strip()),
        }
        completeness = sum(bool(cleaned.get(field)) for field in ("FullName", "Phone", "Email", "DateOfBirth", "District"))
        rank = (completeness, -SOURCE_PRIORITY.get(row.get("SourceSystem", ""), 99), row["CustomerID"])
        if key not in best_by_person or rank > best_by_person[key][0]:
            best_by_person[key] = (rank, cleaned)
    mastered = [item[1] for item in best_by_person.values()]
    group_to_master = {group: value[1]["CustomerID"] for group, value in best_by_person.items()}
    crosswalk = [
        {"SourceSystem": row["SourceSystem"], "SourceCustomerID": row["CustomerID"],
         "EnterpriseCustomerID": group_to_master[source_to_group[row["CustomerID"]]],
         "MatchRule": source_to_group[row["CustomerID"]][0],
         "MatchStatus": "GOLDEN" if row["CustomerID"] == group_to_master[source_to_group[row["CustomerID"]]] else "EXACT_MATCH_ALIAS"}
        for row in rows
    ]
    return mastered, crosswalk


def product_metrics(rows: list[dict[str, str]]) -> dict[str, float]:
    skus = [row.get("SKU", "").strip().upper() for row in rows]
    duplicates = len(skus) - len(set(skus))
    canonical_units = {"kg": "kg", "kgs": "kg", "kilograms": "kg", "each": "each", "pcs": "each", "litre": "litre"}
    canonical_categories = {"grocery", "household", "personal care", "beverages", "electronics", "fresh food"}
    category_aliases = {"grocerys": "grocery", "households": "household", "personal cares": "personal care", "beveragess": "beverages", "electronicss": "electronics", "fresh foods": "fresh food"}
    valid = sum(row.get("Unit", "").strip().lower() in {"kg", "each", "litre"} and row.get("Category", "").strip().lower() in canonical_categories and float(row.get("UnitPrice", 0) or 0) > 0 for row in rows)
    complete = sum(all(row.get(field, "").strip() for field in ("SKU", "ProductName", "Category", "Unit", "UnitPrice", "SupplierID")) for row in rows)
    consistent = sum(row.get("SKU", "").strip() == row.get("SKU", "").strip().upper() and row.get("Unit", "").strip().lower() in {"kg", "each", "litre"} and row.get("Category", "").strip().lower() in canonical_categories for row in rows)
    timely = sum(bool((updated := parse_date(row.get("LastUpdatedAt", ""))) and (AS_OF - date.fromisoformat(updated)).days <= 90) for row in rows)
    return {
        "rows": len(rows), "duplicate_skus_pct": round(duplicates / max(1, len(rows)) * 100, 2),
        "validity_pct": round(valid / max(1, len(rows)) * 100, 2),
        "uniqueness_pct": round((len(rows) - duplicates) / max(1, len(rows)) * 100, 2),
        "completeness_pct": round(complete / max(1, len(rows)) * 100, 2),
        "consistency_pct": round(consistent / max(1, len(rows)) * 100, 2),
        "timeliness_pct": round(timely / max(1, len(rows)) * 100, 2),
        "accuracy_proxy_pct": round(sum(float(row.get("UnitPrice", 0) or 0) > 0 and bool(re.fullmatch(r"SUP\d{2}", row.get("SupplierID", ""))) for row in rows) / max(1, len(rows)) * 100, 2),
    }


def clean_products(rows: list[dict[str, str]]) -> list[dict]:
    units = {"kg": "kg", "kgs": "kg", "kilograms": "kg", "each": "each", "pcs": "each", "litre": "litre"}
    categories = {"grocerys": "Grocery", "households": "Household", "personal cares": "Personal Care", "beveragess": "Beverages", "electronicss": "Electronics", "fresh foods": "Fresh Food"}
    sku_counts = Counter(row.get("SKU", "").strip().upper() for row in rows)
    cleaned_rows = []
    for row in rows:
        source_sku = row.get("SKU", "").strip().upper()
        has_collision = sku_counts[source_sku] > 1
        cleaned_rows.append({
            **row,
            "SKU": f"SRG-{row['ProductID']}" if has_collision else source_sku,
            "SourceSKU": source_sku,
            "SKUStatus": "REVIEW_DUPLICATE_SOURCE_SKU" if has_collision else "SOURCE_UNIQUE",
            "Unit": units.get(row.get("Unit", "").strip().lower(), "Unknown"),
            "Category": categories.get(row.get("Category", "").strip().lower(), row.get("Category", "").strip()),
            "LastUpdatedAt": parse_date(row.get("LastUpdatedAt", "")),
        })
    return cleaned_rows


def main() -> None:
    customers = read_csv(DATA / "SRG_Customers_demo.csv")
    products = read_csv(DATA / "SRG_Products_demo.csv")
    sales = read_csv(DATA / "SRG_Sales_demo.csv")
    stores = read_csv(DATA / "SRG_Stores_demo.csv")
    customer_before = customer_metrics(customers)
    product_before = product_metrics(products)
    clean_customer_rows, customer_crosswalk = clean_customers(customers)
    clean_product_rows = clean_products(products)
    customer_after = customer_metrics(clean_customer_rows)
    product_after = product_metrics(clean_product_rows)
    write_csv(CLEAN / "customers.csv", clean_customer_rows)
    write_csv(CLEAN / "customer_crosswalk.csv", customer_crosswalk)
    write_csv(CLEAN / "products.csv", clean_product_rows)
    write_csv(CLEAN / "stores.csv", [
        {"StoreID": row["StoreID"].strip().upper(), "StoreName": row["StoreName"].strip(), "District": row["District"].strip()}
        for row in stores
    ])

    metric_rows = []
    for domain, before, after in (("customers", customer_before, customer_after), ("products", product_before, product_after)):
        for metric in sorted(set(before) | set(after)):
            metric_rows.append({"domain": domain, "metric": metric, "before": before.get(metric, ""), "after": after.get(metric, "")})
    write_csv(DATA / "quality_before_after.csv", metric_rows)

    store_lookup = {row[0]: (row[1], row[2]) for row in [
        ("ST01", "Kampala Central", "Kampala"), ("ST02", "Ntinda", "Kampala"), ("ST03", "Jinja", "Jinja"),
        ("ST04", "Mbarara", "Mbarara"), ("ST05", "Gulu", "Gulu"), ("ST06", "Entebbe", "Kampala"),
        ("ST07", "Mukono", "Mukono"), ("ST08", "Fort Portal", "Fort Portal"), ("ST09", "Mbale", "Mbale"),
        ("ST10", "Arua", "Arua"), ("ST11", "Masaka", "Masaka"), ("ST12", "Lira", "Lira"),
        ("ST13", "Hoima", "Hoima"), ("ST14", "Wakiso", "Wakiso"), ("ST15", "Kabalagala", "Kampala"),
        ("ST16", "Nansana", "Wakiso"), ("ST17", "Kasese", "Kasese"), ("ST18", "Soroti", "Soroti"),
        ("ST19", "Iganga", "Iganga"), ("ST20", "Kireka", "Wakiso"), ("ST21", "Kabale", "Kabale"),
        ("ST22", "Kitgum", "Kitgum"), ("ST23", "Kampala East", "Kampala"),
    ]}
    product_by_id = {row["ProductID"]: row for row in clean_product_rows}
    customer_map = {row["SourceCustomerID"]: row["EnterpriseCustomerID"] for row in customer_crosswalk}
    monthly, stores, channels, categories = defaultdict(float), defaultdict(float), defaultdict(float), defaultdict(float)
    dashboard_rows = []
    active_customer_ids = set()
    clean_sales = []
    rejected_sales = []
    net_sales_ugx = 0.0
    return_rows = 0
    for row in sales:
        currency = row["Currency"].strip().rstrip(".").upper()
        fx = FX_TO_UGX.get(currency)
        if fx is None:
            rejected_sales.append({**row, "RejectReason": "unsupported currency"})
            continue
        raw_date = row["TransactionDate"]
        canonical_date = parse_date(raw_date)
        if not canonical_date:
            continue
        amount = float(row["Quantity"]) * float(row["UnitPrice"]) * fx
        enterprise_customer_id = customer_map.get(row["CustomerID"], row["CustomerID"])
        active_customer_ids.add(enterprise_customer_id)
        month = canonical_date[:7]
        monthly[month] += amount
        stores[row["StoreID"]] += amount
        channels[row["Channel"]] += amount
        category = product_by_id[row["ProductID"]]["Category"]
        categories[category] += amount
        net_sales_ugx += amount
        return_rows += int(int(row["Quantity"]) < 0)
        store_name, district = store_lookup.get(row["StoreID"], (row["StoreName"], "Digital"))
        dashboard_rows.append([canonical_date, enterprise_customer_id, row["ProductID"], row["StoreID"], store_name, row["Channel"], int(row["Quantity"]), round(amount, 2), district, category])
        clean_sales.append({
            "TransactionID": row["TransactionID"], "TransactionDate": canonical_date,
            "CustomerID": enterprise_customer_id, "ProductID": row["ProductID"],
            "StoreID": row["StoreID"], "Channel": row["Channel"],
            "Quantity": int(row["Quantity"]), "UnitPrice": round(float(row["UnitPrice"]), 2),
            "Currency": currency, "AmountUGX": round(amount, 2),
            "PaymentMethod": row["PaymentMethod"], "PaymentReference": row["PaymentReference"],
            "PaymentReferenceMissing": not bool(row["PaymentReference"]),
        })
    write_csv(CLEAN / "sales.csv", clean_sales)
    write_csv(DATA / "sales_rejected_demo.csv", rejected_sales)
    summary = {
        "transactions": len(clean_sales), "customers": len(clean_customer_rows), "rawCustomerRows": len(customers), "products": len(products),
        "activeCustomers": len(active_customer_ids),
        "netSalesUGX": round(net_sales_ugx, 2), "returnRows": return_rows,
        "fxAssumptionsUGX": FX_TO_UGX,
    }
    payload = {
        "provenance": "Synthetic demonstration data generated from the assignment scenario; not instructor-provided SRG records.",
        "period": "2025-01 to 2025-06", "seed": 20261004, "summary": summary,
        "monthly": [{"month": k, "sales": round(v, 2)} for k, v in sorted(monthly.items())],
        "stores": [{"store": k, "sales": round(v, 2)} for k, v in sorted(stores.items(), key=lambda x: x[1], reverse=True)],
        "channels": [{"channel": k, "sales": round(v, 2)} for k, v in sorted(channels.items())],
        "categories": [{"category": k, "sales": round(v, 2)} for k, v in sorted(categories.items(), key=lambda x: x[1], reverse=True)],
        "transactions": dashboard_rows,
        "quality": {"customerBefore": customer_before, "customerAfter": customer_after, "productBefore": product_before, "productAfter": product_after},
    }
    DASHBOARD_JSON.parent.mkdir(parents=True, exist_ok=True)
    DASHBOARD_JSON.write_text(json.dumps(payload, separators=(",", ":")), encoding="utf-8")
    print(f"Profiled {len(customers):,} customers and {len(products):,} products; dashboard includes {len(dashboard_rows):,} transactions.")


if __name__ == "__main__":
    main()
