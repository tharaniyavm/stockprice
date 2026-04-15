import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from database import df_to_mysql

# Page configuration
st.set_page_config(layout="wide", page_title="Monthly Performance")


def load_and_merge_data():
    try:
        df = pd.read_csv('FullData.csv')
        sector_df = pd.read_csv('sectorData.csv')
        
        # Clean column names
        df.columns = df.columns.str.strip()
        sector_df.columns = sector_df.columns.str.strip()

        # Handle 'Symbol' split from image format "Name: Ticker"
        if 'Symbol' in sector_df.columns:
            split_data = sector_df['Symbol'].str.split(':', expand=True)
            sector_df['Company_Name'] = split_data[0].str.strip()
            sector_df['Ticker'] = split_data[1].str.strip()
        
        # Normalize Ticker column for merging
        ticker_col_price = next((c for c in df.columns if c.lower() in ['ticker', 'symbol']), None)
        if ticker_col_price:
            df = df.rename(columns={ticker_col_price: 'Ticker'})
        
        # Handle Date
        date_col = next((c for c in df.columns if c.lower() == 'date'), None)
        if date_col:
            df['date'] = pd.to_datetime(df[date_col])
            df['Month_Year'] = df['date'].dt.to_period('M').astype(str)
        
        return df.merge(sector_df, on='Ticker', how='left')
        
    except Exception as e:
        st.error(f"Error processing data: {e}")
        st.stop()

def get_top_5_gainers_losers(merged_df):
    price_col = next((c for c in merged_df.columns if any(x in c.lower() for x in ['close', 'price'])), None)
    
    if not price_col:
        raise ValueError("Could not find a price or close column.")

    # 1. Calculate Monthly Returns
    # Note: Sector is kept in the index to preserve it through the calculation
    monthly_perf = merged_df.groupby(['Month_Year', 'Ticker', 'sector'])[price_col].agg(['first', 'last'])
    monthly_perf['Returns'] = (monthly_perf['last'] - monthly_perf['first']) / monthly_perf['first']
    
    # 2. Get Top 5 Gainers and Losers
    # We use group_keys=False to prevent the groupby key from being added to the index twice
    top_5_gainers = (monthly_perf.groupby('Month_Year', group_keys=False)['Returns']
                     .nlargest(5)
                     .reset_index())
    top_5_gainers['Type'] = 'Top Gainer'
    
    top_5_losers = (monthly_perf.groupby('Month_Year', group_keys=False)['Returns']
                    .nsmallest(5)
                    .reset_index())
    top_5_losers['Type'] = 'Top Loser'
    
    # 3. Combine and Merge back the price data
    final_df = pd.concat([top_5_gainers, top_5_losers])
    
    # Merge back to get the 'first', 'last', and 'Sector' columns 
    # (Sector is now a column in the reset_index above)
    final_df = final_df.merge(monthly_perf[['first', 'last']], on=['Month_Year', 'Ticker'], how='left')
    
    return final_df.sort_values(['Month_Year', 'Type', 'Returns'], ascending=[True, True, False])


# Usage:
# top_5_df = get_top_5_gainers_losers(merged_df)

# To use it:
# df_final = get_top_gainers_losers(df_merged)



# Initialize Data
df = load_and_merge_data()

df_final = get_top_5_gainers_losers(df)
# st.dataframe(df_final, use_container_width=True)

#Adding the dataframe to database
table_name = "topgainerslosers"
df_to_mysql(df_final,table_name)

# --- SIDEBAR FILTERS ---
st.sidebar.header("Dashboard Filters")

# 1. Sector Filter
sector_col = 'sector' if 'sector' in df.columns else 'Sector'
all_sectors = sorted(df[sector_col].dropna().unique().tolist())
selected_sectors = st.sidebar.multiselect("Select Sectors", options=all_sectors, default=all_sectors)

# 2. Month Selector (Single Selection)
all_months = sorted(df['Month_Year'].unique().tolist(), reverse=True)
selected_month = st.sidebar.selectbox("Select Month to View", options=all_months)

# --- DATA PROCESSING ---
filtered_df = df[
    (df[sector_col].isin(selected_sectors)) & 
    (df['Month_Year'] == selected_month)
]

# Calculate monthly returns
close_col = 'close' if 'close' in df.columns else 'Close'
monthly_stats = filtered_df.groupby(['Ticker', 'Month_Year', sector_col])[close_col].agg(['first', 'last']).reset_index()
monthly_stats['Returns'] = ((monthly_stats['last'] - monthly_stats['first']) / monthly_stats['first']) * 100

# --- MAIN DASHBOARD DISPLAY ---
st.title(f"📊 Top 5 Gainers & Losers: {selected_month}")

if monthly_stats.empty:
    st.warning(f"No data available for the selected sectors in {selected_month}.")
else:
    # Identify Top 5 Gainers and Top 5 Losers for the SINGLE selected month
    top_5 = monthly_stats.nlargest(5, 'Returns')
    bottom_5 = monthly_stats.nsmallest(5, 'Returns')
    
    # Combine and sort for the chart
    plot_df = pd.concat([top_5, bottom_5]).sort_values('Returns', ascending=True)

    # Visualization - Centered in a column layout
    _, mid_col, _ = st.columns([1, 2, 1])
    
    with mid_col:
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['#e74c3c' if x < 0 else '#2ecc71' for x in plot_df['Returns']]
        
        sns.barplot(x='Returns', y='Ticker', data=plot_df, palette=colors, ax=ax)
        ax.set_title(f"Performance Distribution for {selected_month}", fontsize=14, fontweight='bold')
        ax.axvline(0, color='black', linewidth=1.5)
        ax.set_xlabel("% Return")
        ax.grid(axis='x', linestyle='--', alpha=0.7)
        
        st.pyplot(fig)
        plt.close()

    # Optional: Display Raw Data Table
    with st.expander("View Data Table"):
        st.dataframe(plot_df[['Ticker', sector_col, 'Returns']].sort_values('Returns', ascending=False), use_container_width=True)
