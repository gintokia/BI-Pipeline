"""
Generates a synthetic supply-chain / production dataset that mirrors the
kind of data a manufacturing PM works with (program, supplier, promised vs.
actual ship date, cost).

Swap this out for a real dataset later: Kaggle has several supply-chain and
logistics datasets ("DataCo Smart Supply Chain", "Supply Chain Shipment
Pricing Data") that use the same shape of columns. If you use a real one,
skip this script and point clean_data.py at your CSV instead.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

N_ORDERS = 500
PROGRAMS = [f"Program-{c}" for c in ["A", "B", "C", "D", "E", "F"]]
SUPPLIERS = ["Aerostar Components", "NorthField Machining", "Delta Avionics",
             "Vantage Precision", "  orbital systems  ", "Delta avionics"]  # messy on purpose
CATEGORIES = ["Structural", "Electrical", "Avionics", "Fasteners", np.nan]  # missing on purpose

start_date = datetime(2023, 1, 1)

rows = []
for i in range(N_ORDERS):
    program = np.random.choice(PROGRAMS)
    supplier = np.random.choice(SUPPLIERS)
    category = np.random.choice(CATEGORIES, p=[0.3, 0.25, 0.25, 0.15, 0.05])
    order_date = start_date + timedelta(days=int(np.random.uniform(0, 600)))
    promised_lead_days = int(np.random.choice([14, 21, 30, 45, 60]))
    promised_date = order_date + timedelta(days=promised_lead_days)

    # Build in realistic delay behavior: most on time, some late, a few very late
    delay_roll = np.random.random()
    if delay_roll < 0.65:
        actual_delay = np.random.randint(-3, 3)   # on time-ish
    elif delay_roll < 0.90:
        actual_delay = np.random.randint(3, 15)   # moderately late
    else:
        actual_delay = np.random.randint(15, 45)  # badly late

    actual_date = promised_date + timedelta(days=int(actual_delay))
    unit_cost = round(np.random.uniform(50, 5000), 2)
    quantity = int(np.random.choice([1, 5, 10, 25, 50, 100]))

    rows.append({
        "order_id": f"ORD-{1000+i}",
        "program": program,
        "supplier": supplier,
        "category": category,
        "order_date": order_date.date().isoformat(),
        "promised_date": promised_date.date().isoformat(),
        "actual_date": actual_date.date().isoformat(),
        "unit_cost": unit_cost,
        "quantity": quantity,
    })

df = pd.DataFrame(rows)

# Sprinkle in some missing values to make the cleaning step meaningful
missing_idx = np.random.choice(df.index, size=20, replace=False)
df.loc[missing_idx, "unit_cost"] = np.nan

df.to_csv("raw_orders.csv", index=False)
print(f"Wrote raw_orders.csv with {len(df)} rows")
