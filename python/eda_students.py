import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


sns.set_style("whitegrid")

# 1.LOAD DATA
# ====================================
df = pd.read_csv("cleaning.csv")

print("Shape:", df.shape)
print("\nData Types:")
print(df.dtypes)

# 2. TARGET DISTRIBUTION
# =====================================
import os
os.makedirs("images", exist_ok=True)

print("\nChurn Distribution (%):")
print(df["churn_status"].value_counts(normalize=True) * 100)

plt.figure()
df["churn_status"].value_counts().plot(kind="bar")
plt.title("Distribution of Churn Status")
plt.xlabel("Status")
plt.ylabel("Count")
plt.savefig("churn_distribution.png", dpi=300, bbox_inches="tight")
plt.show()


# 3.ACADEMIC PERFORMANCE ANALYSIS
# ====================================

print("\nApproval Rate by Status:")
print(df.groupby("churn_status")["approval_rate"].mean())

plt.figure()
sns.boxplot(x="churn_status", y="approval_rate", data=df)
plt.title("Approval Rate vs Churn Status")
plt.show()

print("\nTotal Units Approved by Status:")
print(df.groupby("churn_status")["total_units_approved"].mean())

plt.figure()
sns.boxplot(x="churn_status", y="total_units_approved", data=df)
plt.title("Total Units Approved vs Churn Status")
plt.show()


# 4. FINANCIAL RISK ANALYSIS
#=========================================

print("\nPayment Risk vs Churn (%):")
print(pd.crosstab(df["payment_risk"], df["churn_status"], normalize="index") * 100)

plt.figure()
sns.countplot(x="payment_risk", hue="churn_status", data=df)
plt.title("Payment Risk vs Churn Status")
plt.show()

print("\nDebtor vs Churn (%):")
print(pd.crosstab(df["debtor"], df["churn_status"], normalize="index") * 100)


# 5. CORRELATION ANALYSIS
#======================================

numerical_cols = df.select_dtypes(include=["int64", "float64"])

plt.figure(figsize=(12, 8))
corr = numerical_cols.corr()
sns.heatmap(corr, cmap="coolwarm")
plt.title("Correlation Matrix")
plt.show()

# 6. HIGH RISK SEGMENT CHECK
#============================================

high_risk = df[
    (df["approval_rate"] < 0.5) &
    (df["payment_risk"] == 1)
]

print("\nHigh Risk Students Distribution:")
print(high_risk ["churn_status"].value_counts(normalize=True) * 100)


# 7. SUMMARY INSIGHT METRICS
# =====================================

print("\n=== KPI SUMMARY ===")
print("Total Students:", len(df))
print("Dropout Rate:",
      round((df["churn_status"] == "Churn").mean() * 100, 2), "%")
print("Average Approval Rate:",
      round(df["approval_rate"].mean(), 2))
print("Payment Risk Rate:",
      round(df["payment_risk"].mean() * 100, 2), "%")

print("\nEDA Completed Successfully.")