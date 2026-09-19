# Supply Chain Risk Dashboard

**Business question:** Which programs and suppliers are at risk of late delivery, and where should a program lead intervene first?

This mirrors the reporting/dashboard work described on my resume for a
production-planning role: cleaning messy operational data, standardizing
inconsistent supplier records, and surfacing schedule risk earlier than a
manual status report would.

## What's here

- `generate_data.py` — creates a synthetic dataset (`raw_orders.csv`) with
  realistic mess: inconsistent supplier name casing/whitespace, a few
  missing categories and costs, and a mix of on-time/late/very-late orders.
- `clean_data.py` — cleans it: standardizes supplier names, fills missing
  categories/costs, computes `days_late`, and flags `at_risk` orders.
  Outputs `cleaned_orders.csv`.

## To use your own data instead

Kaggle's **"DataCo Smart Supply Chain"** or **"Supply Chain Shipment Pricing
Data"** datasets have a similar shape. Skip `generate_data.py`, point
`clean_data.py` at your CSV, and adjust the column names at the top of the
script to match.

## Steps to run

```bash
pip install pandas numpy
python generate_data.py
python clean_data.py
```

This produces `cleaned_orders.csv`.

## Building the Power BI dashboard

Load `cleaned_orders.csv` into Power BI and build:

1. **On-time % trend** — line chart of `on_time` rate by month (`order_date`)
2. **At-risk orders by supplier** — bar chart of `at_risk` count, split by `supplier`
3. **Cost exposure** — table or card of `total_cost` summed where `at_risk = True`, so a lead can see dollars at risk, not just order counts
4. **Risk detail table** — filtered table showing `order_id`, `program`, `supplier`, `days_late` where `at_risk = True`, sorted by `days_late` descending

Add a slicer on `program` so a lead can filter to just their portfolio.

## What this demonstrates

- Data cleaning / standardization (the "reconciliation errors" work)
- A derived risk metric, not just a raw report (the "surfaced risks earlier" work)
- A dashboard built around a decision ("where do I intervene first"), not just a data dump

## What I'd add with more time

- Automate the refresh (scheduled script + Power BI dataflow instead of manual CSV load)
- A simple lateness-prediction model (logistic regression on program/supplier/category) instead of a static threshold
- Cost-of-delay estimates, not just days late
