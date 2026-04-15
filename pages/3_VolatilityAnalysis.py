import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from database import df_to_mysql

# Set page title
st.set_page_config(page_title="Volatility Analysis", layout="wide")

st.title("⚡ Stock Volatility Analysis")

# 1. Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("FullData.csv")
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(['Ticker', 'date'])
    return df

try:
    df = load_data()

    # 2. Metrics Calculation
    # Calculate daily returns for each stock: (Close - Prev Close) / Prev Close
    df['daily_return'] = df.groupby('Ticker')['close'].pct_change()

    # Compute standard deviation of daily returns (Volatility)
    volatility_df = df.groupby('Ticker')['daily_return'].std().reset_index()
    volatility_df.columns = ['Ticker', 'Volatility']

    # Get Top 10 most volatile stocks
    top_10_volatile = volatility_df.sort_values(by='Volatility', ascending=False).head(10)
    
   

    # 3. Visualization
    st.subheader("Top 10 Most Volatile Stocks")
    
    # Create Matplotlib Figure
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(top_10_volatile['Ticker'], top_10_volatile['Volatility'], color='firebrick')
    
    # Labels and Formatting
    ax.set_xlabel("Stock Ticker")
    ax.set_ylabel("Volatility (Standard Deviation)")
    ax.set_title("Highest Price Fluctuations Over the Year")
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.6)

    # Display in Streamlit
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.pyplot(fig)

    with col2:
        st.write("📊 **Raw Volatility Data**")
        st.dataframe(top_10_volatile.reset_index(drop=True), use_container_width=True)

    # Explanation for User
    st.info("""
    **Understanding Volatility:**
    - **High Volatility:** Prices fluctuate significantly day-to-day (Higher Risk).
    - **Low Volatility:** Prices are stable and move in small increments (Lower Risk).
    """)
    
     #Adding the dataframe to database
    table_name = "volatilityanalysis"
    df_to_mysql(top_10_volatile, table_name)

except FileNotFoundError:
    st.error("Error: 'FullData.csv' not found. Please ensure the file is in the same directory.")
