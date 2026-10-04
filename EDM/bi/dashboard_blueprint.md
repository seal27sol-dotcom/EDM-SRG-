# Power BI / Tableau dashboard blueprint

This blueprint matches the structure of the current Savanna dashboard so the same story can be recreated in either Power BI or Tableau.

## 1. KPI cards

Top row, four tiles:

- Total Sales
- Active Customers
- Transactions
- Return Rate %

Suggested formulas:

Power BI:

```DAX
Total Sales = SUM('BI_dashboard_dataset'[NetSales])
Transactions = DISTINCTCOUNT('BI_dashboard_dataset'[TransactionID])
Active Customers = DISTINCTCOUNT('BI_dashboard_dataset'[CustomerID])
Return Lines = CALCULATE(COUNTROWS('BI_dashboard_dataset'), 'BI_dashboard_dataset'[ReturnFlag] = TRUE())
Return Rate % = DIVIDE([Return Lines], [Transactions])
```

Tableau:

```
SUM([NetSales])
COUNTD([TransactionID])
COUNTD([CustomerID])
SUM(IIF([ReturnFlag] = TRUE, 1, 0)) / COUNT([TransactionID])
```

## 2. Trend chart

- X-axis: Month
- Y-axis: Total Sales
- Filter: all date / month / channel / store / district / category

This should replicate the line chart showing monthly movement from Jan–Jun 2025.

## 3. Category bar chart

- X-axis: Category
- Y-axis: NetSales
- Sort descending

Use the same categories as the static dashboard, such as:

- Personal Care
- Electronics
- Household
- Grocery
- Beverages

## 4. Store performance panel

- Top store sales ranked descending
- Each store shown as a horizontal bar or ranked list
- Clickable filter to isolate a single store

## 5. District and channel analysis

Use these breakdowns:

- Sales by District
- Sales by Channel (POS / ECOM / APP)
- Optional map or treemap in Power BI

## 6. Detail table

Include columns:

- TransactionID
- TransactionDate
- StoreName
- Category
- ProductName
- CustomerID
- Quantity
- NetSales
- ReturnFlag

## 7. Publication checklist

Before publishing:

- set `TransactionDate` to date type
- confirm `NetSales` is decimal/number
- confirm `ReturnFlag` is Boolean
- hide raw customer and HR data from public view
- include a synthetic data disclaimer
- keep the same Uganda UGX currency context

## 8. Reporting narrative

The final story should say:

- sales trend is measured month by month
- store and category performance vary materially
- POS remains the dominant channel
- return activity should be monitored for operational quality
- the dataset is synthetic demo data, not raw SRG records
