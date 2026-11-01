import pandas as pd
from pathlib import Path

# Locate project files
project_root = Path(__file__).resolve().parent.parent

file_path = project_root / "data" / "cleaned_customers.csv"

# Load prepared dataset
df = pd.read_csv(file_path)

print("=" * 65)
print("EUROPEAN BANKING - TENURE-BASED CHURN ANALYSIS")
print("=" * 65)

# 1. Group customers by tenure
tenure_analysis = df.groupby(
    "TenureGroup",
    observed=True
).agg(
    TotalCustomers=("CustomerId", "count"),
    ChurnedCustomers=("Exited", "sum"),
    AverageBalance=("Balance", "mean"),
    AverageAge=("Age", "mean")
)

# 2. Calculate retained customers
tenure_analysis["RetainedCustomers"] = (
    tenure_analysis["TotalCustomers"]
    - tenure_analysis["ChurnedCustomers"]
)

# 3. Calculate churn rate
tenure_analysis["ChurnRate"] = (
    tenure_analysis["ChurnedCustomers"]
    / tenure_analysis["TotalCustomers"]
    * 100
)

# 4. Calculate churn contribution
total_churned = df["Exited"].sum()

tenure_analysis["ChurnContribution"] = (
    tenure_analysis["ChurnedCustomers"]
    / total_churned
    * 100
)

# 5. Calculate relative risk index
overall_churn_rate = df["Exited"].mean() * 100

tenure_analysis["RelativeRiskIndex"] = (
    tenure_analysis["ChurnRate"]
    / overall_churn_rate
)

# 6. Display results
print("\nTENURE CHURN SUMMARY")

print(
    tenure_analysis.round(2).to_string()
)

# 7. Analyze exact tenure years
yearly_analysis = df.groupby("Tenure").agg(
    TotalCustomers=("CustomerId", "count"),
    ChurnedCustomers=("Exited", "sum")
)

yearly_analysis["ChurnRate"] = (
    yearly_analysis["ChurnedCustomers"]
    / yearly_analysis["TotalCustomers"]
    * 100
)

print("\nCHURN RATE BY EXACT TENURE YEAR")

print(yearly_analysis.round(2).to_string())

# 8. Identify highest-risk tenure group
highest_risk = tenure_analysis["ChurnRate"].idxmax()

highest_rate = tenure_analysis.loc[
    highest_risk, "ChurnRate"
]

print("\nHIGHEST-RISK TENURE GROUP")

print(f"Tenure Group: {highest_risk}")
print(f"Churn Rate: {highest_rate:.2f}%")

# 9. Validate results
print("\nVALIDATION CHECKS")

assert tenure_analysis["TotalCustomers"].sum() == len(df)

assert tenure_analysis["ChurnedCustomers"].sum() == total_churned

assert abs(
    tenure_analysis["ChurnContribution"].sum() - 100
) < 0.000001

print("All tenure calculations verified successfully!")

# 10. Save results
output_file = project_root / "data" / "tenure_churn_summary.csv"

tenure_analysis.to_csv(output_file)

print(f"\nResults saved to: {output_file}")

print("\n" + "=" * 65)
print("TENURE-BASED CHURN ANALYSIS COMPLETED")
print("=" * 65)