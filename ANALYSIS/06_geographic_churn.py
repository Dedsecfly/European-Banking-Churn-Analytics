import pandas as pd
from pathlib import Path

# Locate project files
project_root = Path(__file__).resolve().parent.parent

file_path = project_root / "data" / "cleaned_customers.csv"

# Load prepared dataset
df = pd.read_csv(file_path)

print("=" * 65)
print("EUROPEAN BANKING - GEOGRAPHIC CHURN ANALYSIS")
print("=" * 65)

# 1. Calculate overall churn rate
overall_churn_rate = df["Exited"].mean() * 100

total_churned = df["Exited"].sum()

# 2. Group customers by country
geographic_analysis = df.groupby("Geography").agg(
    TotalCustomers=("CustomerId", "count"),
    ChurnedCustomers=("Exited", "sum"),
    TotalBalance=("Balance", "sum")
)

# 3. Calculate retained customers
geographic_analysis["RetainedCustomers"] = (
    geographic_analysis["TotalCustomers"]
    - geographic_analysis["ChurnedCustomers"]
)

# 4. Calculate country churn rates
geographic_analysis["ChurnRate"] = (
    geographic_analysis["ChurnedCustomers"]
    / geographic_analysis["TotalCustomers"]
    * 100
)

# 5. Calculate churn contribution
geographic_analysis["ChurnContribution"] = (
    geographic_analysis["ChurnedCustomers"]
    / total_churned
    * 100
)

# 6. Calculate geographic risk index
geographic_analysis["GeographicRiskIndex"] = (
    geographic_analysis["ChurnRate"]
    / overall_churn_rate
)

# 7. Calculate churned customer balances
churned_balances = (
    df[df["Exited"] == 1]
    .groupby("Geography")["Balance"]
    .sum()
)

geographic_analysis["ChurnedBalance"] = churned_balances

# 8. Sort countries by churn rate
geographic_analysis = geographic_analysis.sort_values(
    "ChurnRate",
    ascending=False
)

# 9. Display results
print("\nGEOGRAPHIC CHURN SUMMARY")

print(
    geographic_analysis[
        [
            "TotalCustomers",
            "ChurnedCustomers",
            "RetainedCustomers",
            "ChurnRate",
            "ChurnContribution",
            "GeographicRiskIndex"
        ]
    ].round(2).to_string()
)

print("\nFINANCIAL EXPOSURE BY COUNTRY")

print(
    geographic_analysis[
        ["TotalBalance", "ChurnedBalance"]
    ].round(2).to_string()
)

# 10. Validate results
print("\nVALIDATION CHECKS")

assert geographic_analysis["TotalCustomers"].sum() == len(df)

assert (
    geographic_analysis["ChurnedCustomers"].sum()
    == total_churned
)

assert abs(
    geographic_analysis["ChurnContribution"].sum() - 100
) < 0.000001

assert abs(
    geographic_analysis["ChurnedBalance"].sum()
    - df.loc[df["Exited"] == 1, "Balance"].sum()
) < 0.01

print("All geographic calculations verified successfully!")

# 11. Save results for future dashboard use
output_file = project_root / "data" / "geographic_churn_summary.csv"

geographic_analysis.to_csv(output_file)

print(f"\nResults saved to: {output_file}")

print("\n" + "=" * 65)
print("GEOGRAPHIC CHURN ANALYSIS COMPLETED")
print("=" * 65)