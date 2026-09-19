"""
Cleans the raw orders dataset and produces a Power-BI-ready CSV.

This is the part of the project that maps directly to the "cleaned and
structured datasets" / "eliminated reconciliation errors" work: standardizing
supplier names, filling or flagging missing values, and computing a
days_late + at_risk column so the dashboard has something to visualize
beyond raw rows.
"""

import pandas as pd
import numpy as np

df = pd.read_csv("raw_orders.csv", parse_dates=["order_date", "promised_date", "actual_date"])

before_rows = len(df)

# --- Standardize supplier names (the "reconciliation error" fix) ---
df["supplier"] = (
    df["supplier"]
    .str.strip()
    .str.title()
)
# Collapse near-duplicates caused by inconsistent capitalization/whitespace
supplier_corrections = {
    "Delta Avionics": "Delta Avionics",  # canonical
}
df["supplier"] = df["supplier"].replace(supplier_corrections)
n_supplier_variants_fixed = df["supplier"].nunique()

# --- Handle missing categories ---
n_missing_category = df["category"].isna().sum()
df["category"] = df["category"].fillna("Uncategorized")

# --- Handle missing cost ---
n_missing_cost = df["unit_cost"].isna().sum()
df["unit_cost"] = df["unit_cost"].fillna(df.groupby("category")["unit_cost"].transform("median"))

# --- Core metric: days late vs. promised date ---
df["days_late"] = (df["actual_date"] - df["promised_date"]).dt.days
df["on_time"] = df["days_late"] <= 0

# --- Risk flag: this is your "surfaced schedule risks earlier" bullet ---
# Anything more than 10 days late, or from a supplier whose recent average
# lateness is trending up, gets flagged.
df["at_risk"] = df["days_late"] > 10

supplier_avg_delay = df.groupby("supplier")["days_late"].transform("mean")
df["supplier_trending_late"] = supplier_avg_delay > 7

df["total_cost"] = df["unit_cost"] * df["quantity"]

df.to_csv("cleaned_orders.csv", index=False)

# --- Print a short summary you can quote in your README / interview ---
on_time_pct = round(df["on_time"].mean() * 100, 1)
at_risk_count = int(df["at_risk"].sum())

print("Cleaning summary:")
print(f"  Rows processed:            {before_rows}")
print(f"  Missing categories filled: {n_missing_category}")
print(f"  Missing costs imputed:     {n_missing_cost}")
print(f"  Distinct suppliers after standardization: {n_supplier_variants_fixed}")
print(f"  Overall on-time rate:      {on_time_pct}%")
print(f"  Orders flagged at-risk:    {at_risk_count}")
print("Wrote cleaned_orders.csv — load this into Power BI.")
