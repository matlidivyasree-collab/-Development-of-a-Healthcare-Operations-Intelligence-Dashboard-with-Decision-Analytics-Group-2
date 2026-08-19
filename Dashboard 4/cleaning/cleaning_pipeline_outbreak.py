
import pandas as pd
import numpy as np

# load raw data
df = pd.read_csv("C:\\Users\\Madhav Yadav\\OneDrive\\Desktop\\Medical_Operations_Intelligence_Dashboard\\data\\fact_outbreak.csv")
print(df.shape)
print(df.head())

# checking how messy the flag columns are
print(df["new_outbreak_flag"].unique())
print(df["controlled_flag"].unique())
print(df["emergency_alert_flag"].unique())

# these three columns are basically yes/no 
# going to  map them all to True/False

yes_vals = ["yes", "y", "true", "1"]
no_vals = ["no", "n", "false", "0"]

def fix_bool(x):
    x = str(x).strip().lower()
    if x in yes_vals:
        return True
    elif x in no_vals:
        return False
    else:
        return np.nan

for col in ["new_outbreak_flag", "controlled_flag", "emergency_alert_flag"]:
    df[col] = df[col].apply(fix_bool)

# alert_level has extra spaces fix that's problem
df["alert_level"] = df["alert_level"].str.strip().str.lower()
df["alert_level"] = df["alert_level"].replace({
    "low": "Low",
    "moderate": "Moderate",
    "high": "High"
})

# state names are all over the place - spacing, caps
df["state_name_raw"] = df["state_name_raw"].str.strip()
df["state_name_raw"] = df["state_name_raw"].apply(lambda x: " ".join(x.split()))
df["state_name_raw"] = df["state_name_raw"].str.title()

# NCT looks weird after title case (Delhi (Nct)) so fix that manually
df["state_name_raw"] = df["state_name_raw"].str.replace("(Nct)", "(NCT)", regex=False)
df = df.rename(columns={"state_name_raw": "state_name"})

# check null values
print(df.isnull().sum())

# fill missing numeric values with median
num_cols = ["containment_rate_pct", "response_time_hours", "forecast_accuracy_pct", "hospital_readiness_score"]
for col in num_cols:
    med = df[col].median()
    df[col] = df[col].fillna(med)
    print(col, "filled with", med)

# Getting duplicate Rows and Drop duplicate rows in our datasets 
before = len(df)
df = df.drop_duplicates()
print("dropped", before - len(df), "duplicate rows")

# also drop rows where outbreak_id is  repeats 
df = df.drop_duplicates(subset="outbreak_id", keep="first")

# quick sanity check on percentage columns, shouldn't be outside 0-100
for col in ["containment_rate_pct", "forecast_accuracy_pct", "hospital_readiness_score", "resource_readiness_score"]:
    bad = df[(df[col] < 0) | (df[col] > 100)]
    if len(bad) > 0:
        print(col, "has", len(bad), "rows out of range")

# make ids proper ints just in case
id_cols = ["outbreak_id", "date_id", "state_id", "disease_id", "source_id", "predicted_cases", "historical_cases"]
for col in id_cols:
    df[col] = df[col].astype(int)

df = df.sort_values("outbreak_id")

df.to_csv("fact_outbreak_clean.csv", index=False)
print("done, saved clean file")
print(df.shape)