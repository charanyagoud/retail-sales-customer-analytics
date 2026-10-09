from ucimlrepo import fetch_ucirepo
import pandas as pd
import os

os.makedirs("data/raw", exist_ok=True)

print("Downloading Online Retail dataset...")

online_retail = fetch_ucirepo(id=352)

# Use original data so we keep ID columns such as
# InvoiceNo and StockCode as well as the feature columns.
data = online_retail.data.original.copy()

print("Dataset downloaded successfully")
print("Rows:", len(data))
print("Columns:", len(data.columns))

print("\nColumns:")
print(data.columns.tolist())

data.to_csv(
    "data/raw/online_retail.csv",
    index=False
)

print("\nSaved to data/raw/online_retail.csv")