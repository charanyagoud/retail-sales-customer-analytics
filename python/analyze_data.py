import pandas as pd
import os

os.makedirs("data/analysis", exist_ok=True)

df = pd.read_csv(
    "data/cleaned/online_retail_cleaned.csv",
    dtype={
        "invoice_no": "string",
        "stock_code": "string"
    },
    parse_dates=["invoice_date"],
    low_memory=False
)

# --------------------------------------------------
# OVERALL KPIs
# --------------------------------------------------

total_revenue = df["revenue"].sum()
total_orders = df["invoice_no"].nunique()
unique_customers = df["customer_id"].nunique()
total_units = df["quantity"].sum()

order_values = (
    df.groupby("invoice_no")["revenue"]
    .sum()
)

average_order_value = order_values.mean()

print("\n========== OVERALL BUSINESS KPIs ==========")
print("Total Revenue: £", round(total_revenue, 2))
print("Total Orders:", total_orders)
print("Unique Customers:", unique_customers)
print("Units Sold:", total_units)
print("Average Order Value: £", round(average_order_value, 2))

print("\nDate Range:")
print("Start:", df["invoice_date"].min())
print("End:", df["invoice_date"].max())

# --------------------------------------------------
# MONTHLY SALES
# --------------------------------------------------

monthly_summary = (
    df.groupby("year_month")
    .agg(
        revenue=("revenue", "sum"),
        orders=("invoice_no", "nunique"),
        customers=("customer_id", "nunique"),
        units_sold=("quantity", "sum")
    )
    .reset_index()
    .sort_values("year_month")
)

monthly_summary["avg_order_value"] = (
    monthly_summary["revenue"] /
    monthly_summary["orders"]
)

monthly_summary.to_csv(
    "data/analysis/monthly_sales_summary.csv",
    index=False
)

print("\n========== MONTHLY SALES ==========")
print(monthly_summary.round(2))

# --------------------------------------------------
# TOP PRODUCTS
# --------------------------------------------------

product_summary = (
    df.groupby(["stock_code", "description"])
    .agg(
        units_sold=("quantity", "sum"),
        revenue=("revenue", "sum"),
        orders=("invoice_no", "nunique")
    )
    .reset_index()
    .sort_values("revenue", ascending=False)
)

product_summary.to_csv(
    "data/analysis/product_summary.csv",
    index=False
)

print("\n========== TOP 10 PRODUCTS BY REVENUE ==========")
print(
    product_summary[
        ["description", "units_sold", "revenue"]
    ].head(10).round(2)
)

# --------------------------------------------------
# COUNTRY PERFORMANCE
# --------------------------------------------------

country_summary = (
    df.groupby("country")
    .agg(
        revenue=("revenue", "sum"),
        orders=("invoice_no", "nunique"),
        customers=("customer_id", "nunique"),
        units_sold=("quantity", "sum")
    )
    .reset_index()
    .sort_values("revenue", ascending=False)
)

country_summary["avg_order_value"] = (
    country_summary["revenue"] /
    country_summary["orders"]
)

country_summary.to_csv(
    "data/analysis/country_summary.csv",
    index=False
)

print("\n========== TOP 10 COUNTRIES BY REVENUE ==========")
print(country_summary.head(10).round(2))

# --------------------------------------------------
# CUSTOMER ANALYSIS
# --------------------------------------------------

customer_df = df.dropna(subset=["customer_id"]).copy()

customer_summary = (
    customer_df.groupby("customer_id")
    .agg(
        total_revenue=("revenue", "sum"),
        orders=("invoice_no", "nunique"),
        units_purchased=("quantity", "sum")
    )
    .reset_index()
)

customer_summary["avg_order_value"] = (
    customer_summary["total_revenue"] /
    customer_summary["orders"]
)

customer_summary = customer_summary.sort_values(
    "total_revenue",
    ascending=False
)

customer_summary.to_csv(
    "data/analysis/customer_summary.csv",
    index=False
)

print("\n========== TOP 10 CUSTOMERS ==========")
print(customer_summary.head(10).round(2))

# --------------------------------------------------
# DAY OF WEEK ANALYSIS
# --------------------------------------------------

day_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

day_summary = (
    df.groupby("day_of_week")
    .agg(
        revenue=("revenue", "sum"),
        orders=("invoice_no", "nunique"),
        units_sold=("quantity", "sum")
    )
    .reindex(day_order)
    .reset_index()
)

day_summary.to_csv(
    "data/analysis/day_of_week_summary.csv",
    index=False
)

print("\n========== SALES BY DAY ==========")
print(day_summary.round(2))

print("\nAnalysis files saved successfully.")