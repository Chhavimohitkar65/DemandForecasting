import streamlit as st
from pymongo import MongoClient
from datetime import datetime

# MongoDB connection string
mongo_uri = "mongodb+srv://chhavimohitkar06:123@cluster0.3oybioi.mongodb.net/"
client = MongoClient(mongo_uri)

# Databases
db_inventory = client['inventory_database']
categories_collection = db_inventory['categories']
db_compliance = client['historical_inventory_database']

# Initialize session state
if 'active_section' not in st.session_state:
    st.session_state['active_section'] = None

# Functions for Expiry Tracking
def add_update_expiry(category, product_id, expiry_date):
    product_collection = db_inventory[f'{category}_collection']
    try:
        expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d')
    except ValueError:
        st.error("Invalid date format for Expiry Date.")
        return

    product_collection.update_one(
        {"Product_ID": product_id},
        {"$set": {"Expiry_Date": expiry_date.strftime('%Y-%m-%d')}},
        upsert=True
    )

    st.success("Expiry date added/updated successfully.")

def check_expired_products():
    expired_products = []
    for category in categories_collection.distinct("Category"):
        product_collection = db_inventory[f'{category}_collection']
        products = product_collection.find({"Expiry_Date": {"$exists": True}})
        for product in products:
            expiry_date = datetime.strptime(product['Expiry_Date'], '%Y-%m-%d')
            if expiry_date < datetime.now():
                expired_products.append((category, product['Product_ID'], product['Expiry_Date']))

    return expired_products

# Functions for Regulatory Compliance
def check_compliance(category, product_id):
    collection = db_compliance[category]
    product = collection.find_one({'Product_ID': product_id})

    if product:
        current_date = datetime.now().date()
        expiry_date = datetime.strptime(product['Expiry_Date'], '%Y-%m-%d').date()
        expiry_compliance = "Compliant" if expiry_date > current_date else "Non-Compliant"
        temperature_requirement = product['Temperature_Requirement']
        temperature_compliance = "Compliant" if temperature_requirement in ["Room Temperature", "Cool Storage"] else "Non-Compliant"

        return {
            "Expiry Date": expiry_compliance,
            "Storage Temperature": temperature_compliance
        }
    else:
        return None

# Functions for Temperature-Sensitive Inventory Management
def manage_temperature_sensitive_inventory(category, product_id, storage_temp):
    product_collection = db_inventory[f'{category}_collection']
    product_collection.update_one(
        {"Product_ID": product_id},
        {"$set": {"Storage_Temperature": storage_temp}},
        upsert=True
    )

    st.success("Storage temperature updated successfully.")

# Streamlit app layout


# Place buttons in a row
col1, col2, col3 = st.columns(3)
if col1.button("Expiry Tracking"):
    st.session_state['active_section'] = 'expiry_tracking'
if col2.button("Regulatory Compliance"):
    st.session_state['active_section'] = 'regulatory_compliance'
if col3.button("Temperature Sensitive "):
    st.session_state['active_section'] = 'temperature_sensitive_inventory'

# Display content based on the active section
if st.session_state['active_section'] == 'expiry_tracking':
   

    # Display Expired Products
 
    expired_products = check_expired_products()
    if expired_products:
        for category, product_id, expiry_date in expired_products:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.warning(f"Product ID: {product_id} in Category: {category} expired on {expiry_date}")
            with col2:
                done = st.checkbox("Done", key=f"{category}_{product_id}")
                if done:
                    product_collection = db_inventory[f'{category}_collection']
                    product_collection.update_one(
                        {"Product_ID": product_id},
                        {"$unset": {"Expiry_Date": ""}}
                    )
                    st.experimental_rerun()
    else:
        st.success("No expired products found.")
    # Add/Update Expiry Date Form
    st.subheader("Add/Update Expiry Date")
    categories = categories_collection.distinct("Category")
    selected_category = st.selectbox("Select a category:", categories)
    product_id = st.text_input("Enter Product ID:")
    expiry_date = st.date_input("Enter Expiry Date:", value=datetime.now())

    if st.button("Add/Update Expiry Date"):
        add_update_expiry(selected_category, product_id, expiry_date.strftime('%Y-%m-%d'))

elif st.session_state['active_section'] == 'regulatory_compliance':
  

    # Regulatory Compliance Check Form
    st.subheader("Regulatory Compliance Check")
    category = st.selectbox("Select a category:", ["Medical Supplies", "Medication", "Medical Equipment"])
    product_id = st.text_input("Enter Product ID:")

    if st.button("Check Compliance"):
        if product_id:
            compliance_status = check_compliance(category, product_id)
            if compliance_status:
                st.subheader("Compliance Status:")
                st.json(compliance_status)
            else:
                st.error("Product not found.")
        else:
            st.error("Please enter a Product ID.")

elif st.session_state['active_section'] == 'temperature_sensitive_inventory':
   

    # Temperature-Sensitive Inventory Management Form
    st.subheader("Temperature-Sensitive")
    categories = categories_collection.distinct("Category")
    selected_category = st.selectbox("Select a category:", categories)
    product_id = st.text_input("Enter Product ID:")
    storage_temp = st.text_input("Enter Storage Temperature Requirement:")

    if st.button("Update Storage Temperature"):
        manage_temperature_sensitive_inventory(selected_category, product_id, storage_temp)
