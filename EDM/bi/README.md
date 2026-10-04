# Power BI and Tableau compatibility pack

This folder adds a Business Intelligence-ready export of the same demo dataset used by the dashboard so the project can be opened in either Power BI Desktop or Tableau.

## Files

- `../data/BI_dashboard_dataset.csv` — a flattened fact table suitable for direct import into Power BI or Tableau.

## Import into Power BI

1. Open Power BI Desktop.
2. Select Get data > Text/CSV.
3. Import `data/BI_dashboard_dataset.csv`.
4. In the Data view, set `TransactionDate` to Date type.
5. Set `ReturnFlag` to True/False and `NetSales` to Decimal Number.
6. Add the following measures:

```DAX
Total Sales = SUM('BI_dashboard_dataset'[NetSales])
Transactions = DISTINCTCOUNT('BI_dashboard_dataset'[TransactionID])
Active Customers = DISTINCTCOUNT('BI_dashboard_dataset'[CustomerID])
Return Lines = CALCULATE(COUNTROWS('BI_dashboard_dataset'), 'BI_dashboard_dataset'[ReturnFlag] = TRUE())
Return Rate % = DIVIDE([Return Lines], [Transactions])
```

Recommended visuals:

- KPI cards: Total Sales, Active Customers, Transactions, Return Rate %
- Line chart: Total Sales by Month
- Bar chart: Total Sales by Category
- Map or treemap: Sales by District
- Table: TransactionID, CustomerID, ProductName, StoreName, Quantity, NetSales

## Import into Tableau

1. Open Tableau Desktop.
2. Connect to Text file and select `data/BI_dashboard_dataset.csv`.
3. Drag `TransactionDate` to Columns and set it as Month.
4. Drag `NetSales` to Rows.
5. Use `StoreName`, `Category`, `District`, and `Channel` as dimensions.

Example calculations:

```
SUM([NetSales])
COUNTD([TransactionID])
COUNTD([CustomerID])
SUM(IIF([ReturnFlag] = TRUE, 1, 0))
SUM(IIF([ReturnFlag] = TRUE, 1, 0)) / COUNT([TransactionID])
```

## Dashboard blueprint

The layout is documented in [dashboard_blueprint.md](dashboard_blueprint.md). It mirrors the current HTML dashboard with four KPI tiles, a monthly sales trend, category ranking, store comparison, and a detailed transaction table.

## Publishing note

If the lecturer requires a Power BI or Tableau Public submission, publish the final report to the respective service and submit the public link instead of the static HTML dashboard. The underlying data and measures are already aligned with the same business story: sales, customers, product mix, store performance, and return quality.

## Provenance

The data remains synthetic demo data generated from the assignment scenario and is not an instructor-provided SRG dataset. It is safe for academic demonstration and dashboard prototyping.
