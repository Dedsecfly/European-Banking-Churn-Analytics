import pandas as pd
from pathlib import Path

# Locate project files
project_root = Path(__file__).resolve().parent.parent

file_path = project_root / "data" / "cleaned_customers.csv"

# Load dataset
df = pd.read_csv(file_path)

print("=" * 65)
print("EUROPEAN BANKING - CUSTOMER ACTIVITY ANALYSIS")
print("=" * 65)

# 1. Create readable activity labels
df["ActivityStatus"] = df["IsActiveMember"].map({
    0: "Inactive",
    1: "Active"
})

# 2. Analyze churn by activity status
activity_analysis = df.groupby("ActivityStatus").agg(
    TotalCustomers=("CustomerId", "count"),
    ChurnedCustomers=("Exited", "sum"),
    AverageBalance=("Balance", "mean"),
    AverageAge=("Age", "mean")
)

# 3. Calculate retained customers
activity_analysis["RetainedCustomers"] = (
    activity_analysis["TotalCustomers"]
    - activity_analysis["ChurnedCustomers"]
)

# 4. Calculate churn rates
activity_analysis["ChurnRate"] = (
    activity_analysis["ChurnedCustomers"]
    / activity_analysis["TotalCustomers"]
    * 100
)

# 5. Calculate churn contribution
total_churned = df["Exited"].sum()

activity_analysis["ChurnContribution"] = (
    activity_analysis["ChurnedCustomers"]
    / total_churned
    * 100
)

# 6. Calculate relative risk index
overall_churn_rate = df["Exited"].mean() * 100

activity_analysis["RelativeRiskIndex"] = (
    activity_analysis["ChurnRate"]
    / overall_churn_rate
)

print("\nCUSTOMER ACTIVITY CHURN SUMMARY")

print(activity_analysis.round(2).to_string())

# 7. Calculate inactive vs active churn ratio
inactive_rate = activity_analysis.loc[
    "Inactive", "ChurnRate"
]

active_rate = activity_analysis.loc[
    "Active", "ChurnRate"
]

print("\nACTIVITY RISK COMPARISON")

print(f"Inactive Churn Rate: {inactive_rate:.2f}%")
print(f"Active Churn Rate: {active_rate:.2f}%")

if active_rate > 0:
    print(
        f"Inactive-to-Active Churn Ratio: "
        f"{inactive_rate / active_rate:.2f}x"
    )

# 8. Analyze activity across countries
geographic_activity = df.groupby(
    ["Geography", "ActivityStatus"]
).agg(
    TotalCustomers=("CustomerId", "count"),
    ChurnedCustomers=("Exited", "sum")
)

geographic_activity["ChurnRate"] = (
    geographic_activity["ChurnedCustomers"]
    / geographic_activity["TotalCustomers"]
    * 100
)

print("\nGEOGRAPHY × ACTIVITY CHURN ANALYSIS")

print(geographic_activity.round(2).to_string())

# 9. Calculate churn-associated balances
churned_balance = (
    df[df["Exited"] == 1]
    .groupby("ActivityStatus")["Balance"]
    .sum()
)

print("\nCHURN-ASSOCIATED ACCOUNT BALANCES")

print(churned_balance.round(2).to_string())

# 10. Validate calculations
print("\nVALIDATION CHECKS")

assert activity_analysis["TotalCustomers"].sum() == len(df)

assert activity_analysis["ChurnedCustomers"].sum() == total_churned

assert geographic_activity["TotalCustomers"].sum() == len(df)

assert geographic_activity["ChurnedCustomers"].sum() == total_churned

assert abs(
    activity_analysis["ChurnContribution"].sum() - 100
) < 0.000001

print("All customer activity calculations verified!")

# 11. Save results
output_file = (
    project_root / "data" / "customer_activity_summary.csv"
)

activity_analysis.to_csv(output_file)

print(f"\nResults saved to: {output_file}")

print("\n" + "=" * 65)
print("CUSTOMER ACTIVITY ANALYSIS COMPLETED")
print("=" * 65)