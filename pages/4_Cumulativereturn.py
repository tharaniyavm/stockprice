import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from database import df_to_mysql

st.set_page_config(layout="wide")

st.title("📈 Cumulative Return Analysis")

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
    df['daily_return'] = df.groupby('Ticker')['close'].pct_change()
    df['cum_return'] = df.groupby('Ticker')['daily_return'].transform(lambda x: (1 + x.fillna(0)).cumprod() - 1)

    # 3. Identify Top 5 Performing Stocks
    final_returns = df.groupby('Ticker')['cum_return'].last().sort_values(ascending=False)
    top_5_tickers = final_returns.head(5).index.tolist()
    top_5_df = df[df['Ticker'].isin(top_5_tickers)]

    # 4. Visualization with Matplotlib
    st.subheader("Top 5 Performing Stocks: Cumulative Growth")
    
    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Set dark theme style (optional, to match your previous plotly_dark theme)
    plt.style.use('dark_background')
    fig.patch.set_facecolor('#0e1117') # Match Streamlit dark background
    ax.set_facecolor('#0e1117')

    # Plot each ticker
    for ticker in top_5_tickers:
        ticker_data = top_5_df[top_5_df['Ticker'] == ticker]
        ax.plot(ticker_data['date'], ticker_data['cum_return'], label=ticker)

    # Formatting
    ax.set_title("Growth of Investment Over Time", color='white')
    ax.set_xlabel("Date", color='white')
    ax.set_ylabel("Cumulative Return", color='white')
    ax.legend()
    
    # Format Y-axis as percentage
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Display in Streamlit
    st.pyplot(fig)

    # 5. Display Summary Table
    st.write("### Final Cumulative Performance")
    summary_data = final_returns.head(5).reset_index()
    summary_data.columns = ['Ticker', 'Final Cumulative Return']
    st.table(summary_data.style.format({'Final Cumulative Return': '{:.2%}'}))
    
    # Adding the dataframe to database
    table_name = "cumulativereturn"
    df_to_mysql(top_5_df, table_name)

except FileNotFoundError:
    st.error("Please ensure 'FullData.csv' is in the project directory.")
