import streamlit as st
from utils.auth_config import get_authenticator

# Get authenticator
authenticator, config = get_authenticator()

# Login interface
name, auth_status, username = authenticator.login('Login', 'main')

if auth_status is False:
    st.error('❌ Incorrect username or password.')
elif auth_status is None:
    st.warning('⚠️ Please enter your credentials.')
elif auth_status:
    # If logged in, show the app
    authenticator.logout('Logout', 'sidebar')
    st.sidebar.success(f"Welcome, {name} 👋")

    # Paste your original Streamlit app logic below this line
    # -------------------- PAGE CONFIG --------------------
    st.set_page_config(page_title="Retail Sales Dashboard", layout="wide")
    import streamlit as st
import pandas as pd
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Retail Sales Dashboard", layout="wide")

# -------------------- BACKGROUND STYLING --------------------
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(to right, #c4fda1, #c2e9fb, #cfa1fd);
            animation: gradient 15s ease infinite;
            background-size: 400% 400%;
        }
        @keyframes gradient {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }
    </style>
""", unsafe_allow_html=True)

# -------------------- DATABASE SETUP --------------------
engine = sqlalchemy.create_engine('sqlite:///sales.db')
Session = sessionmaker(bind=engine)
session = Session()

def save_to_db(df):
    try:
        df.columns = df.columns.str.strip().str.lower()
        if 'date' not in df.columns:
            st.error("❌ Column 'date' not found in uploaded file.")
            return False
        df['date'] = pd.to_datetime(df['date'])
        df.to_sql('sales', engine, if_exists='append', index=False)
        return True
    except Exception as e:
        st.error(f"Error saving to DB: {e}")
        return False

def load_data():
    try:
        df = pd.read_sql("SELECT * FROM sales", engine)
        return df
    except:
        return pd.DataFrame()

# -------------------- MENU --------------------
menu = ["Upload Data", "View Data", "Dashboard"]
choice = st.sidebar.selectbox("Navigate", menu)

if choice == "Upload Data":
    st.subheader("Upload Sales CSV File")

    with st.expander("📌 CSV Format Example"):
        st.markdown("""
        | date       | product     | region  | units_sold | revenue |
        |------------|-------------|---------|------------|---------|
        | 2024-06-01 | Widget A    | East    | 10         | 100     |
        | 2024-06-02 | Widget B    | West    | 5          | 50      |
        """)

    file = st.file_uploader("Upload CSV", type=["csv"])
    if file:
        try:
            df = pd.read_csv(file, encoding='latin1')
            st.write("✅ Preview of uploaded data:")
            st.dataframe(df)

            if st.button("Save to Database"):
                success = save_to_db(df)
                if success:
                    st.success("✅ Data saved to database!")
        except Exception as e:
            st.error(f"❌ Error reading file: {e}")

elif choice == "View Data":
    st.subheader("📑 View Stored Sales Data")
    data = load_data()
    if data.empty:
        st.warning("⚠ No data found. Please upload some CSVs first.")
    else:
        st.dataframe(data)

elif choice == "Dashboard":
    st.subheader("📊 Sales Dashboard")
    data = load_data()
    if data.empty:
        st.warning("⚠ No data found. Please upload some CSVs first.")
    else:
        data['date'] = pd.to_datetime(data['date'])

        col1, col2 = st.columns(2)
        with col1:
            region = st.selectbox("Select Region", ["All"] + sorted(data['region'].unique()))
        with col2:
            product = st.selectbox("Select Product", ["All"] + sorted(data['product'].unique()))

        if region != "All":
            data = data[data['region'] == region]
        if product != "All":
            data = data[data['product'] == product]

        st.markdown("### 📈 Key Performance Indicators")
        col1, col2 = st.columns(2)
        col1.metric("Total Revenue", f"${data['revenue'].sum():,.2f}")
        col2.metric("Total Units Sold", f"{data['units_sold'].sum():,.0f}")

        daily = data.groupby('date').agg({'revenue': 'sum', 'units_sold': 'sum'}).reset_index()

        st.markdown("### 📅 Revenue Over Time")
        fig1 = px.line(daily, x='date', y='revenue', markers=True)
        st.plotly_chart(fig1, use_container_width=True)

        st.markdown("### 📅 Units Sold Over Time")
        fig2 = px.line(daily, x='date', y='units_sold', markers=True)
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown("### 🥇 Top Selling Products")
        top_products = data.groupby('product').agg({'revenue': 'sum'}).reset_index().sort_values(by='revenue', ascending=False)
        fig3 = px.bar(top_products, x='product', y='revenue', text_auto=True)
        st.plotly_chart(fig3, use_container_width=True)

        st.markdown("### 🌍 Region vs Product Heatmap")
        pivot = data.pivot_table(values='revenue', index='region', columns='product', aggfunc='sum', fill_value=0)
        fig4, ax = plt.subplots()
        sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu", ax=ax)
        st.pyplot(fig4)

        st.markdown("### 📆 Monthly Trend Analysis")
        data['month'] = data['date'].dt.to_period('M')
        monthly = data.groupby('month').agg({'revenue': 'sum', 'units_sold': 'sum'}).reset_index()
        st.bar_chart(monthly.set_index('month'))

        st.markdown("### 🔍 Correlation Matrix")
        st.dataframe(data.corr(numeric_only=True).round(2))                                                                                   
