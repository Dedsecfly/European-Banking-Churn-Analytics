import pandas as pd
from pathlib import Path

# Locate project files
project_root = Path(__file__).resolve().parent.parent

file_path = project_root / "data" / "cleaned_customers.csv"

# Load prepared dataset
df = pd.read_csv(file_path)

print("=" * 65)
print("EUROPEAN BANKING - AGE-BASED CHURN ANALYSIS")
print("=" * 65)

# 1. Group customers by age segment
age_analysis = df.groupby(
    "AgeGroup",
    observed=True
).agg(
    TotalCustomers=("CustomerId", "count"),
    ChurnedCustomers=("Exited", "sum"),
    AverageBalance=("Balance", "mean"),
    AverageCreditScore=("CreditScore", "mean")
)

# 2. Calculate retained customers
age_analysis["RetainedCustomers"] = (
    age_analysis["TotalCustomers"]
    - age_analysis["ChurnedCustomers"]
)

# 3. Calculate churn rate
age_analysis["ChurnRate"] = (
    age_analysis["ChurnedCustomers"]
    / age_analysis["TotalCustomers"]
    * 100
)

# 4. Calculate churn contribution
total_churned = df["Exited"].sum()

age_analysis["ChurnContribution"] = (
    age_analysis["ChurnedCustomers"]
    / total_churned
    * 100
)

# 5. Calculate relative churn risk
overall_churn_rate = df["Exited"].mean() * 100

age_analysis["RelativeRiskIndex"] = (
    age_analysis["ChurnRate"]
    / overall_churn_rate
)

# 6. Display age churn results
print("\nAGE GROUP CHURN SUMMARY")

print(
    age_analysis[
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

# 7. Display financial profile
print("\nFINANCIAL PROFILE BY AGE GROUP")

print(
    age_analysis[
        ["AverageBalance", "AverageCreditScore"]
    ].round(2).to_string()
)

# 8. Identify highest-risk age group
highest_risk_group = age_analysis["ChurnRate"].idxmax()

highest_churn_rate = age_analysis.loc[
    highest_risk_group, "ChurnRate"
]

print("\nHIGHEST-RISK AGE GROUP")

print(f"Age Group: {highest_risk_group}")
print(f"Churn Rate: {highest_churn_rate:.2f}%")

# 9. Validate calculations
print("\nVALIDATION CHECKS")

assert age_analysis["TotalCustomers"].sum() == len(df)

assert age_analysis["ChurnedCustomers"].sum() == total_churned

assert abs(
    age_analysis["ChurnContribution"].sum() - 100
) < 0.000001

print("All age-based calculations verified successfully!")

# 10. Save results
output_file = project_root / "data" / "age_churn_summary.csv"

age_analysis.to_csv(output_file)

print(f"\nResults saved to: {output_file}")

print("\n" + "=" * 65)
print("AGE-BASED CHURN ANALYSIS COMPLETED")
print("=" * 65)