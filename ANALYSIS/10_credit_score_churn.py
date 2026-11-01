import pandas as pd
from pathlib import Path

# Locate project files
project_root = Path(__file__).resolve().parent.parent

file_path = project_root / "data" / "cleaned_customers.csv"

# Load prepared dataset
df = pd.read_csv(file_path)

print("=" * 65)
print("EUROPEAN BANKING - CREDIT SCORE CHURN ANALYSIS")
print("=" * 65)

# 1. Group customers by credit score category
credit_analysis = df.groupby(
    "CreditScoreGroup",
    observed=True
).agg(
    TotalCustomers=("CustomerId", "count"),
    ChurnedCustomers=("Exited", "sum"),
    AverageCreditScore=("CreditScore", "mean"),
    AverageBalance=("Balance", "mean"),
    AverageAge=("Age", "mean")
)

# 2. Calculate retained customers
credit_analysis["RetainedCustomers"] = (
    credit_analysis["TotalCustomers"]
    - credit_analysis["ChurnedCustomers"]
)

# 3. Calculate churn rate
credit_analysis["ChurnRate"] = (
    credit_analysis["ChurnedCustomers"]
    / credit_analysis["TotalCustomers"]
    * 100
)

# 4. Calculate churn contribution
total_churned = df["Exited"].sum()

credit_analysis["ChurnContribution"] = (
    credit_analysis["ChurnedCustomers"]
    / total_churned
    * 100
)

# 5. Calculate relative risk index
overall_churn_rate = df["Exited"].mean() * 100

credit_analysis["RelativeRiskIndex"] = (
    credit_analysis["ChurnRate"]
    / overall_churn_rate
)

# 6. Display credit score analysis
print("\nCREDIT SCORE CHURN SUMMARY")

print(
    credit_analysis.round(2).to_string()
)

# 7. Analyze credit scores in 50-point intervals
credit_bins = list(range(350, 851, 50)) + [float("inf")]

df["CreditScoreBand"] = pd.cut(
    df["CreditScore"],
    bins=credit_bins,
    right=False,
    include_lowest=True
)

band_analysis = df.groupby(
    "CreditScoreBand",
    observed=True
).agg(
    TotalCustomers=("CustomerId", "count"),
    ChurnedCustomers=("Exited", "sum")
)

band_analysis["ChurnRate"] = (
    band_analysis["ChurnedCustomers"]
    / band_analysis["TotalCustomers"]
    * 100
)

print("\nCHURN RATE BY 50-POINT CREDIT SCORE BAND")

print(band_analysis.round(2).to_string())

# 8. Identify highest-risk credit score group
highest_risk = credit_analysis["ChurnRate"].idxmax()

highest_rate = credit_analysis.loc[
    highest_risk, "ChurnRate"
]

print("\nHIGHEST-RISK CREDIT SCORE GROUP")

print(f"Credit Score Group: {highest_risk}")
print(f"Churn Rate: {highest_rate:.2f}%")

# 9. Validate results
print("\nVALIDATION CHECKS")

assert credit_analysis["TotalCustomers"].sum() == len(df)

assert credit_analysis["ChurnedCustomers"].sum() == total_churned

assert abs(
    credit_analysis["ChurnContribution"].sum() - 100
) < 0.000001

assert band_analysis["TotalCustomers"].sum() == len(df)

assert band_analysis["ChurnedCustomers"].sum() == total_churned

print("All credit score calculations verified successfully!")

# 10. Save results
output_file = (
    project_root / "data" / "credit_score_churn_summary.csv"
)

credit_analysis.to_csv(output_file)

print(f"\nResults saved to: {output_file}")

print("\n" + "=" * 65)
print("CREDIT SCORE CHURN ANALYSIS COMPLETED")
print("=" * 65)

