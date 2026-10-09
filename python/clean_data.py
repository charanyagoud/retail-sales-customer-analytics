import pandas as pd
import os

os.makedirs("data/cleaned", exist_ok=True)

df = pd.read_csv("data/raw/online_retail.csv")

print("Original rows:", len(df))

# Standardize column names
df.columns = [
    "invoice_no",
    "stock_code",
    "description",
    "quantity",
    "invoice_date",
    "unit_price",
    "customer_id",
    "country"
]

# Convert date column
df["invoice_date"] = pd.to_datetime(df["invoice_date"])

# Remove exact duplicate rows
df = df.drop_duplicates()

# Remove rows without product description
df = df.dropna(subset=["description"])

# Create cancellation flag before filtering
df["is_cancelled"] = (
    df["invoice_no"]
    .astype(str)
    .str.upper()
    .str.startswith("C")
)

# Create revenue column
df["revenue"] = df["quantity"] * df["unit_price"]

# Create date-related fields
df["year"] = df["invoice_date"].dt.year
df["month"] = df["invoice_date"].dt.month
df["month_name"] = df["invoice_date"].dt.month_name()
df["year_month"] = df["invoice_date"].dt.to_period("M").astype(str)
df["day_of_week"] = df["invoice_date"].dt.day_name()
df["hour"] = df["invoice_date"].dt.hour

# Valid sales transactions:
# positive quantity and positive unit price
sales_df = df[
    (df["quantity"] > 0) &
    (df["unit_price"] > 0) &
    (~df["is_cancelled"])
].copy()

# Add customer-known flag
sales_df["customer_known"] = sales_df["customer_id"].notna()

# Save cleaned sales data
sales_df.to_csv(
    "data/cleaned/online_retail_cleaned.csv",
    index=False
)

print("\nCLEANING COMPLETE")
print("Cleaned rows:", len(sales_df))
print("Columns:", len(sales_df.columns))

print("\nTOTAL REVENUE")
print(round(sales_df["revenue"].sum(), 2))

print("\nTOTAL ORDERS")
print(sales_df["invoice_no"].nunique())

print("\nUNIQUE CUSTOMERS")
print(sales_df["customer_id"].nunique())

print("\nCOUNTRIES")
print(sales_df["country"].nunique())

print("\nSaved to data/cleaned/online_retail_cleaned.csv")