import streamlit as st
import pandas as pd
import os

# Page Configuration
st.set_page_config(page_title="My Fashion - Live Dashboard", layout="wide")

st.title("🛍️ MY FASHION — Live Business Portal")
st.markdown("Access your boutique inventory and sales live from any phone or device.")
st.write("---")

DB_FILE = "my_fashion_data.xlsx"

# Load or Initialize Data
def load_data():
    if os.path.exists(DB_FILE):
        try:
            with pd.ExcelFile(DB_FILE) as xls:
                prod_df = pd.read_excel(xls, 'Products') if 'Products' in xls.sheet_names else pd.DataFrame(columns=["Item/Design Name", "Cost Price (CP)", "Selling Price (SP)"])
                sales_df = pd.read_excel(xls, 'Sales') if 'Sales' in xls.sheet_names else pd.DataFrame(columns=["Item/Design Name", "Quantity Sold", "Total Revenue", "Total Cost", "Profit (20%)"])
                return prod_df, sales_df
        except Exception:
            pass
    return pd.DataFrame(columns=["Item/Design Name", "Cost Price (CP)", "Selling Price (SP)"]), pd.DataFrame(columns=["Item/Design Name", "Quantity Sold", "Total Revenue", "Total Cost", "Profit (20%)"])

def save_data(prod_df, sales_df):
    with pd.ExcelWriter(DB_FILE, engine='openpyxl') as writer:
        prod_df.to_excel(writer, sheet_name='Products', index=False)
        sales_df.to_excel(writer, sheet_name='Sales', index=False)

products_df, sales_df = load_data()

# --- SIDEBAR: ADD ITEM ---
st.sidebar.header("➕ Add New Clothing Item")
with st.sidebar.form("product_form", clear_on_submit=True):
    p_name = st.text_input("Item Name").strip()
    cp = st.number_input("Cost Price (Per Piece)", min_value=0.0, format="%.2f")
    submit_p = st.form_submit_button("Add to Collection")

    if submit_p and p_name and cp > 0:
        if p_name in products_df["Item/Design Name"].values:
            st.sidebar
