import pandas as pd
from pathlib import Path

# Locate project files
project_root = Path(__file__).resolve().parent.parent

input_file = project_root / "data" / "cleaned_customers.csv"
output_file = project_root / "data" / "master_analytics.csv"

# Load cleaned dataset
df = pd.read_csv(input_file)

print("=" * 65)
print("EUROPEAN BANKING - MASTER ANALYTICS DATASET")
print("=" * 65)

# 1. Create readable customer status
df["CustomerStatus"] = df["Exited"].map({
    0: "Retained",
    1: "Churned"
})

# 2. Create readable activity status
df["ActivityStatus"] = df["IsActiveMember"].map({
    0: "Inactive",
    1: "Active"
})

# 3. Create credit card ownership label
df["CreditCardStatus"] = df["HasCrCard"].map({
    0: "No Credit Card",
    1: "Has Credit Card"
})

# 4. Create high-value customer indicator
high_value_threshold = df["Balance"].quantile(0.80)

df["HighValueCustomer"] = (
    df["Balance"] >= high_value_threshold
)

df["HighValueStatus"] = df["HighValueCustomer"].map({
    True: "High Value",
    False: "Standard"
})

# 5. Create churn-associated balance metric
df["ChurnAssociatedBalance"] = df["Balance"].where(
    df["Exited"] == 1,
    0
)

# 6. Create retained customer balance metric
df["RetainedBalance"] = df["Balance"].where(
    df["Exited"] == 0,
    0
)

# 7. Validate the dataset
print("\nDATASET VALIDATION")

assert len(df) == 10000

assert df["CustomerId"].is_unique

assert df["CustomerStatus"].notna().all()

assert df["ActivityStatus"].notna().all()

assert df["HighValueStatus"].notna().all()

assert abs(
    df["ChurnAssociatedBalance"].sum()
    - df.loc[df["Exited"] == 1, "Balance"].sum()
) < 0.01

assert abs(
    df["RetainedBalance"].sum()
    - df.loc[df["Exited"] == 0, "Balance"].sum()
) < 0.01

print("All master dataset validation checks passed!")

# 8. Display summary
print("\nMASTER DATASET SUMMARY")

print(f"Total Customers: {len(df):,}")
print(f"Total Columns: {len(df.columns)}")
print(f"Overall Churn Rate: {df['Exited'].mean() * 100:.2f}%")

print(
    f"High-Value Customers: "
    f"{df['HighValueCustomer'].sum():,}"
)

print(
    f"Churn-Associated Balance: "
    f"{df['ChurnAssociatedBalance'].sum():,.2f}"
)

print("\nAVAILABLE COLUMNS")

for column in df.columns:
    print(f"- {column}")

# 9. Save master dataset
df.to_csv(output_file, index=False)

print(f"\nMaster dataset saved to: {output_file}")

print("\n" + "=" * 65)
print("MASTER ANALYTICS DATASET COMPLETED")
print("=" * 65)
