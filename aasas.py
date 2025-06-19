import streamlit as st # type: ignore
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page settings
st.set_page_config(page_title="Retail Sales Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("https://raw.githubusercontent.com/leonism/sample-superstore/refs/heads/master/data/superstore.csv", parse_dates=["Order Date", "Ship Date"])
    df['Year-Month'] = df['Order Date'].dt.to_period('M').astype(str)
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("📊 Filter Data")

categories = st.sidebar.multiselect("Select Category", options=df['Category'].unique(), default=df['Category'].unique())
regions = st.sidebar.multiselect("Select Region", options=df['Region'].unique(), default=df['Region'].unique())
date_range = st.sidebar.date_input("Select Date Range", [df['Order Date'].min(), df['Order Date'].max()])

# Filter data
filtered_df = df[
    (df['Category'].isin(categories)) &
    (df['Region'].isin(regions)) &
    (df['Order Date'] >= pd.to_datetime(date_range[0])) &
    (df['Order Date'] <= pd.to_datetime(date_range[1]))
]

# KPI Section
st.title("📈 Superstore Sales Dashboard")
st.markdown("### Performance Summary")

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${filtered_df['Sales'].sum():,.2f}")
col2.metric("Total Profit", f"${filtered_df['Profit'].sum():,.2f}")
col3.metric("Total Orders", f"{filtered_df['Order ID'].nunique()}")

# Charts
st.markdown("### 📊 Monthly Sales Trend")
monthly_sales = filtered_df.groupby("Year-Month")["Sales"].sum()

fig1, ax1 = plt.subplots()
monthly_sales.plot(kind="line", marker="o", ax=ax1)
ax1.set_xlabel("Month")
ax1.set_ylabel("Sales")
ax1.set_title("Sales Trend Over Time")
st.pyplot(fig1)

st.markdown("### 📊 Profit by Category")
fig2, ax2 = plt.subplots()
sns.barplot(data=filtered_df, x="Category", y="Profit", estimator=sum, ci=None, ax=ax2)
ax2.set_title("Total Profit by Category")
st.pyplot(fig2)

st.markdown("### 📍 Sales by Region")
fig3, ax3 = plt.subplots()
sns.boxplot(data=filtered_df, x="Region", y="Sales", ax=ax3)
ax3.set_title("Sales Distribution by Region")
st.pyplot(fig3)

# Top Products Table
st.markdown("### 🏆 Top 10 Products by Sales")
top_products = filtered_df.groupby("Product Name")["Sales"].sum().sort_values(ascending=False).head(10)
st.dataframe(top_products.reset_index())
