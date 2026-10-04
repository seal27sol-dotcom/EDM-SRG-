from __future__ import annotations

import csv
from pathlib import Path


def normalize_date(value: str) -> str:
    value = (value or '').strip()
    if not value:
        return ''
    for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%m/%d/%Y', '%m-%d-%Y', '%d.%m.%Y'):
        try:
            from datetime import datetime
            return datetime.strptime(value, fmt).strftime('%Y-%m-%d')
        except ValueError:
            continue
    return value


def main() -> None:
    base = Path(__file__).resolve().parents[1]
    data_dir = base / 'data'

    products = {}
    with (data_dir / 'SRG_Products_demo.csv').open('r', newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            products[row['ProductID']] = row

    stores = {}
    with (data_dir / 'SRG_Stores_demo.csv').open('r', newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            stores[row['StoreID']] = row

    output_path = data_dir / 'BI_dashboard_dataset.csv'
    with (data_dir / 'SRG_Sales_demo.csv').open('r', newline='', encoding='utf-8') as src, output_path.open('w', newline='', encoding='utf-8') as dst:
        reader = csv.DictReader(src)
        writer = csv.DictWriter(
            dst,
            fieldnames=[
                'TransactionID', 'TransactionDate', 'Month', 'Year', 'CustomerID', 'ProductID',
                'ProductName', 'Category', 'StoreID', 'StoreName', 'District', 'Channel',
                'Quantity', 'UnitPrice', 'NetSales', 'Currency', 'PaymentMethod', 'ReturnFlag',
                'SourceSystem'
            ],
        )
        writer.writeheader()

        for row in reader:
            product = products.get(row.get('ProductID', ''), {})
            store = stores.get(row.get('StoreID', ''), {})
            txn_date = normalize_date(row.get('TransactionDate', ''))
            month = txn_date[:7] if len(txn_date) >= 7 else ''
            year = txn_date[:4] if len(txn_date) >= 4 else ''
            quantity = float(row.get('Quantity', '0') or 0)
            unit_price = float(row.get('UnitPrice', '0') or 0)
            net_sales = quantity * unit_price

            writer.writerow({
                'TransactionID': row.get('TransactionID', ''),
                'TransactionDate': txn_date,
                'Month': month,
                'Year': year,
                'CustomerID': row.get('CustomerID', ''),
                'ProductID': row.get('ProductID', ''),
                'ProductName': product.get('ProductName', ''),
                'Category': product.get('Category', ''),
                'StoreID': row.get('StoreID', ''),
                'StoreName': store.get('StoreName', ''),
                'District': store.get('District', ''),
                'Channel': row.get('Channel', ''),
                'Quantity': quantity,
                'UnitPrice': unit_price,
                'NetSales': f'{net_sales:.2f}',
                'Currency': row.get('Currency', 'UGX'),
                'PaymentMethod': row.get('PaymentMethod', ''),
                'ReturnFlag': 'True' if quantity < 0 else 'False',
                'SourceSystem': row.get('SourceSystem', ''),
            })

    print(f"Created BI dataset at {output_path} with rows from {data_dir / 'SRG_Sales_demo.csv'}")


if __name__ == '__main__':
    main()
