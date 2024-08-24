import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Set page configuration
st.set_page_config(page_title="Healthcare Inventory Dashboard", layout="wide")

# Generate random data for overview
def generate_random_data():
    product_sales = {
        "Product": ["Bandages", "Gloves", "Syringes", "Masks", "Thermometers", "Stethoscopes", "Wheelchairs"],
        "Revenue": [12000, 8200, 5400, 27000, 1200, 4800, 11000],
        "Purchase Cost": [6000, 4100, 2700, 13500, 600, 2400, 5500]
    }
    df_sales = pd.DataFrame(product_sales)

    expenses_breakdown = {
        "Category": ["Cost of Goods Sold (COGS)", "Advertising"],
        "Amount": [55300, 8300]
    }
    df_expenses = pd.DataFrame(expenses_breakdown)

    return df_sales, df_expenses



tabs = st.sidebar.selectbox("Choose an action", ["Home", "Stock Report", "Historic Data"])

if tabs == "Home":
    st.markdown(
        """
        <style>
        .reportview-container {
            background: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 10px 20px;
            text-align: center;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
        }
        .stTextInput>div>div>input {
            padding: 10px;
            border-radius: 4px;
            border: 1px solid #ccc;
        }
        .stDateInput>div>div>input {
            padding: 10px;
            border-radius: 4px;
            border: 1px solid #ccc;
        }
        .stMetric>div {
            padding: 20px;
            border-radius: 10px;
            background: #ffffff;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .metric-box {
            background-color: #f8f9fa;  /* Light grey background */
            border: 1px solid #dee2e6;  /* Light grey border */
            border-radius: 8px;
            padding: 15px;
            text-align: center;
            margin-bottom: 15px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        }
        .total-categories { background-color: #d3f9d8; }  /* Pastel green */
        .total-items { background-color: #d0e9f5; }       /* Pastel blue */
        .remaining-stock { background-color: #f9d6d5; }   /* Pastel red */
        .out-of-stock { background-color: #fef6d0; }      /* Pastel yellow */
        .donut-chart {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 300px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


    
    # Generate random data
    df_sales, df_expenses = generate_random_data()

    # Inventory Summary
    st.markdown("### Inventory Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="metric-box total-categories">
                <h3>Total Categories</h3>
                <p style="font-size: 24px; color: #007bff;">10</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-box total-items">
                <h3>Total Items</h3>
                <p style="font-size: 24px; color: #28a745;">150</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="metric-box remaining-stock">
                <h3>Remaining Stock</h3>
                <p style="font-size: 24px; color: #17a2b8;">120</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="metric-box out-of-stock">
                <h3>Out of Stock Products</h3>
                <p style="font-size: 24px; color: #dc3545;">5</p>
            </div>
            """, unsafe_allow_html=True)

    # Stock Availability Status (Donut Chart)
    st.markdown("### Stock Availability Status")
    stock_status_summary = {
        "Out of Stock": 5,
        "Low Stock": 10,
        "Medium Stock": 25,
        "High Stock": 60
    }
    df_stock_status = pd.DataFrame(list(stock_status_summary.items()), columns=['Status', 'Count'])
    
    fig_donut = px.pie(df_stock_status, names='Status', values='Count', hole=0.4, title='Stock Availability Status', color_discrete_sequence=px.colors.sequential.Plasma)
    fig_donut.update_traces(textinfo='percent+label', textfont_size=15)
    
    st.plotly_chart(fig_donut, use_container_width=True, height=300, config={'displayModeBar': False})

    # Financial Summary
    st.markdown("### Financial Summary")
    col1, col2, col3 = st.columns(3)
    revenue = 90700.00
    expenses = 63600.00
    profit = revenue - expenses
    col1.metric("Revenue", f"${revenue:,.2f}")
    col2.metric("Expenses", f"${expenses:,.2f}")
    col3.metric("Profit", f"${profit:,.2f}")

    # Revenue and Purchase Cost Chart
  
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_sales["Product"], y=df_sales["Revenue"], name="Revenue", marker_color='royalblue'))
    fig.add_trace(go.Bar(x=df_sales["Product"], y=df_sales["Purchase Cost"], name="Purchase Cost", marker_color='firebrick'))
    fig.update_layout(
        title="Revenue and Purchase Cost",
        xaxis_title="Product",
        yaxis_title="Amount ($)",
        barmode="group",
        template="plotly_dark"  # Dark mode for better contrast
    )
    st.plotly_chart(fig, use_container_width=True)

    # Expenses Breakdown
    fig_pie = px.pie(df_expenses, names='Category', values='Amount', hole=0.3, title='Expenses Breakdown', color_discrete_sequence=px.colors.sequential.Plasma)
    fig_pie.update_traces(textinfo='percent+label', textfont_size=15)
    st.plotly_chart(fig_pie, use_container_width=True)

    # Top 3 Highest Sales Products
    st.markdown("### Top 3 Highest Sales Products")
    top_3_products = df_sales.nlargest(3, 'Revenue')[["Product", "Revenue"]]
    st.table(top_3_products)

  

elif tabs == "Stock Report":
    st.header("Stock Report Management")
    action = st.selectbox("Select an action", ["Add", "Update", "Delete", "View"])

    if action == "Add":
        with st.form("stock_report_form"):
            category = st.text_input("Category")
            product_id = st.text_input("Product ID")
            product_name = st.text_input("Product Name")
            stock_level = st.text_input("Stock Level")
            date_updated = st.date_input("Date Updated", datetime.today())
            max_capacity = st.text_input("Max Capacity")

            submit = st.form_submit_button("Submit")

            if submit:
                create_or_update_stock_report(category, product_id, product_name, stock_level, date_updated.strftime('%Y-%m-%d'), max_capacity)
                st.success("Stock report added successfully!")

    elif action == "Update":
        with st.form("update_stock_report_form"):
            category = st.text_input("Category")
            product_id = st.text_input("Product ID")
            product_name = st.text_input("Product Name")
            stock_level = st.text_input("Stock Level")
            date_updated = st.date_input("Date Updated", datetime.today())
            max_capacity = st.text_input("Max Capacity")

            submit = st.form_submit_button("Update")

            if submit:
                create_or_update_stock_report(category, product_id, product_name, stock_level, date_updated.strftime('%Y-%m-%d'), max_capacity)
                st.success("Stock report updated successfully!")

    elif action == "Delete":
        with st.form("delete_stock_report_form"):
            category = st.text_input("Category")
            product_id = st.text_input("Product ID")

            submit = st.form_submit_button("Delete")

            if submit:
                if st.confirm("Are you sure you want to delete this record?"):
                    delete_stock_report(category, product_id)
                    st.success("Stock report deleted successfully!")

    elif action == "View":
        view_data_by_category()

elif tabs == "Historic Data":
    st.header("Historical Data Upload")
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file:
        upload_historical_data(uploaded_file)
