import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from database import df_to_mysql

# 1. Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("FullData.csv")
    df['date'] = pd.to_datetime(df['date'])
    return df

stockpricedf = load_data()

# 2. Sidebar Ticker Selection
st.sidebar.header("Filter Heatmap")
all_tickers = sorted(stockpricedf['Ticker'].unique())

selected_tickers = st.sidebar.multiselect(
    "Select Tickers for Correlation",
    options=all_tickers,
    default=all_tickers[:5] 
)

# 3. Correlation Logic
if len(selected_tickers) > 1:
    filtered_df = stockpricedf[stockpricedf['Ticker'].isin(selected_tickers)]
    pivot_df = filtered_df.pivot(index='date', columns='Ticker', values='close')
    
    # Calculate Correlation Matrix
    corr_matrix = pivot_df.corr()
    
    # Adding the dataframe to database
    table_name = "correlation"
    df_to_mysql(pivot_df, table_name)
    
    # Adding the correlation matrix to database
    table_name = "correlationmatrix"
    df_to_mysql(corr_matrix, table_name)

    # 4. Visualization with Matplotlib/Seaborn
    st.header(f"📉 Correlation Heatmap ({len(selected_tickers)} Stocks)")
    
    # Set the style and create the plot
    fig, ax = plt.subplots(figsize=(10, 8))
    plt.style.use('dark_background')
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#0e1117')

    # Create heatmap
    sns.heatmap(
        corr_matrix, 
        annot=True, 
        fmt=".2f", 
        cmap='RdBu_r', 
        vmin=-1, 
        vmax=1, 
        center=0,
        ax=ax,
        cbar_kws={'label': 'Correlation'}
    )

    # Styling adjustments
    ax.set_title("Stock Price Correlation Matrix", color='white', pad=20)
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)

    st.pyplot(fig)

    # Context for the user
    st.caption("Values closer to 1.0 indicate stocks that move together. Values closer to -1.0 indicate they move in opposite directions.")
else:
    st.warning("Please select at least **two** tickers in the sidebar to view the correlation heatmap.")
