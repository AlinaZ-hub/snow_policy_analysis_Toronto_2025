# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pandas as pd
import matplotlib.pyplot as plt

climate0 = pd.read_csv('2025_climate_daily.csv')
# print(climate.columns)
# The output is: ['Longitude (x)', 'Latitude (y)', 'Station Name', 'Climate ID',
#        'Date/Time', 'Year', 'Month', 'Day', 'Data Quality', 'Max Temp (°C)',
#        'Max Temp Flag', 'Min Temp (°C)', 'Min Temp Flag', 'Mean Temp (°C)',
#        'Mean Temp Flag', 'Heat Deg Days (°C)', 'Heat Deg Days Flag',
#        'Cool Deg Days (°C)', 'Cool Deg Days Flag', 'Total Rain (mm)',
#        'Total Rain Flag', 'Total Snow (cm)', 'Total Snow Flag',
#        'Total Precip (mm)', 'Total Precip Flag', 'Snow on Grnd (cm)',
#        'Snow on Grnd Flag', 'Dir of Max Gust (10s deg)',
#        'Dir of Max Gust Flag', 'Spd of Max Gust (km/h)',
#        'Spd of Max Gust Flag']
policy = pd.read_csv('2025_policy.csv')

climate0["Date/Time"] = pd.to_datetime(climate0["Date/Time"])
policy["Date/Time"] = pd.to_datetime(policy["Date/Time"])

policy["Policy"] = 1
climate = climate0.merge(policy[["Date/Time", "Policy"]],
                   on="Date/Time",
                   how="left")
climate["Policy"] = climate["Policy"].fillna(0)

winter = climate[climate["Month"].isin([12, 1, 2])]
winter_climate = winter[[
    "Date/Time",
    "Mean Temp (°C)",
    "Max Temp (°C)",
    "Min Temp (°C)",
    "Total Precip (mm)",
    "Policy"]]

winter_climate = winter_climate.rename(columns={
    "Date/Time": "date",
    "Mean Temp (°C)": "mean_temp",
    "Max Temp (°C)": "max_temp",
    "Min Temp (°C)": "min_temp",
    "Total Precip (mm)": "total_precip"})

# print(winter_climate.isnull().sum())
# The output is:
# date            0
# mean_temp       1
# max_temp        1
# min_temp        1
# total_precip    2
# Policy          0
# dtype: int64

winter_climate["mean_temp"] = pd.to_numeric(
    winter_climate["mean_temp"], errors="coerce")

winter_climate["total_precip"] = pd.to_numeric(
    winter_climate["total_precip"], errors="coerce")

winter_climate = winter_climate.dropna()

winter_climate["snow_event"] = (
    (winter_climate["mean_temp"] <= 0) &
    (winter_climate["total_precip"] > 0)).astype(int)

# print(winter_climate.head())
# print("Snow days:", winter_climate["snow_event"].sum())
#The output is:
# date  mean_temp  max_temp  min_temp  total_precip  Policy  snow_event
# 0 2025-01-01        2.4       3.6       1.1           0.4     0.0           0
# 1 2025-01-02       -0.3       1.5      -2.1           0.0     0.0           0
# 2 2025-01-03       -1.4       1.4      -4.1           0.0     0.0           0
# 3 2025-01-04       -3.5      -1.1      -5.8           0.0     0.0           0
# 4 2025-01-05       -2.4       0.0      -4.8           0.0     0.0           0
# Snow days: 20

snow_dates = winter_climate[winter_climate["snow_event"] == 1]["date"]
policy_dates = winter_climate[winter_climate["Policy"] == 1]["date"]

results = []

for p_date in policy_dates:

    diffs = snow_dates - p_date

    nearest = diffs.iloc[(diffs.abs().argmin())]

    days_diff = nearest.days

    if days_diff < 0:
        timing = "Before Snow"
    elif days_diff > 0:
        timing = "After Snow"
    else:
        timing = "Same Day"

    results.append({
        "policy_date": p_date,
        "days_from_snow": days_diff,
        "timing": timing})

results_df = pd.DataFrame(results)

plt.figure(figsize=(12, 5))

plt.scatter(
    winter_climate["date"],
    winter_climate["total_precip"],
    label="Snow day",
    alpha=0.7)

for d in policy["Date/Time"]:
    plt.axvline(d, color="black", linestyle="--", alpha=0.8)

plt.title("Timing of Snow Events and Government Policy Announcements (Winter 2025)")
plt.xlabel("Date")
plt.ylabel("Total Precipitation (mm)")
plt.legend()
plt.tight_layout()
plt.show()
print(results_df)
