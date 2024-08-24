import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np

st.set_page_config(layout="wide")

# Initialize global variables with default values
out_of_stock_products = 0
low_stock_products = 0
arriving_products = 0
weighted_score_low_stock = 0
weighted_score_arriving_stock = 0
weighted_score_out_of_stock = 0
predicted_stock_level = 70  # Example predicted stock level

# Function to calculate the stock status
def calculate_status(row):
    if row['Stock_Level'] == 0:
        return 'out_of_stock'
    elif row['Stock_Level'] < row['Max_Capacity'] * 0.2:
        return 'low_stock'
    elif row['Stock_Level'] > row['Max_Capacity'] * 0.2 and row['Stock_Level'] < row['Max_Capacity']:
        return 'arriving'
    else:
        return 'in_stock'

# Function to update metrics and charts based on uploaded data
def update_metrics(df):
    global out_of_stock_products, low_stock_products, arriving_products
    global weighted_score_low_stock, weighted_score_arriving_stock, weighted_score_out_of_stock

    df['status'] = df.apply(calculate_status, axis=1)

    out_of_stock_products = df[df['status'] == 'out_of_stock']['Product_Name'].count()
    low_stock_products = df[df['status'] == 'low_stock']['Product_Name'].count()
    arriving_products = df[df['status'] == 'arriving']['Product_Name'].count()

    total_products = len(df)
    weighted_score_low_stock = (low_stock_products / total_products) * 100 if total_products > 0 else 0
    weighted_score_arriving_stock = (arriving_products / total_products) * 100 if total_products > 0 else 0
    weighted_score_out_of_stock = (out_of_stock_products / total_products) * 100 if total_products > 0 else 0

    return df

# Load the processed inventory data
def load_data():
    try:
        return pd.read_csv('daily.csv')
    except FileNotFoundError:
        return None

# Main function to control the Streamlit app
def main():
    global out_of_stock_products, low_stock_products, arriving_products
    global weighted_score_low_stock, weighted_score_arriving_stock, weighted_score_out_of_stock
    global predicted_stock_level

    st.markdown("<h1 style='text-align: ; color: #000000;'>SmartCast Your Stock Control </h1>", unsafe_allow_html=True)
    st.image('https://plus.unsplash.com/premium_vector-1682269150539-926ee2aabab6?q=80&w=1740&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', use_column_width=True)
    # App Title
    # Load data and update metrics
    df = load_data()

    if df is not None:
        df = update_metrics(df)
    else:
        # Initialize metrics with default values
        out_of_stock_products = 0
        low_stock_products = 0
        arriving_products = 0
        weighted_score_low_stock = 0
        weighted_score_arriving_stock = 0
        weighted_score_out_of_stock = 0

    # Metrics
    st.markdown("<h3 style='text-align: center; color: #333;'>Inventory Metrics</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div style='background-color: #ffcccc; padding: 10px; border-radius: 10px;'>"
                    f"<h2 style='text-align: center;'>{out_of_stock_products}</h2>"
                    "<p style='text-align: center;'>Out of stock products</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div style='background-color: #ffffcc; padding: 10px; border-radius: 10px;'>"
                    f"<h2 style='text-align: center;'>{low_stock_products}</h2>"
                    "<p style='text-align: center;'>Products on low stock</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div style='background-color: #CBC3E3; padding: 10px; border-radius: 10px;'>"
                    f"<h2 style='text-align: center;'>{arriving_products}</h2>"
                    "<p style='text-align: center;'>Products arriving soon</p></div>", unsafe_allow_html=True)

    # Interactive Controls
    st.sidebar.markdown("<h3 style='text-align: center; color: #333;'>Adjust Predicted Stock Level</h3>", unsafe_allow_html=True)
    predicted_stock_level = st.sidebar.slider('Predicted Stock Level', min_value=0, max_value=200, value=predicted_stock_level, step=1)

    # Update Metrics Button
    if st.sidebar.button('Update Metrics'):
        df = load_data()
        if df is not None:
            df = update_metrics(df)

    # Charts
    st.markdown("<h3 style='text-align: center; color: #333;'>Inventory Status Overview</h3>", unsafe_allow_html=True)
    col4, col5 = st.columns(2)
    with col4:
        # Weighted Score Pie Chart
        labels = ['Low Stock', 'Arriving Stock', 'Out of Stock']
        sizes = [weighted_score_low_stock, weighted_score_arriving_stock, weighted_score_out_of_stock]
        colors = ['#61a4b2', '#a3e3c3', '#f9a6a6']

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig1)

    with col5:
        # Pyramid Chart for Stock Levels
        fig2, ax2 = plt.subplots()
        ax2.barh(['Products on Low Stock'], [low_stock_products], color='#e74c3c', label='Low Stock')
        ax2.barh(['Products Arriving Soon'], [arriving_products], color='#f39c12', left=[low_stock_products], label='Arriving Soon')
        ax2.barh(['Products Out of Stock'], [out_of_stock_products], color='#3498db', left=[low_stock_products + arriving_products], label='Out of Stock')

        ax2.set_xlabel('Number of Products')
        ax2.set_title('Inventory Pyramid')
        ax2.legend()

        st.pyplot(fig2)

    # Example: Predicted vs Actual Stock Levels
    st.markdown("<h3 style='text-align: center; color: #333;'>Example: Predicted vs Actual Stock Levels</h3>", unsafe_allow_html=True)
    if df is not None and 'Stock_Level' in df.columns:
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=np.arange(len(df)), y=df['Stock_Level'], mode='lines+markers', name='Actual Stock Level', line=dict(color='royalblue', width=2)))
        fig3.add_trace(go.Scatter(x=np.arange(len(df)), y=[predicted_stock_level] * len(df), mode='lines', name='Predicted Stock Level', line=dict(color='firebrick', width=2, dash='dash')))
        fig3.update_layout(title='Predicted vs Actual Stock Levels',
                           xaxis_title='Time',
                           yaxis_title='Stock Level',
                           legend=dict(x=0, y=1, traceorder='normal'))
        st.plotly_chart(fig3)
    else:
        st.write("No data available to display example chart.")

# Initialize session state for navigation
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

if __name__ == "__main__":
    main()
