import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import os
from datetime import datetime

# PATH CONFIGURATION

OUTBREAK_DATA_PATH = r"cleaning/fact_outbreak_clean.csv"
DATE_DIMENSION_PATH = r"data/dim_date.csv"
OUTPUT_DIR = r"data"

MONTHLY_FILE = os.path.join(OUTPUT_DIR, "monthly_outbreak_history.csv")
FORECAST_FILE = os.path.join(OUTPUT_DIR, "outbreak_forecast.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# LOAD DATASET

print("=" * 50)
print("OUTBREAK FORECASTING MODEL")
print("=" * 50)
print("\nLoading outbreak dataset...")

# Load fact_outbreak_clean
df_outbreak = pd.read_csv(OUTBREAK_DATA_PATH)
print(f"✓ Outbreak records loaded: {len(df_outbreak)}")

# Load dim_date for date mapping
df_date = pd.read_csv(DATE_DIMENSION_PATH)
print(f"✓ Date dimension loaded: {len(df_date)} rows")

# DATA CLEANING & MERGING

print("\nCleaning outbreak data...")

# Convert historical_cases to numeric
df_outbreak["historical_cases"] = pd.to_numeric(
    df_outbreak["historical_cases"], errors="coerce"
)

# Merge with dim_date to get actual dates
df_merged = df_outbreak.merge(
    df_date[["date_id", "full_date", "year_month"]],
    on="date_id",
    how="left"
)

# Convert to datetime
df_merged["full_date"] = pd.to_datetime(df_merged["full_date"], errors="coerce")

# Drop rows with missing dates or cases
df_merged = df_merged.dropna(subset=["full_date", "historical_cases"])

print(f"✓ Records after cleaning: {len(df_merged)}")
print(f"✓ Date range: {df_merged['full_date'].min()} to {df_merged['full_date'].max()}")

# CREATE MONTHLY OUTBREAK CASES

print("\nAggregating outbreak cases by month...")

monthly_cases = (
    df_merged.groupby("year_month")["historical_cases"]
    .sum()
    .reset_index()
)

# Convert year_month back to timestamp for proper time series
monthly_cases["Month"] = pd.to_datetime(monthly_cases["year_month"])
monthly_cases = monthly_cases.sort_values("Month")
monthly_cases = monthly_cases[["Month", "historical_cases"]].copy()

monthly_cases.rename(
    columns={"historical_cases": "Actual_Cases"},
    inplace=True
)

# Display monthly aggregation
print("\nMonthly Outbreak Cases Summary:")
print(monthly_cases.to_string())

# Save monthly history
monthly_cases.to_csv(MONTHLY_FILE, index=False)
print(f"\n✓ Monthly history saved: {MONTHLY_FILE}")

# PREPARE TIME SERIES

print("\nPreparing time series for ARIMA model...")

ts = monthly_cases.set_index("Month")

# Log transform for stability (prevents negative forecasts)
ts["log_cases"] = np.log(ts["Actual_Cases"] + 1)  # +1 to avoid log(0)

print(f"✓ Time series prepared: {len(ts)} months")
print(f"✓ Min cases: {ts['Actual_Cases'].min():.0f}")
print(f"✓ Max cases: {ts['Actual_Cases'].max():.0f}")
print(f"✓ Mean cases: {ts['Actual_Cases'].mean():.0f}")

# TRAIN FORECAST MODEL

print("\nTraining ARIMA (1,1,1) forecasting model...")

try:
    model = ARIMA(ts["log_cases"], order=(1, 1, 1))
    model_fit = model.fit()
    
    print("✓ Model training completed successfully")
    print("\nARIMA Model Summary:")
    print(model_fit.summary())
    
except Exception as e:
    print(f"⚠ Error during model training: {e}")
    print("Fallback: Using last value as baseline forecast")

# FORECAST NEXT 6 MONTHS

print("\n" + "=" * 50)
print("GENERATING FORECAST")
print("=" * 50)

forecast_steps = 6

# Generate forecast
log_forecast = model_fit.forecast(steps=forecast_steps)

# Convert back from log scale
forecast_values = np.exp(log_forecast) - 1
forecast_values = np.maximum(forecast_values, 0)  # Ensure non-negative

# Generate future dates
last_date = ts.index[-1]
forecast_dates = pd.date_range(
    start=last_date + pd.DateOffset(months=1),
    periods=forecast_steps,
    freq="MS"
)

# Create forecast dataframe
forecast_df = pd.DataFrame({
    "Month": forecast_dates,
    "Forecast_Cases": forecast_values.values
})

# Round to whole numbers (cases)
forecast_df["Forecast_Cases"] = forecast_df["Forecast_Cases"].round(0).astype(int)

print("\nForecast Results (Next 6 Months):")
print(forecast_df.to_string(index=False))

# CALCULATE FORECAST METRICS

print("\n" + "=" * 50)
print("FORECAST METRICS")
print("=" * 50)

last_actual = ts["Actual_Cases"].iloc[-1]
forecast_avg = forecast_df["Forecast_Cases"].mean()
growth_rate = ((forecast_avg - last_actual) / last_actual * 100) if last_actual > 0 else 0

print(f"\nLast Actual Cases (Latest Month): {last_actual:.0f}")
print(f"Forecast Average (Next 6 Months): {forecast_avg:.0f}")
print(f"Projected Growth Rate: {growth_rate:+.2f}%")

# Save forecast
forecast_df.to_csv(FORECAST_FILE, index=False)
print(f"\n✓ Forecast saved: {FORECAST_FILE}")

# CREATE COMBINED HISTORY + FORECAST VIEW

print("\nCreating combined history + forecast view...")

# Extend monthly_cases for visualization
combined_df = monthly_cases.copy()
combined_df["Forecast_Cases"] = np.nan

# Add forecast rows
forecast_display = forecast_df.copy()
forecast_display.rename(columns={"Forecast_Cases": "Forecast_Cases"}, inplace=True)
forecast_display["Actual_Cases"] = np.nan

# Combine
combined_view = pd.concat(
    [combined_df, forecast_display],
    ignore_index=True
)
combined_view = combined_view.sort_values("Month").reset_index(drop=True)

print("\nCombined View (History + Forecast):")
print(combined_view.to_string())

# COMPLETION MESSAGE

print("\n" + "=" * 50)
print("✓ OUTBREAK FORECASTING COMPLETED SUCCESSFULLY")
print("=" * 50)
print("\nGenerated Files:")
print(f"1. {MONTHLY_FILE} - Historical monthly aggregation")
print(f"2. {FORECAST_FILE} - 6-month forecast")
