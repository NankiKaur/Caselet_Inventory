import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Global Style ---
plt.style.use("ggplot")  # Clean and compatible with Streamlit themes

# --- Page Config ---
st.set_page_config(page_title="Inventory KPI Dashboard", layout="wide")

# --- Title ---
st.title("📦 Inventory KPI Dashboard")

# --- Load Data ---
df = pd.read_csv("inventory_forecasting.csv")

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filters")
categories = df["Category"].unique()
selected_category = st.sidebar.selectbox("Select Product Category", options=categories)

regions = df["Region"].unique()
selected_region = st.sidebar.selectbox("Select Store Region", options=regions)

# --- Apply Filters ---
filtered_df = df[(df["Category"] == selected_category) & (df["Region"] == selected_region)]

st.markdown(f"### Showing data for **{selected_category}** in **{selected_region}** region")

# --- KPI Metrics ---
col1, col2, col3 = st.columns(3)

with col1:
    total_inventory = int(filtered_df["Inventory Level"].sum())
    st.metric("📦 Total Inventory", total_inventory)

with col2:
    turnover_ratio = filtered_df["Units Sold"].sum() / filtered_df["Inventory Level"].sum()
    st.metric("🔁 Avg Turnover Ratio", f"{turnover_ratio:.2f}")

with col3:
    stockout_rate = (filtered_df["Units Sold"] >= filtered_df["Inventory Level"]).mean()
    st.metric("⚠️ Stockout Rate", f"{stockout_rate:.1%}")

# --- Tabs for Charts ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Avg Inventory",
    "⚡ Fast Movers",
    "⚠️ Stockout Rate",
    "🔁 Turnover Ratio",
    "🏷️ Discount by Category"
])

# --- Tab 1: Avg Inventory by Category ---
with tab1:
    st.subheader("📊 Avg Inventory Level by Category")
    inventory_by_category = filtered_df.groupby("Category")["Inventory Level"].mean().sort_values(ascending=False)
    fig1, ax1 = plt.subplots(figsize=(6, 2.5), facecolor='none')
    fig1.patch.set_alpha(0.0)
    ax1.set_facecolor('none')
    inventory_by_category.plot(kind='barh', ax=ax1, color='tomato')
    ax1.set_xlabel("Inventory Level", labelpad=10)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.grid(axis="x", linestyle="--", alpha=0.3)
    st.pyplot(fig1)

# --- Tab 2: Fast Moving Products ---
with tab2:
    st.subheader("⚡ Top 10 Fast Moving Products (Avg Units Sold)")
    product_sales = filtered_df.groupby("Product ID")["Units Sold"].mean().sort_values(ascending=False)
    fig2, ax2 = plt.subplots(figsize=(6, 2.5), facecolor='none')
    fig2.patch.set_alpha(0.0)
    ax2.set_facecolor('none')
    product_sales.head(10).plot(kind='bar', ax=ax2, color='limegreen')
    ax2.set_ylabel("Avg Units Sold")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.grid(axis="y", linestyle="--", alpha=0.3)
    st.pyplot(fig2)

# --- Tab 3: Stockout Rate ---
with tab3:
    st.subheader("⚠️ Stockout Rate by Category")
    filtered_df["Stockout"] = filtered_df["Units Sold"] >= filtered_df["Inventory Level"]
    stockout_rate = filtered_df.groupby("Category")["Stockout"].mean().sort_values(ascending=False)
    fig3, ax3 = plt.subplots(figsize=(6, 2.5), facecolor='none')
    fig3.patch.set_alpha(0.0)
    ax3.set_facecolor('none')
    stockout_rate.plot(kind='barh', ax=ax3, color='salmon')
    ax3.set_xlabel("Stockout Frequency")
    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)
    ax3.grid(axis="x", linestyle="--", alpha=0.3)
    st.pyplot(fig3)

# --- Tab 4: Turnover Ratio ---
with tab4:
    st.subheader("🔁 Inventory Turnover Ratio (Top 10)")
    turnover = filtered_df.groupby("Product ID").agg({
        "Units Sold": "sum",
        "Inventory Level": "mean"
    })
    turnover["Turnover Ratio"] = turnover["Units Sold"] / turnover["Inventory Level"]
    turnover_sorted = turnover["Turnover Ratio"].sort_values(ascending=False)
    fig4, ax4 = plt.subplots(figsize=(6, 2.5), facecolor='none')
    fig4.patch.set_alpha(0.0)
    ax4.set_facecolor('none')
    turnover_sorted.head(10).plot(kind='bar', ax=ax4, color='purple')
    ax4.set_ylabel("Turnover Ratio")
    ax4.spines["top"].set_visible(False)
    ax4.spines["right"].set_visible(False)
    ax4.grid(axis="y", linestyle="--", alpha=0.3)
    st.pyplot(fig4)

# --- Tab 5: Discount by Category ---
with tab5:
    st.subheader("🏷️ Avg Discount by Category")
    discount_by_category = filtered_df.groupby("Category")["Discount"].mean().sort_values(ascending=False)
    fig5, ax5 = plt.subplots(figsize=(6, 2.5), facecolor='none')
    fig5.patch.set_alpha(0.0)
    ax5.set_facecolor('none')
    discount_by_category.plot(kind='barh', ax=ax5, color='orange')
    ax5.set_xlabel("Avg Discount (%)")
    ax5.spines["top"].set_visible(False)
    ax5.spines["right"].set_visible(False)
    ax5.grid(axis="x", linestyle="--", alpha=0.3)
    st.pyplot(fig5)
