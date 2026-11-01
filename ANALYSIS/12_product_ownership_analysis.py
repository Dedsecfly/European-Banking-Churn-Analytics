import pandas as pd
from pathlib import Path

# Locate project files
project_root = Path(__file__).resolve().parent.parent

file_path = project_root / "data" / "cleaned_customers.csv"

# Load dataset
df = pd.read_csv(file_path)

print("=" * 65)
print("EUROPEAN BANKING - PRODUCT OWNERSHIP ANALYSIS")
print("=" * 65)

# 1. Analyze churn by number of products
product_analysis = df.groupby("NumOfProducts").agg(
    TotalCustomers=("CustomerId", "count"),
    ChurnedCustomers=("Exited", "sum"),
    AverageBalance=("Balance", "mean"),
    AverageAge=("Age", "mean")
)

# 2. Calculate retained customers
product_analysis["RetainedCustomers"] = (
    product_analysis["TotalCustomers"]
    - product_analysis["ChurnedCustomers"]
)

# 3. Calculate churn rate
product_analysis["ChurnRate"] = (
    product_analysis["ChurnedCustomers"]
    / product_analysis["TotalCustomers"]
    * 100
)

# 4. Calculate churn contribution
total_churned = df["Exited"].sum()

product_analysis["ChurnContribution"] = (
    product_analysis["ChurnedCustomers"]
    / total_churned
    * 100
)

# 5. Calculate relative risk index
overall_churn_rate = df["Exited"].mean() * 100

product_analysis["RelativeRiskIndex"] = (
    product_analysis["ChurnRate"]
    / overall_churn_rate
)

print("\nPRODUCT OWNERSHIP CHURN SUMMARY")

print(product_analysis.round(2).to_string())

# 6. Analyze product ownership across countries
geographic_products = df.groupby(
    ["Geography", "NumOfProducts"]
).agg(
    TotalCustomers=("CustomerId", "count"),
    ChurnedCustomers=("Exited", "sum")
)

geographic_products["ChurnRate"] = (
    geographic_products["ChurnedCustomers"]
    / geographic_products["TotalCustomers"]
    * 100
)

print("\nGEOGRAPHY × PRODUCT OWNERSHIP")

print(geographic_products.round(2).to_string())

# 7. Calculate churn-associated account balances
churned_balances = (
    df[df["Exited"] == 1]
    .groupby("NumOfProducts")["Balance"]
    .sum()
)

print("\nCHURN-ASSOCIATED BALANCES BY PRODUCT COUNT")

print(
    churned_balances.map(
        lambda value: f"{value:,.2f}"
    ).to_string()
)

# 8. Identify highest-risk product category
highest_risk = product_analysis["ChurnRate"].idxmax()

highest_rate = product_analysis.loc[
    highest_risk, "ChurnRate"
]

print("\nHIGHEST-RISK PRODUCT CATEGORY")

print(f"Number of Products: {highest_risk}")
print(f"Churn Rate: {highest_rate:.2f}%")

# 9. Validate results
print("\nVALIDATION CHECKS")

assert product_analysis["TotalCustomers"].sum() == len(df)

assert product_analysis["ChurnedCustomers"].sum() == total_churned

assert geographic_products["TotalCustomers"].sum() == len(df)

assert geographic_products["ChurnedCustomers"].sum() == total_churned

assert abs(
    product_analysis["ChurnContribution"].sum() - 100
) < 0.000001

assert abs(
    churned_balances.sum()
    - df.loc[df["Exited"] == 1, "Balance"].sum()
) < 0.01

print("All product ownership calculations verified!")

# 10. Save results
output_file = (
    project_root / "data" / "product_ownership_summary.csv"
)

product_analysis.to_csv(output_file)

print(f"\nResults saved to: {output_file}")

print("\n" + "=" * 65)
print("PRODUCT OWNERSHIP ANALYSIS COMPLETED")
print("=" * 65)
