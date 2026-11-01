import pandas as pd
from pathlib import Path

# Locate the dataset
project_root = Path(__file__).resolve().parent.parent
file_path = project_root / "data" / "cleaned_customers.csv"

# Load prepared dataset
df = pd.read_csv(file_path)

print("=" * 60)
print("EUROPEAN BANKING - OVERALL CHURN ANALYSIS")
print("=" * 60)

# 1. Calculate customer counts
total_customers = len(df)

churned_customers = (df["Exited"] == 1).sum()
retained_customers = (df["Exited"] == 0).sum()

# 2. Calculate churn and retention rates
churn_rate = (churned_customers / total_customers) * 100
retention_rate = (retained_customers / total_customers) * 100

print("\nCUSTOMER KPIs")
print(f"Total Customers: {total_customers:,}")
print(f"Churned Customers: {churned_customers:,}")
print(f"Retained Customers: {retained_customers:,}")
print(f"Churn Rate: {churn_rate:.2f}%")
print(f"Retention Rate: {retention_rate:.2f}%")

# 3. Compare churned and retained customers
print("\nCUSTOMER PROFILE COMPARISON")

profile_comparison = df.groupby("Exited", observed=True).agg(
    Customers=("CustomerId", "count"),
    AverageAge=("Age", "mean"),
    AverageCreditScore=("CreditScore", "mean"),
    AverageBalance=("Balance", "mean"),
    AverageSalary=("EstimatedSalary", "mean"),
    AverageTenure=("Tenure", "mean")
)

profile_comparison.index = profile_comparison.index.map({
    0: "Retained",
    1: "Churned"
})

print(profile_comparison.round(2).to_string())

# 4. Calculate total recorded balances
print("\nACCOUNT BALANCE ANALYSIS")

total_balance = df["Balance"].sum()

churned_balance = df.loc[
    df["Exited"] == 1, "Balance"
].sum()

retained_balance = df.loc[
    df["Exited"] == 0, "Balance"
].sum()

print(f"Total Recorded Balance: {total_balance:,.2f}")
print(f"Churned Customer Balance: {churned_balance:,.2f}")
print(f"Retained Customer Balance: {retained_balance:,.2f}")

# 5. Verify calculations
print("\nVALIDATION CHECKS")

assert churned_customers + retained_customers == total_customers
assert abs(churn_rate + retention_rate - 100) < 0.000001
assert abs(churned_balance + retained_balance - total_balance) < 0.01

print("All KPI calculations verified successfully!")

print("\n" + "=" * 60)
print("OVERALL CHURN ANALYSIS COMPLETED")
print("=" * 60)