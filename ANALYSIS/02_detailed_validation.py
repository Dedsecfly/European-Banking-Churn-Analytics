import pandas as pd
from pathlib import Path

# Load dataset
project_root = Path(__file__).resolve().parent.parent
file_path = project_root / "data" / "European_Bank.csv"

df = pd.read_csv(file_path)

print("=" * 55)
print("EUROPEAN BANKING - DETAILED DATA VALIDATION")
print("=" * 55)

# 1. Check duplicate customer IDs
duplicate_ids = df["CustomerId"].duplicated().sum()

print(f"\nDuplicate Customer IDs: {duplicate_ids}")

# 2. Check age range
print("\nAGE VALIDATION")
print(f"Minimum Age: {df['Age'].min()}")
print(f"Maximum Age: {df['Age'].max()}")
print(f"Invalid Ages: {(df['Age'] < 18).sum()}")

# 3. Check credit scores
print("\nCREDIT SCORE VALIDATION")
print(f"Minimum Credit Score: {df['CreditScore'].min()}")
print(f"Maximum Credit Score: {df['CreditScore'].max()}")

# 4. Check countries
print("\nGEOGRAPHIC VALIDATION")
print(df["Geography"].value_counts())

# 5. Check binary columns
print("\nBINARY COLUMN VALIDATION")

binary_columns = [
    "HasCrCard",
    "IsActiveMember",
    "Exited"
]

for column in binary_columns:
    invalid = (~df[column].isin([0, 1])).sum()
    print(f"{column}: {invalid} invalid values")

# 6. Check financial values
print("\nFINANCIAL VALIDATION")
print(f"Negative Balances: {(df['Balance'] < 0).sum()}")
print(f"Negative Salaries: {(df['EstimatedSalary'] < 0).sum()}")

# 7. Check product ownership
print("\nPRODUCT VALIDATION")
print(df["NumOfProducts"].value_counts().sort_index())

# 8. Check year distribution
print("\nYEAR VALIDATION")
print(df["Year"].value_counts().sort_index())

print("\n" + "=" * 55)
print("DETAILED VALIDATION CHECKS FINISHED")
print("=" * 55)