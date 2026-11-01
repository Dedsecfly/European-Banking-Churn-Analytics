import pandas as pd
from pathlib import Path

# Locate project files
project_root = Path(__file__).resolve().parent.parent
file_path = project_root / "data" / "cleaned_customers.csv"

# Load dataset
df = pd.read_csv(file_path)

print("=" * 65)
print("EUROPEAN BANKING - BALANCE-BASED CHURN ANALYSIS")
print("=" * 65)

# 1. Group customers by balance category
balance_analysis = df.groupby(
    "BalanceGroup",
    observed=True
).agg(
    TotalCustomers=("CustomerId", "count"),
    ChurnedCustomers=("Exited", "sum"),
    TotalBalance=("Balance", "sum"),
    AverageBalance=("Balance", "mean"),
    AverageAge=("Age", "mean")
)

# 2. Calculate retained customers
balance_analysis["RetainedCustomers"] = (
    balance_analysis["TotalCustomers"]
    - balance_analysis["ChurnedCustomers"]
)

# 3. Calculate churn rate
balance_analysis["ChurnRate"] = (
    balance_analysis["ChurnedCustomers"]
    / balance_analysis["TotalCustomers"]
    * 100
)

# 4. Calculate churn contribution
total_churned = df["Exited"].sum()

balance_analysis["ChurnContribution"] = (
    balance_analysis["ChurnedCustomers"]
    / total_churned
    * 100
)

# 5. Calculate relative risk index
overall_churn_rate = df["Exited"].mean() * 100

balance_analysis["RelativeRiskIndex"] = (
    balance_analysis["ChurnRate"]
    / overall_churn_rate
)

# 6. Calculate churn-associated balances
churned_balances = (
    df[df["Exited"] == 1]
    .groupby("BalanceGroup", observed=True)["Balance"]
    .sum()
)

balance_analysis["ChurnedBalance"] = churned_balances

# 7. Calculate share of total churn-associated balances
total_churned_balance = df.loc[
    df["Exited"] == 1, "Balance"
].sum()

balance_analysis["ChurnedBalanceShare"] = (
    balance_analysis["ChurnedBalance"]
    / total_churned_balance
    * 100
)

# 8. Display customer churn results
print("\nBALANCE SEGMENT CHURN SUMMARY")

print(
    balance_analysis[
        [
            "TotalCustomers",
            "ChurnedCustomers",
            "RetainedCustomers",
            "ChurnRate",
            "ChurnContribution",
            "RelativeRiskIndex"
        ]
    ].round(2).to_string()
)

# 9. Display financial exposure
print("\nFINANCIAL EXPOSURE BY BALANCE SEGMENT")

financial_columns = [
    "TotalBalance",
    "AverageBalance",
    "ChurnedBalance",
    "ChurnedBalanceShare"
]

print(
    balance_analysis[financial_columns]
    .round(2)
    .to_string(float_format=lambda x: f"{x:,.2f}")
)

# 10. Analyze geography and balance together
geographic_balance = df.groupby(
    ["Geography", "BalanceGroup"],
    observed=True
).agg(
    TotalCustomers=("CustomerId", "count"),
    ChurnedCustomers=("Exited", "sum")
)

geographic_balance["ChurnRate"] = (
    geographic_balance["ChurnedCustomers"]
    / geographic_balance["TotalCustomers"]
    * 100
)

print("\nGEOGRAPHY × BALANCE CHURN ANALYSIS")

print(geographic_balance.round(2).to_string())

# 11. Identify highest-risk balance category
highest_risk = balance_analysis["ChurnRate"].idxmax()

highest_rate = balance_analysis.loc[
    highest_risk, "ChurnRate"
]

print("\nHIGHEST-RISK BALANCE CATEGORY")

print(f"Balance Group: {highest_risk}")
print(f"Churn Rate: {highest_rate:.2f}%")

# 12. Validate calculations
print("\nVALIDATION CHECKS")

assert balance_analysis["TotalCustomers"].sum() == len(df)

assert balance_analysis["ChurnedCustomers"].sum() == total_churned

assert abs(
    balance_analysis["TotalBalance"].sum()
    - df["Balance"].sum()
) < 0.01

assert abs(
    balance_analysis["ChurnedBalance"].sum()
    - total_churned_balance
) < 0.01

assert abs(
    balance_analysis["ChurnContribution"].sum() - 100
) < 0.000001

assert abs(
    balance_analysis["ChurnedBalanceShare"].sum() - 100
) < 0.000001

print("All balance calculations verified successfully!")

# 13. Save results
output_file = (
    project_root / "data" / "balance_churn_summary.csv"
)

balance_analysis.to_csv(output_file)

print(f"\nResults saved to: {output_file}")

print("\n" + "=" * 65)
print("BALANCE-BASED CHURN ANALYSIS COMPLETED")
print("=" * 65)