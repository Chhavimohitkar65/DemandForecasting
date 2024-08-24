import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

# List of medical categories and products
categories = ['Cardiology', 'Neurology', 'Oncology', 'Pediatrics']
products = [
    'Aspirin', 'Paracetamol', 'Ibuprofen', 'Insulin', 'Amoxicillin',
    'Ventilator', 'ECG Machine', 'Defibrillator', 'Stethoscope', 'X-Ray Machine',
    'Ultrasound Machine', 'IV Drip', 'Syringe', 'Blood Pressure Monitor', 'Oxygen Mask'
]

# Generate random medical data
np.random.seed(42)
data = {
    'Category': np.random.choice(categories, size=100),
    'Product_Name': np.random.choice(products, size=100),
    'Historical_Demand': np.random.randint(10, 100, size=100),
    'Forecasted_Demand': np.random.randint(10, 100, size=100),
    'Emergency_Buffer_Stock': np.random.randint(5, 30, size=100)
}

df = pd.DataFrame(data)

# Page layout
st.title("Emergency Stock Management Dashboard")


st.dataframe(df.head())

# Create and display a bar chart for forecasted demand vs historical demand
st.subheader("Demand Comparison")
fig = plt.figure(figsize=(12, 6))
plt.bar(df['Product_Name'], df['Historical_Demand'], alpha=0.6, label='Historical Demand')
plt.bar(df['Product_Name'], df['Forecasted_Demand'], alpha=0.6, label='Forecasted Demand')
plt.xlabel('Product Name')
plt.ylabel('Demand')
plt.title('Historical vs Forecasted Demand')
plt.xticks(rotation=90)
plt.legend()
st.pyplot(fig)

buffer_stock_counts = df.groupby('Product_Name')['Emergency_Buffer_Stock'].sum().reset_index()
fig_pie = px.pie(buffer_stock_counts, names='Product_Name', values='Emergency_Buffer_Stock',
                 title="Emergency Buffer Stock Distribution",
                 labels={'Product_Name': 'Product', 'Emergency_Buffer_Stock': 'Buffer Stock'},
                 color_discrete_sequence=px.colors.sequential.Plasma)

# Enhance hover information
fig_pie.update_traces(
    hovertemplate="<b>%{label}</b><br>Buffer Stock: %{value}<br>Percentage: %{percent:.2%}<extra></extra>"
)

# Add customization for better visual appeal
fig_pie.update_layout(
    title_font_size=24,
    legend_title_text='Products',
    legend_title_font_size=18,
    legend_font_size=14,
    margin=dict(l=0, r=0, t=40, b=0)
)

st.plotly_chart(fig_pie)

# Create a line chart for historical and forecasted demand trends over time
st.subheader("Demand Trends Over Time")
df['Date'] = pd.date_range(start='2023-01-01', periods=100)
df.set_index('Date', inplace=True)
fig_trend = px.line(df, x=df.index, y=['Historical_Demand', 'Forecasted_Demand'],
                    title="Historical and Forecasted Demand Trends")
st.plotly_chart(fig_trend)
