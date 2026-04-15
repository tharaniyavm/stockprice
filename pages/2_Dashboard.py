import streamlit as st
import pandas as pd

# Set page to wide mode to accommodate side-by-side tables
st.set_page_config(layout="wide")

def get_processed_data(df):
    # Ensure date and types
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(['Ticker', 'date'])
    
    # Calculate performance per ticker
    summary = df.groupby('Ticker').agg(
        start_price=('close', 'first'),
        end_price=('close', 'last')
    )
    
    # Yearly return calculation
    summary['return_pct'] = ((summary['end_price'] - summary['start_price']) / summary['start_price']) * 100
    
    # Rounding prices
    summary['start_price'] = summary['start_price'].round(2)
    summary['end_price'] = summary['end_price'].round(2)
    summary['return_pct'] = summary['return_pct'].round(2)
    
    return summary

# 1. Data Loading
stockpricedf = pd.read_csv("FullData.csv")
performance_summary = get_processed_data(stockpricedf)

# 2. Market Summary Calculations
num_green = len(performance_summary[performance_summary['return_pct'] > 0])
num_red = len(performance_summary[performance_summary['return_pct'] < 0])
avg_price = stockpricedf['close'].mean()
avg_volume = stockpricedf['volume'].mean()

# 3. Top and Bottom Performers
top_10_green = performance_summary.sort_values(by='return_pct', ascending=False).head(10)
top_10_loss = performance_summary.sort_values(by='return_pct', ascending=True).head(10)

# --- STREAMLIT UI ---
st.title("📊 Stock Market Dashboard")

# Section 1: Market Summary Metrics
st.header("Market Summary")
m_col1, m_col2 = st.columns(2)
m_col1.metric("🟢 Green Stocks", f"{num_green}")
m_col2.metric("🔴 Red Stocks", f"{num_red}")
# m_col3.metric("Avg Market Price", f"₹{avg_price:.2f}")
# m_col4.metric("Avg Trading Volume", f"{avg_volume:,.0f}")

st.divider()

# Section 2: Performance Tables
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🚀 Top 10 Green Stocks")
    st.dataframe(
        top_10_green.style.format({"return_pct": "{:.2f}%", "start_price": "₹{:.2f}", "end_price": "₹{:.2f}"}),
        use_container_width=True
    )

with col_right:
    st.subheader("🔻 Top 10 Loss Stocks")
    st.dataframe(
        top_10_loss.style.format({"return_pct": "{:.2f}%", "start_price": "${:.2f}", "end_price": "${:.2f}"}),
        use_container_width=True
    )
