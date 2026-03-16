# Global Internet Freedom Dashboard

This project visualizes and analyzes internet freedom, governance, and development indicators across countries. It helps explore patterns, trends, and forecasts of freedom scores worldwide.

## Features

Country Explorer – View a country’s freedom score over time and its relationships with key indicators like internet access, GDP, HDI, democracy, and corruption.

Global Trends – See how freedom scores and internet access evolve over the years globally.

Country Comparison – Compare freedom scores and development indicators across all countries.

Correlation Heatmap – Understand how different indicators relate to each other.

Forecasts – Predict the next 10 years of internet freedom for selected countries using damped exponential smoothing.

World Map – Visualize freedom scores on a global map for the latest year.

## Data Sources

Quality of Government (QoG) Data
 – Socioeconomic and governance indicators.

Freedom House
 – Country-level internet and political freedom scores.

## Insights

Wealth, HDI, and internet access are strongly correlated; richer countries tend to have higher freedom scores.

Corruption decreases with higher GDP and stronger democratic institutions.

Some outliers (like Singapore) show high wealth but partially restricted internet freedom, highlighting unique country-specific patterns.

Forecasting shows potential trends in internet freedom over the next decade, with damping providing more realistic predictions.

Clustering countries via PCA and K-Means identifies groups with similar socioeconomic profiles, making global comparisons easier.

## Technologies

Python (Pandas, Matplotlib, Seaborn, Plotly, Statsmodels)

Streamlit for interactive dashboards
