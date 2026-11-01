import pandas as pd
from pathlib import Path

# Locate project files
project_root = Path(__file__).resolve().parent.parent
file_path = project_root / "data" / "cleaned_customers.csv"

# Load prepared dataset
df = pd.read_csv(file_path)

print("=" * 70)
print("EUROPEAN BANKING - HIGH-VALUE CUSTOMER CHURN ANALYSIS")
print("=" * 70)

# 1. Define high-value customers using the 80th percentile
high_value_threshold = df["Balance"].quantile(0.80)

df["HighValueCustomer"] = (
    df["Balance"] >= high_value_threshold
)

print("\nHIGH-VALUE CUSTOMER DEFINITION")
print(f"80th Percentile Balance: {high_value_threshold:,.2f}")

# 2. Calculate overall high-value customer metrics
high_value_df = df[df["HighValueCustomer"]].copy()

total_high_value = len(high_value_df)
churned_high_value = int(high_value_df["Exited"].sum())
retained_high_value = total_high_value - churned_high_value

high_value_churn_rate = (
    churned_high_value / total_high_value * 100
)

high_value_total_balance = high_value_df["Balance"].sum()

high_value_churned_balance = high_value_df.loc[
    high_value_df["Exited"] == 1, "Balance"
].sum()

total_churned_balance = df.loc[
    df["Exited"] == 1, "Balance"
].sum()

high_value_exposure_share = (
    high_value_churned_balance / total_churned_balance * 100
)

print("\nHIGH-VALUE CUSTOMER KPIs")

print(f"Total High-Value Customers: {total_high_value:,}")
print(f"Churned High-Value Customers: {churned_high_value:,}")
print(f"Retained High-Value Customers: {retained_high_value:,}")
print(f"High-Value Churn Rate: {high_value_churn_rate:.2f}%")

print(f"High-Value Total Balance: {high_value_total_balance:,.2f}")
print(f"High-Value Churned Balance: {high_value_churned_balance:,.2f}")

print(
    f"Share of All Churned Balances: "
    f"{high_value_exposure_share:.2f}%"
)

# 3. Analyze high-value customers by geography
geographic_analysis = high_value_df.groupby(
    "Geography"
).agg(
    TotalCustomers=("CustomerId", "count"),
    ChurnedCustomers=("Exited", "sum"),
    TotalBalance=("Balance", "sum")
)

geographic_analysis["ChurnRate"] = (
    geographic_analysis["ChurnedCustomers"]
    / geographic_analysis["TotalCustomers"]
    * 100
)

geographic_churned_balances = (
    high_value_df[high_value_df["Exited"] == 1]
    .groupby("Geography")["Balance"]
    .sum()
)

geographic_analysis["ChurnedBalance"] = (
    geographic_churned_balances
)

print("\nHIGH-VALUE CHURN BY GEOGRAPHY")

print(
    geographic_analysis.round(2).to_string(
        float_format=lambda x: f"{x:,.2f}"
    )
)

# 4. Analyze high-value customers by age
age_analysis = high_value_df.groupby(
    "AgeGroup",
    observed=True
).agg(
    TotalCustomers=("CustomerId", "count"),
    ChurnedCustomers=("Exited", "sum"),
    TotalBalance=("Balance", "sum")
)

age_analysis["ChurnRate"] = (
    age_analysis["ChurnedCustomers"]
    / age_analysis["TotalCustomers"]
    * 100
)

age_churned_balances = (
    high_value_df[high_value_df["Exited"] == 1]
    .groupby("AgeGroup", observed=True)["Balance"]
    .sum()
)

age_analysis["ChurnedBalance"] = age_churned_balances

print("\nHIGH-VALUE CHURN BY AGE GROUP")

print(
    age_analysis.round(2).to_string(
        float_format=lambda x: f"{x:,.2f}"
    )
)

# 5. Identify highest financial exposure country
highest_exposure_country = (
    geographic_analysis["ChurnedBalance"].idxmax()
)

print("\nHIGHEST FINANCIAL EXPOSURE COUNTRY")

print(f"Country: {highest_exposure_country}")

print(
    "Churn-Associated Balance: "
    f"{geographic_analysis.loc[highest_exposure_country, 'ChurnedBalance']:,.2f}"
)

# 6. Validate results
print("\nVALIDATION CHECKS")

assert geographic_analysis["TotalCustomers"].sum() == total_high_value

assert geographic_analysis["ChurnedCustomers"].sum() == churned_high_value

assert age_analysis["TotalCustomers"].sum() == total_high_value

assert age_analysis["ChurnedCustomers"].sum() == churned_high_value

assert abs(
    geographic_analysis["ChurnedBalance"].sum()
    - high_value_churned_balance
) < 0.01

assert abs(
    age_analysis["ChurnedBalance"].sum()
    - high_value_churned_balance
) < 0.01

print("All high-value customer calculations verified!")

# 7. Save summary datasets
geographic_output = (
    project_root / "data" / "high_value_geographic_summary.csv"
)

age_output = (
    project_root / "data" / "high_value_age_summary.csv"
)

geographic_analysis.to_csv(geographic_output)
age_analysis.to_csv(age_output)

print(f"\nGeographic results saved to: {geographic_output}")
print(f"Age results saved to: {age_output}")

print("\n" + "=" * 70)
print("HIGH-VALUE CUSTOMER ANALYSIS COMPLETED")
print("=" * 70)