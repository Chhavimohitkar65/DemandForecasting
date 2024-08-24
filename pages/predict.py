import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import statsmodels.api as sm
from statsmodels.tsa.api import VAR
import matplotlib.pyplot as plt

# Generate synthetic data for demonstration
def generate_synthetic_data():
    np.random.seed(42)
    dates = pd.date_range(start="2020-01-01", periods=24, freq='M')
    stock_levels = np.random.randint(50, 150, size=len(dates))
    revenue = np.random.randint(5000, 15000, size=len(dates))
    sales_units = np.random.randint(100, 500, size=len(dates))
    
    df = pd.DataFrame({
        'Date': dates,
        'Stock_Level': stock_levels,
        'Revenue': revenue,
        'Sales_Units': sales_units
    })
    df.set_index('Date', inplace=True)
    return df

# Univariate Forecasting with ARIMA
def univariate_forecast(df, value_col):
    model = sm.tsa.ARIMA(df[value_col], order=(1, 1, 1))  # ARIMA model parameters (p,d,q)
    results = model.fit()
    forecast = results.forecast(steps=12)  # Forecasting next 12 months
    forecast_dates = pd.date_range(start=df.index[-1] + pd.DateOffset(months=1), periods=12, freq='M')
    forecast_df = pd.DataFrame(forecast, index=forecast_dates, columns=['Forecast'])
    return forecast_df

# Multivariate Forecasting with VAR
def multivariate_forecast(df, target_col, feature_cols):
    model = VAR(df[feature_cols + [target_col]])
    
    # Automatically select the number of lags
    maxlags = min(15, len(df) // (5 * len(df.columns)))
    results = model.fit(maxlags=maxlags, ic='aic')
    
    forecast = results.forecast(df[feature_cols + [target_col]].values[-results.k_ar:], steps=12)
    forecast_df = pd.DataFrame(forecast, index=pd.date_range(start=df.index[-1] + pd.DateOffset(months=1), periods=12, freq='M'), columns=feature_cols + [target_col])
    return forecast_df

# Streamlit UI
st.title("Inventory Forecasting")

# Generate synthetic data
df = generate_synthetic_data()

# Univariate Forecasting
st.subheader("Univariate Forecasting with ARIMA")
st.write("Historical Stock Levels:")
st.line_chart(df['Stock_Level'], use_container_width=True)

forecast_df_univariate = univariate_forecast(df, 'Stock_Level')
st.write("Forecasted Stock Levels:")
st.line_chart(pd.concat([df['Stock_Level'], forecast_df_univariate], axis=1), use_container_width=True)
st.write("**Forecasted Data**")
st.dataframe(forecast_df_univariate, use_container_width=True)

# Multivariate Forecasting
st.subheader("Multivariate Forecasting with VAR")
st.write("Historical Data (Stock Level, Revenue, Sales Units):")
st.line_chart(df[['Stock_Level', 'Revenue', 'Sales_Units']], use_container_width=True)

forecast_df_multivariate = multivariate_forecast(df, 'Stock_Level', ['Revenue', 'Sales_Units'])
st.write("Forecasted Data:")
st.line_chart(forecast_df_multivariate[['Stock_Level']], use_container_width=True)
st.write("**Forecasted Data**")
st.dataframe(forecast_df_multivariate, use_container_width=True)
