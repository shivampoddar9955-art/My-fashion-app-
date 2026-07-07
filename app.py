import streamlit as st
import pandas as pd
import os

# Page Configuration (Mobile Friendly Layout)
st.set_page_config(page_title="My Fashion - Live Dashboard", layout="wide")

# Branding Header
st.title("🛍️ MY FASHION — Live Business Portal")
st.markdown("Access your boutique inventory and sales live from any phone or device.")
st.write("---")

DB_FILE = "my_fashion_data.xlsx"

# Load or Initialize Data
def load_data():
    if os.path.exists(DB_FILE):
        with pd.ExcelFile(DB_FILE) as xls:
            prod_df = pd.read_excel(xls, 'Products') if 'Products' in xls.sheet_names else pd.DataFrame(columns=["Item/Design Name", "Cost Price (CP)", "Selling Price (SP)"])
            sales_df = pd.read_excel(xls, 'Sales') if 'Sales' in xls.sheet_names else pd.DataFrame(columns=["Item/Design Name", "Quantity Sold", "Total Revenue", "Total Cost", "Profit (20%)"])
            return prod_df, sales_df
    return pd.DataFrame(columns=["Item/Design Name", "Cost Price (CP)", "Selling Price (SP)"]), pd.DataFrame(columns=["Item/Design Name", "Quantity Sold", "Total Revenue", "Total Cost", "Profit (20%)"])

def save_data(prod_df, sales_df):
    with pd.ExcelWriter(DB_FILE, engine='openpyxl') as writer:
        prod_df.to_excel(writer, sheet_name='Products', index=False)
        sales_df.to_excel(writer, sheet_name='Sales', index=False)

products_df, sales_df = load_data()

# --- MAIN DASHBOARD WITH ICONS ---
st.subheader("📊 Business Performance & Profit Overview")
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

if not sales_df.empty:
    total_rev = sales_df["Total Revenue"].sum()
    total_cost = sales_df["Total Cost"].sum()
    total_prof = sales_df["Profit (20%)"].sum()
    
    col1.metric("💰 Total Sales", f"₹{total_rev:,.2f}")
    col2.metric("📉 Total Cost", f"₹{total_cost:,.2f}")
    col3.metric("📈 Net Profit (20%)", f"₹{total_prof:,.2f}", delta="🟢 Profit Safe")
    col4.metric("📦 Clothes Sold", f"{int(sales_df['Quantity Sold'].sum())} Pcs")
else:
    col1.metric("💰 Total Sales", "₹0.00")
    col2.metric("📉 Total Cost", "₹0.00")
    col3.metric("📈 Net Profit (20%)", "₹0.00", delta="No Sales Yet")
    col4.metric("📦 Clothes Sold", "0 Pcs")

st.write("---")

# --- NO SIDEBAR: ALL ACTIONS IN EASY TABS ---
st.subheader("🛠️ Management Actions")
action_tab1, action_tab2, action_tab3, action_tab4 = st.tabs([
    "🛒 SELL ITEM (Record Sale)", 
    "➕ ADD NEW ITEM", 
    "📊 SALES HISTORY LOG", 
    "📦 STOCK / INVENTORY"
])

# 1. SELL ITEM TAB
with action_tab1:
    st.markdown("### 🛒 Log a New Sale Here")
    if not products_df.empty:
        with st.form("sale_form_main", clear_on_submit=True):
            selected_p = st.selectbox("Select Sold Item", products_df["Item/Design Name"].tolist(), key="main_sale_select")
            qty = st.number_input("Quantity Sold", min_value=1, step=1, key="main_sale_qty")
            submit_s = st.form_submit_with_button("🎉 Complete Sale (Sell)")

            if submit_s:
                p_details = products_df[products_df["Item/Design Name"] == selected_p].iloc[0]
                rev = p_details["Selling Price (SP)"] * qty
                cost = p_details["Cost Price (CP)"] * qty
                profit = rev - cost
                
                new_sale = pd.DataFrame([[selected_p, qty, rev, cost, profit]], columns=sales_df.columns)
                sales_df = pd.concat([sales_df, new_sale], ignore_index=True)
                save_data(products_df, sales_df)
                st.success(f"💥 Sale Recorded for {selected_p}! Profit updated.")
                st.rerun()
    else:
        st.info("⚠️ Pehle 'ADD NEW ITEM' tab mein jaakar apne kapde add kariye, uske baad yahan sell kar payenge.")

# 2. ADD ITEM TAB
with action_tab2:
    st.markdown("### ➕ Add New Clothing Item to Stock")
    with st.form("product_form_main", clear_on_submit=True):
        p_name = st.text_input("Item Name (e.g., Saree, Kurti, Jeans)", key="main_prod_name").strip()
        cp = st.number_input("Cost Price Per Piece (₹)", min_value=0.0, format="%.2f", key="main_prod_cp")
        submit_p = st.form_submit_with_button("📦 Add to My Fashion Collection")

        if submit_p and p_name and cp > 0:
            if p_name in products_df["Item/Design Name"].values:
                st.error("This item already exists in your inventory!")
            else:
                sp = cp * 1.20
                new_p = pd.DataFrame([[p_name, cp, sp]], columns=products_df.columns)
                products_df = pd.concat([products_df, new_p], ignore_index=True)
                save_data(products_df, sales_df)
                st.success(f"✅ Added {p_name}! Selling Price automatically set to ₹{sp:.2f} (20% Profit included)")
                st.rerun()

# 3. SALES HISTORY TAB
with action_tab3:
    st.markdown("### 📝 History of Items Sold")
    if not sales_df.empty:
        st.dataframe(sales_df, use_container_width=True)
    else:
        st.info("No sales tracked yet.")

# 4. INVENTORY TAB
with action_tab4:
    st.markdown("### 🏷️ Available Items & Calculated Prices")
    if not products_df.empty:
        st.dataframe(products_df, use_container_width=True)
    else:
        st.info("Inventory is empty.")
