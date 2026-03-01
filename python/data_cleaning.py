import pandas as pd
import numpy as np

# ========================
# 1. Load Data
# ========================
df = pd.read_csv('data.csv', sep=';')


# =======================
# 2. Basic Inspection
# =======================
print(df.shape)
df.head()
df.info()

# =======================
# 3. Rename Columns (Readable)
# =======================
df.columns = (
    df.columns
    .str.lower()
    .str.strip()
    .str.replace(" ", "_")
    .str.replace("-", "_")
    .str.replace("(", "", regex=False)
    .str.replace(")", "", regex=False)
)

print(df.columns.tolist())


# ========================
# 4. Check Missing Values
# ========================
missing = df.isnull().sum()
missing[missing > 0]


#========================
# 5. Remove Duplicates
#========================
df = df.drop_duplicates()

#========================
# 6. Data Type Correction
#========================
df["target"] = df["target"].astype("category")

# =======================
# 7. Map Target --> Business Label
# =======================
df["churn_status"] = df["target"].map({
    "Dropout": "Churn",
    "Graduate": "Retained",
    "Enrolled": "Active"
})

# =======================
# 8. Feature Engineering (Businness Logic)
# =======================

# Total performa akdemik
df["total_units_approved"] = (
    df["curricular_units_1st_sem_approved"] +
    df["curricular_units_2nd_sem_approved"]
)

#Rasio kelulusan mata kuliah
df["approval_rate"] = (
    df["total_units_approved"] /
    (
        df["curricular_units_1st_sem_enrolled"] +
        df["curricular_units_2nd_sem_enrolled"]
    )
).replace([np.inf, -np.inf], 0)

#Risiko finansial
df["payment_risk"] = np.where(
    (df["tuition_fees_up_to_date"] == 0) | 
    (df["debtor"] == 1),
    1, 0
)

# ==========================
# 9. Outlier Check
# ==========================
numerical_cols = df.select_dtypes(include=["int64", "float64"]).columns

for col in numerical_cols:
    df[col] = df[col].clip(
        lower=df[col].quantile(0.01),
        upper=df[col].quantile(0.99)
    )

# =========================
# 10. Final Dataset Check
# =========================
df.info()
df.head()

# =========================
# 11. Save Clean Data
# =========================
df.to_csv("cleaned_student.csv", index=False)