import pandas as pd
from pathlib import Path

# Locate project files
project_root = Path(__file__).resolve().parent.parent

input_file = project_root / "data" / "European_Bank.csv"
output_file = project_root / "data" / "cleaned_customers.csv"

# Load original dataset
df = pd.read_csv(input_file)

print("=" * 55)
print("EUROPEAN BANKING - DATA PREPARATION")
print("=" * 55)

# 1. Remove surname
df = df.drop(columns=["Surname"])

print("\nSurname column removed.")

# 2. Create age segments
df["AgeGroup"] = pd.cut(
    df["Age"],
    bins=[0, 29, 45, 60, float("inf")],
    labels=["Under 30", "30-45", "46-60", "Above 60"]
)

print("\nAGE SEGMENTS")
print(df["AgeGroup"].value_counts().sort_index())

# 3. Create tenure segments
df["TenureGroup"] = pd.cut(
    df["Tenure"],
    bins=[-1, 2, 6, float("inf")],
    labels=["New", "Mid-term", "Long-term"]
)

print("\nTENURE SEGMENTS")
print(df["TenureGroup"].value_counts().sort_index())

# 4. Determine balance threshold
positive_balances = df.loc[df["Balance"] > 0, "Balance"]

balance_threshold = positive_balances.median()

print(f"\nBalance Threshold: {balance_threshold:,.2f}")

# 5. Create balance segments
def classify_balance(balance):
    if balance == 0:
        return "Zero Balance"
    elif balance <= balance_threshold:
        return "Low Balance"
    else:
        return "High Balance"

df["BalanceGroup"] = df["Balance"].apply(classify_balance)

print("\nBALANCE SEGMENTS")
print(df["BalanceGroup"].value_counts())

# 6. Verify segmentation completeness
segment_columns = [
    "AgeGroup",
    "TenureGroup",
    "BalanceGroup"
]

print("\nMISSING SEGMENT VALUES")
print(df[segment_columns].isnull().sum())

# 7. Save processed dataset
df.to_csv(output_file, index=False)

print("\n" + "=" * 55)
print("DATA PREPARATION COMPLETED")
print("=" * 55)

print(f"\nTotal Customers: {len(df):,}")
print(f"Total Columns: {len(df.columns)}")
print(f"Saved File: {output_file}")