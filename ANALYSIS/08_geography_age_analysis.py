import pandas as pd
from pathlib import Path

# Locate dataset
project_root = Path(__file__).resolve().parent.parent

file_path = project_root / "data" / "cleaned_customers.csv"

# Load data
df = pd.read_csv(file_path)

print("=" * 65)
print("EUROPEAN BANKING - GEOGRAPHY AND AGE CHURN ANALYSIS")
print("=" * 65)

# 1. Group by geography and age
segment_analysis = df.groupby(
    ["Geography", "AgeGroup"],
    observed=True
).agg(
    TotalCustomers=("CustomerId", "count"),
    ChurnedCustomers=("Exited", "sum"),
    AverageBalance=("Balance", "mean")
)

# 2. Calculate churn rate
segment_analysis["ChurnRate"] = (
    segment_analysis["ChurnedCustomers"]
    / segment_analysis["TotalCustomers"]
    * 100
)

# 3. Calculate churn contribution
total_churned = df["Exited"].sum()

segment_analysis["ChurnContribution"] = (
    segment_analysis["ChurnedCustomers"]
    / total_churned
    * 100
)

# 4. Display segment results
print("\nGEOGRAPHY AND AGE SEGMENT SUMMARY")

print(
    segment_analysis.round(2).to_string()
)

# 5. Create churn rate matrix
churn_matrix = df.pivot_table(
    index="Geography",
    columns="AgeGroup",
    values="Exited",
    aggfunc="mean",
    observed=True
) * 100

# Arrange age groups
age_order = [
    "Under 30",
    "30-45",
    "46-60",
    "Above 60"
]

churn_matrix = churn_matrix[age_order]

print("\nGEOGRAPHY × AGE CHURN RATE MATRIX (%)")

print(churn_matrix.round(2).to_string())

# 6. Identify highest-risk segment
highest_risk = segment_analysis["ChurnRate"].idxmax()

highest_rate = segment_analysis.loc[
    highest_risk, "ChurnRate"
]

print("\nHIGHEST-RISK SEGMENT")

print(f"Country: {highest_risk[0]}")
print(f"Age Group: {highest_risk[1]}")
print(f"Churn Rate: {highest_rate:.2f}%")

# 7. Validate results
print("\nVALIDATION CHECKS")

assert segment_analysis["TotalCustomers"].sum() == len(df)

assert segment_analysis["ChurnedCustomers"].sum() == total_churned

assert abs(
    segment_analysis["ChurnContribution"].sum() - 100
) < 0.000001

print("All geography-age calculations verified!")

# 8. Save analysis
output_file = (
    project_root / "data" / "geography_age_summary.csv"
)

segment_analysis.to_csv(output_file)

print(f"\nResults saved to: {output_file}")

print("\n" + "=" * 65)
print("GEOGRAPHY AND AGE ANALYSIS COMPLETED")
print("=" * 65)