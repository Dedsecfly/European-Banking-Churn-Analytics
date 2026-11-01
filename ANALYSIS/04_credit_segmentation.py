import pandas as pd
from pathlib import Path

# Locate project files
project_root = Path(__file__).resolve().parent.parent

file_path = project_root / "data" / "cleaned_customers.csv"

# Load prepared dataset
df = pd.read_csv(file_path)

print("=" * 55)
print("EUROPEAN BANKING - CREDIT SCORE SEGMENTATION")
print("=" * 55)

# 1. Create credit score groups
df["CreditScoreGroup"] = pd.cut(
    df["CreditScore"],
    bins=[0, 579, 699, float("inf")],
    labels=["Low", "Medium", "High"]
)

# 2. Display customer distribution
print("\nCREDIT SCORE DISTRIBUTION")

print(
    df["CreditScoreGroup"]
    .value_counts()
    .sort_index()
)

# 3. Calculate percentage distribution
print("\nCREDIT SCORE PERCENTAGES")

percentages = (
    df["CreditScoreGroup"]
    .value_counts(normalize=True)
    .sort_index()
    * 100
)

print(percentages.round(2))

# 4. Check missing segment values
print("\nMISSING CREDIT SCORE GROUPS")

print(df["CreditScoreGroup"].isnull().sum())

# 5. Verify total customers
print("\nDATASET VERIFICATION")

print(f"Total Customers: {len(df):,}")
print(f"Total Columns: {len(df.columns)}")

# 6. Save updated dataset
df.to_csv(file_path, index=False)

print("\n" + "=" * 55)
print("CREDIT SCORE SEGMENTATION COMPLETED")
print("=" * 55)