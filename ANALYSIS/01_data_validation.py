import pandas as pd
from pathlib import Path

# Locate the dataset
project_root = Path(__file__).resolve().parent.parent
file_path = project_root / "data" / "European_Bank.csv"

# Load the dataset
df = pd.read_csv(file_path)

# Display basic information
print("=" * 50)
print("EUROPEAN BANKING CUSTOMER CHURN ANALYTICS")
print("=" * 50)

print("\nDATASET SHAPE")
print(f"Total Customers: {len(df):,}")
print(f"Total Columns: {len(df.columns)}")

print("\nCOLUMN NAMES")
print(df.columns.tolist())

print("\nFIRST FIVE RECORDS")
print(df.head())

print("\nMISSING VALUES")
print(df.isnull().sum())

print("\nDUPLICATE RECORDS")
print(df.duplicated().sum())

print("\nOVERALL CHURN RATE")
churn_rate = df["Exited"].mean() * 100
print(f"{churn_rate:.2f}%")

print("\nDATA VALIDATION COMPLETE!")
