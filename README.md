# snow_policy_analysis_Toronto_2025
Analysis of snowfall and government policy timing in Toronto(Winter 2025)

## Project Goal:
Are most heavy-snow policy announced before or after snow events?

## Data source:
Climate data: From Environment and Climate Change Canada 

Policy information: self-collected from City of Toronto and City news

## Method:
1. Merge climate and policy data on date
2. Define snow events as mean_temp <= 0°C and total_precip > 0 mm
3. Compute timing of policies relative to nearest snow events
4. Visualize snow events and policy dates

## Result:
Scatter plot of snowfall with policy announcement dates

Most policies are before the snow events
<img width="1772" height="729" alt="image" src="https://github.com/user-attachments/assets/baa3a3ce-2cbc-46f6-a0a2-2072e4b5b523" />

