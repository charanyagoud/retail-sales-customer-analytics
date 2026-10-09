import pandas as pd

df = pd.read_csv("data/raw/online_retail.csv")

print("DATASET SHAPE")
print(df.shape)

print("\nCOLUMNS")
print(df.columns.tolist())

print("\nFIRST 5 ROWS")
print(df.head())

print("\nDATA TYPES")
print(df.dtypes)

print("\nMISSING VALUES")
print(df.isnull().sum())

print("\nDUPLICATE ROWS")
print(df.duplicated().sum())

print("\nNUMERIC SUMMARY")
print(df[["Quantity", "UnitPrice"]].describe())

print("\nUNIQUE COUNTRIES")
print(df["Country"].nunique())

print("\nDATE RANGE")
print("Earliest:", df["InvoiceDate"].min())
print("Latest:", df["InvoiceDate"].max())