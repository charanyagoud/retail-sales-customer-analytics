import sqlite3
import pandas as pd

conn = sqlite3.connect("data/retail_sales.db")

with open(
    "sql/analysis_queries.sql",
    "r",
    encoding="utf-8"
) as file:
    sql_text = file.read()

queries = [
    query.strip()
    for query in sql_text.split(";")
    if query.strip()
]

for number, query in enumerate(queries, start=1):

    first_line = query.splitlines()[0]

    title = first_line.replace("--", "").strip()

    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

    result = pd.read_sql_query(query, conn)

    print(result.to_string(index=False))

conn.close()

print("\nSQL analysis completed successfully.")