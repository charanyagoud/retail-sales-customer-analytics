import pandas as pd
import sqlite3

df = pd.read_csv(
    "data/cleaned/online_retail_cleaned.csv",
    dtype={
        "invoice_no": "string",
        "stock_code": "string"
    },
    low_memory=False
)

conn = sqlite3.connect("data/retail_sales.db")

df.to_sql(
    "sales",
    conn,
    if_exists="replace",
    index=False,
    chunksize=10000
)

# Add indexes to improve query performance
conn.execute(
    "CREATE INDEX IF NOT EXISTS idx_invoice ON sales(invoice_no)"
)

conn.execute(
    "CREATE INDEX IF NOT EXISTS idx_customer ON sales(customer_id)"
)

conn.execute(
    "CREATE INDEX IF NOT EXISTS idx_country ON sales(country)"
)

conn.execute(
    "CREATE INDEX IF NOT EXISTS idx_month ON sales(year_month)"
)

conn.commit()

row_count = conn.execute(
    "SELECT COUNT(*) FROM sales"
).fetchone()[0]

print("DATABASE CREATED SUCCESSFULLY")
print("Database: data/retail_sales.db")
print("Table: sales")
print("Rows:", row_count)

conn.close()